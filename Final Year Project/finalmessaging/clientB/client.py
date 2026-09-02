import sys
import selectors
import socket
import types
import encrypt
import decrypt
import keygen
import numpy as np
import pickle

sel = selectors.DefaultSelector()
inb = b""
state = "handshake"
peer_public_key = None
sk = np.load("privatekey.npy", allow_pickle= True)


def send_framed(outb: bytes, payload: bytes) -> bytes:
    length = len(payload).to_bytes(4, byteorder='big')
    return outb + length + payload


def recv_framed(buffer: bytes):
    frames = []
    while len(buffer) >= 4:
        length = int.from_bytes(buffer[:4], byteorder='big')
        if len(buffer) < 4 + length:
            break
        frames.append(buffer[4:4 + length])
        buffer = buffer[4 + length:]
    return frames, buffer


def start_connections(host, port):
    keygen.main()
    server_addr = (host, port)
    print(f"starting connection to {server_addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    data = types.SimpleNamespace(outb=b"")
    pk = np.load("publickey.npy", allow_pickle=True)
    seed = pk[0]
    b = pk[1].tobytes()
    payload = seed + b
    data.outb = send_framed(b"", payload)
    sel.register(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, data=data)
    sel.register(sys.stdin, selectors.EVENT_READ, data=sock)


def service_connection(key, mask):
    global state, peer_public_key, inb
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(65536)
        if recv_data:
            inb += recv_data
            frames, inb = recv_framed(inb)
            for frame in frames:
                if state == "handshake":
                    if frame in (b"Waiting for another client...\n", b"Connected.\n"):
                        print(frame.decode(), end="")
                    else:
                        seed = frame[:32]
                        b_array = np.frombuffer(frame[32:], dtype=np.int64)
                        peer_public_key = (seed, b_array)
                        state = "ready"
                        print("Key exchange complete.")
                elif state == "ready":
                    ct = pickle.loads(frame)
                    bits = decrypt.main(ct, sk)
                    bit_string = ''.join(str(b) for b in bits)
                    message = bytes(int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8)).decode()
                    print(message)
        else:
            print("Connection closed")
            sel.unregister(sock)
            sock.close()
            sys.exit()

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]


def service_input(key):
    message = sys.stdin.readline().strip()
    if not message or state != "ready":
        return
    bit_string = ''.join(format(byte, '08b') for byte in message.encode())
    encrypted = encrypt.main(bit_string, peer_public_key)
    serialize = pickle.dumps(encrypted)
    sock = key.data
    sock_key = sel.get_key(sock)
    sock_key.data.outb = send_framed(sock_key.data.outb, serialize)
    sel.modify(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, sock_key.data)


host, port = ("127.0.0.1", 65433)
start_connections(host, port)
sk = np.load("privatekey.npy", allow_pickle= True)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.fileobj == sys.stdin:
                service_input(key)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("exiting")
finally:
    sel.close()