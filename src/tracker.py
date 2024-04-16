import os
from time import sleep
import threading
import socket
from bencode import bencode,bdecode


HEADER = 1024
PORT = 7001
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
LOCK = threading.Lock()
PEER_SET=[]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_peer_connection(conn, tracker_ip):  # Run for each Peer connected

    # Receive peer information
    # peer_info_length = conn.recv(HEADER).decode(FORMAT)
    # peer_info_length = int(peer_info_length)
    # peer_info = bdecode(conn.recv(peer_info_length).decode(FORMAT))

    peer_info_msg=conn.recv(HEADER).decode(FORMAT)
    peer_info=bdecode(peer_info_msg)
    peer_ip=peer_info['ip']
    peer_port=peer_info['port']
    print(f"\n[NEW CONNECTION] {peer_ip} connected.")

    conn.send(bencode(f"Tracker established connection to Peer[{peer_ip},{peer_port}]").encode(FORMAT)) # send to peer

    # Update Peer Set when new Peer connects
    if not peer_info in PEER_SET:
        PEER_SET.append(peer_info)

    connected = True
    while connected:
        received_msg = conn.recv(HEADER).decode(FORMAT)
        if received_msg:
            msg = bdecode(received_msg)
            print(f"[{peer_ip},{peer_port}] {msg}")

            msg_parts=msg.split()
            match msg_parts[0]:
                case "/get_peer_set":
                    print(f"[PEER SET] {PEER_SET}")
                    conn.send(bencode(PEER_SET).encode(FORMAT))  # send PEER SET string
                    connected = True
                case "/disconnect_tracker":
                    print(f"[PEER DISCONNECTED TRACKER] {peer_ip},{peer_port}")
                    conn.send(bencode(f"Peer[{peer_ip},{peer_port}] disconnected from tracker").encode(FORMAT))  # send to peer
                    connected = False
                case "/quit_torrent":
                    print(f"[PEER QUITED TORRENT] {peer_ip},{peer_port}")
                    conn.send(bencode(f"Peer[{peer_ip},{peer_port}] quited torrent").encode(FORMAT))  # send to peer
                    PEER_SET.remove(peer_info)
                    connected=False
                case "/update_status":
                    print(f"[PEER UPDATE] {peer_ip},{peer_port}")
                    ###########################################
                    # UPDATE PEER SET HERE
                    # TODO
                    ###########################################
                case _:
                    conn.send(bencode("Invalid command").encode(FORMAT))
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Tracker is listening on {SERVER}")
    while True:
        conn,tracker_ip = server.accept() # detect a client connect
        thread = threading.Thread(target=handle_peer_connection,args=(conn,tracker_ip)) # create a "listening peer" thread
        thread.start()
        print(f"tracker_ip??:{tracker_ip}") # temp
        print(f"[ACTIVE CONNECTION] {threading.active_count()-1}")
        

if __name__ == "__main__":
    print("[STARTING] Tracker is starting")
    start()
