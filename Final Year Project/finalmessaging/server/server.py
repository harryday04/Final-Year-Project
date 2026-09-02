import socket
import selectors
import types
import pickle


sel = selectors.DefaultSelector()


class Client:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.outb = b""
        self.public_key = None
        self.peer = None
        self.state = "handshake"
        self.inb = b""
    
    def is_paired(self):
        return self.peer is not None
    
    def set_peer(self, peer):
        self.peer = peer
        peer.peer = self
    
    def send(self, data: bytes):
        length = len(data).to_bytes(4, byteorder='big')
        self.outb += length + data
        sel.modify(self.conn, selectors.EVENT_READ | selectors.EVENT_WRITE, self)
        
    def disconnect(self):
        if self.peer:
            self.peer.peer = None
            print("Closing channel")
        if channel["waiting"] is self:
            channel["waiting"] = None
        sel.unregister(self.conn)
        self.conn.close()


channel = {"waiting": None}


def pair(client: Client):
    waiting = channel["waiting"]
    if waiting is None:
        print("Waiting for endpoint..")
        channel["waiting"] = client
        client.send(b"Waiting for another client...\n")
    else:
        print("Channel open")
        client.set_peer(waiting)
        channel["waiting"] = None
        client.send(b"Connected.\n")
        waiting.send(b"Connected.\n")


def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"Client connected: {addr}")
    conn.setblocking(False)
    client = Client(conn, addr)
    sel.register(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, data=client)
    pair(client)

def recv_framed(buffer: bytes):
    """
    Extract complete frames from a byte buffer.
    Returns (list of complete payloads, remaining incomplete bytes).
    """
    frames = []
    while len(buffer) >= 4:
        length = int.from_bytes(buffer[:4], byteorder='big')
        if len(buffer) < 4 + length:
            break  # incomplete frame, wait for more data
        frames.append(buffer[4:4 + length])
        buffer = buffer[4 + length:]
    return frames, buffer

def service_connection(key, mask):
    client: Client = key.data
    sock = key.fileobj

    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(65536)
        if recv_data:
            client.inb += recv_data
            frames, client.inb = recv_framed(client.inb)
            for frame in frames:
                if client.state == "handshake":
                    client.public_key = frame
                    if client.peer and client.peer.public_key:
                        client.send(client.peer.public_key)
                        client.peer.send(client.public_key)
                        client.state = "ready"
                        client.peer.state = "ready"
                elif client.state == "ready":
                    if client.is_paired():
                        client.peer.send(frame)
        else:
            print(f"Closing connection to {client.addr}")
            if client.peer:
                client.peer.send(b"Peer disconnected.\n")
                client.peer.disconnect()
            client.disconnect()

    if mask & selectors.EVENT_WRITE:
        if client.outb:
            sent = sock.send(client.outb)
            client.outb = client.outb[sent:]
        if not client.outb:
            sel.modify(sock, selectors.EVENT_READ, client)


host, port = ("0.0.0.0", 65433)
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {host}:{port}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
finally:
    print("Shutting down server...")
    for key in list(sel.get_map().values()):
        sock = key.fileobj
        try:
            sel.unregister(sock)
        except Exception:
            pass
        try:
            sock.close()
        except Exception:
            pass
    sel.close()