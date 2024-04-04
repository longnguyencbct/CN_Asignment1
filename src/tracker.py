from time import sleep
import threading
import socket
from bencode import bencode,bdecode

HEADER = 1024
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'

PEER_SET=[]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


    
def  handle_client(conn, addr): # Run for each Peer connected
    print(f"\n[NEW CONNECTION] {addr} connected.")
    #################################################
    # GET PEER INFO HERE
    # TODO
    peer_info_length= conn.recv(HEADER).decode(FORMAT)
    peer_info_length = int(peer_info_length)
    peer_info = bdecode(conn.recv(peer_info_length).decode(FORMAT))

    #################################################
    #################################################
    # Update Peer Set when new Peer connects
    PEER_SET.append(peer_info)
    #################################################
    conn.send("Updated Peer Set".encode(FORMAT)) # send "Updated Peer Set"
    connected = True
    while connected:
        msg_length= conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = bdecode(conn.recv(msg_length).decode(FORMAT))
            print(f"[{addr}] {msg}")


            match msg:
                case "/quit":
                    print(f"[PEER LEFT] {addr}")
                    conn.send("Disconnected".encode(FORMAT)) # send "Disconnected"
                    connected = False
                case "/get_peer_set":
                    print(f"[PEER SET] {PEER_SET}")
                    print(type(msg))
                    conn.send(bencode(PEER_SET).encode(FORMAT)) # send PEER SET string
                    connected = True
                case "/update_status":
                    print(f"[PEER UPDATE] {addr}")
                    ###########################################
                    # UPDATE PEER SET HERE
                    # TODO
                    ###########################################
                    connected = True
                case _:
                    conn.send("Invalid command".encode(FORMAT))
                    connected = True
    #################################################
    # Update Peer Set when Peer disconnect
    PEER_SET.remove(peer_info)
    #################################################
    conn.close()
def start():
    server.listen()
    print(f"[LISTENING] Tracker is listening on {SERVER}")
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
        print(f"\n[ACTIVE CONNECTION] {threading.active_count()-1}")
        

if __name__ == "__main__":
    print("[STARTING] Tracker is starting")
    start()
