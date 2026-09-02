# import numpy as np
# import sys
# import selectors
# import socket
# import types
# import encrypt
# import decrypt
# import keygen

# sel = selectors.DefaultSelector()

# def start_connections(host, port):
#     server_addr = (host, port)
#     print(f"starting connection to {server_addr}")
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.setblocking(False)
#     sock.connect_ex(server_addr)
#     data = types.SimpleNamespace(outb = b"")
#     sel.register(sock, selectors.EVENT_READ, data=data)
#     sel.register(sys.stdin, selectors.EVENT_READ, data=sock)
#     print("generating keys.. ")
#     keygen.main()
#     send_public(sock)
    

# def send_public(sock):
#     sel.modify(sock, selectors.EVENT_READ | selectors.EVENT_WRITE)
#     with open("publickey.npy", "rb") as f:
#         while chunk := f.read(4096):
#             sock.sendall    (chunk)
#     sel.modify(sock, selectors.EVENT_READ)
    


# def service_connection(key,mask):
#     sock = key.fileobj
#     data = key.data
#     if mask & selectors.EVENT_READ:
#         recv_data = sock.recv(1024)
#         if recv_data:
#             print(recv_data.decode(), end="")
#         else:
#             print("Connection closed")
#             sel.unregister()
#             sock.close()
#             sys.exit()

#     if mask & selectors.EVENT_WRITE:
#         if data.outb:   
#             sent = sock.send(data.outb)  # Should be ready to write
#             data.outb = data.outb[sent:]

# def service_input(key):
#     message = sys.stdin.readline()
#     sock = key.data
#     if message:
#         sock_key = sel.get_key(sock)
#         sock_data = sock_key.data
#         sock_data.outb = message.encode()
#         sel.modify(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, sock_data)



# host, port = ("127.0.0.1", 65432)

# start_connections(host, port)

# try:
#     while True:
#         events = sel.select(timeout=None)
#         for key, mask in events:
#             if key.fileobj == sys.stdin:
#                 service_input(key)
#             else:
#                 service_connection(key, mask) 

# except KeyboardInterrupt:
#     print("exiting")
# finally:
#     sel.close()

import sys
import selectors
import socket
import types
import encrypt
import decrypt
import keygen

sel = selectors.DefaultSelector()

def start_connections(host, port):
    server_addr = (host, port)
    print(f"starting connection to {server_addr}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(server_addr)
    data = types.SimpleNamespace(outb = b"")
    sel.register(sock, selectors.EVENT_READ, data=data)
    sel.register(sys.stdin, selectors.EVENT_READ, data=sock)


def service_connection(key,mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            print(recv_data.decode(), end="")
        else:
            print("Connection closed")
            sel.unregister(sock)
            sock.close()
            sys.exit()

    if mask & selectors.EVENT_WRITE:
        if data.outb:   
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
            
def service_input(key):
    message = sys.stdin.readline()
    sock = key.data
    if message:
        sock_key = sel.get_key(sock)
        sock_data = sock_key.data
        sock_data.outb = message.encode()
        sel.modify(sock, selectors.EVENT_READ | selectors.EVENT_WRITE, sock_data)



host, port = ("127.0.0.1", 65432)

start_connections(host, port)



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

