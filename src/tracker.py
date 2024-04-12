import os
from time import sleep
import threading
import socket
from bencode import bencode,bdecode


HEADER = 1024
PORT = 7000
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
LOCK = threading.Lock()
PEER_SET=[]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_peer_connection(conn, peer_ip):  # Run for each Peer connected
    print(f"\n[NEW CONNECTION] {peer_ip} connected.")

    # Receive peer information
    peer_info_length = conn.recv(HEADER).decode(FORMAT)
    peer_info_length = int(peer_info_length)
    peer_info = bdecode(conn.recv(peer_info_length).decode(FORMAT))

    conn.send(f"Tracker established connection to Peer[{peer_ip}]".encode(FORMAT)) # send to peer

    # Update Peer Set when new Peer connects
    PEER_SET.append(peer_info)

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = bdecode(conn.recv(msg_length).decode(FORMAT))
            print(f"[{peer_ip}] {msg}")

            msg_parts=msg.split()
            match msg_parts[0]:
                case "/get_peer_set":
                    print(f"[PEER SET] {PEER_SET}")
                    conn.send(bencode(PEER_SET).encode(FORMAT))  # send PEER SET string
                    connected = True
                case "/disconnect_tracker":
                    print(f"[PEER DISCONNECTED TRACKER] {peer_ip}")
                    conn.send(f"Peer[{peer_ip}] disconnected from tracker".encode(FORMAT))  # send to peer
                    connected = False
                case "/quit_torrent":
                    print(f"[PEER QUITED TORRENT] {peer_ip}")
                    conn.send(f"Peer[{peer_ip}] quited torrent".encode(FORMAT))  # send to peer
                    PEER_SET.pop(peer_info)
                    connected=False
                case "/update_status":
                    print(f"[PEER UPDATE] {peer_ip}")
                    ###########################################
                    # UPDATE PEER SET HERE
                    # TODO
                    ###########################################
                case _:
                    conn.send("Invalid command".encode(FORMAT))
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Tracker is listening on {SERVER}")
    while True:
        conn,peer_ip = server.accept() # detect a client connect
        thread = threading.Thread(target=handle_peer_connection,args=(conn,peer_ip)) # create a "listening peer" thread
        thread.start()
        print(f"\n[ACTIVE CONNECTION] {threading.active_count()-1}")
        

if __name__ == "__main__":
    print("[STARTING] Tracker is starting")
    start()
