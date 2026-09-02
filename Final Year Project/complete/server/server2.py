import socket
import selectors
import types


sel = selectors.DefaultSelector()



channel = {"waiting" : None, "pair" : {}}
    
def pair(channel, conn):
    if channel["waiting"] is None:
        print("Waiting for endpoint..")
        channel["waiting"] =  conn

        key = sel.get_key(conn)
        key.data.outb = b"Waiting for another client...\n"
        sel.modify(conn, selectors.EVENT_READ | selectors.EVENT_WRITE, key.data)
    else:
        print("Channel open")
        peer = channel["waiting"]
        channel["pair"][conn] = peer     
        channel["pair"][peer] = conn
        channel["waiting"] = None

        for client in (conn, peer):
            key = sel.get_key(client)
            key.data.outb += b"Connected.\n"
            sel.modify(client, selectors.EVENT_READ | selectors.EVENT_WRITE, key.data)

def unpair(channel, conn):
    client = channel["pair"].pop(conn, None)
    if client:
        channel["pair"].pop(client, None)
        print("Closing Channel")
        sel.unregister(client)
        client.close()
    
    if channel["waiting"] == conn:
        channel["waitng"] = None

def get_peer(channel, conn):
    return channel["pair"].get(conn)

def accept_wrapper(sock):
    conn, addr = sock.accept()
    print(f"client connected{addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, outb = b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    pair(channel, conn)

def service_connection(key, mask):  
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)
        if recv_data:
            peer = get_peer(channel, sock)
            peer_key = sel.get_key(peer)
            peer_key.data.outb += recv_data
            sel.modify(peer, selectors.EVENT_READ | selectors.EVENT_WRITE, peer_key.data)
        else:
            print(f"closing connection to {data.addr}")
            unpair(channel, sock)
            sel.unregister(sock)
            sock.close()
            
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            sent = sock.send(data.outb)
            data.outb = data.outb[sent:]
        if not data.outb:
            sel.modify(sock, selectors.EVENT_READ, data)


host, port = ("127.0.0.1", 65432)
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"listening on {host,port}")
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

    # Close all registered sockets
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