import os
import socket

from setuptools import command

from bencode import bencode, bdecode
import threading

# from split_file import *

###########################################START################################################
#                                   PEER'S GLOBAL VARIABLES                                    #
###########################################START################################################

# Constants
HEADER = 1024
FORMAT = 'utf-8'
TRACKER_PORT = 7001
TRACKER_IP = "127.0.1.1"  # get from torrent file
SERVER_ADDR = (TRACKER_IP, TRACKER_PORT)

# Variables
running = True
tracker_connected = False
connected_peers = {}

Peer_set = []

missing_chunks = []
curr_chunks = []

this_peer_tracker_socket = None
peer_peer_socket_dict = {}

this_peer_info = {
    # "peer_id": peer_id,
    "ip": socket.gethostbyname(socket.gethostname()),
    "port": 5001,
    "downloaded": 0,
    "uploaded": 0
}
this_peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
this_peer.bind((this_peer_info["ip"], this_peer_info["port"]))

this_peer_data = {}
chunk_directory = "New_Memory_for_peer"


###########################################END##################################################
#                                   PEER'S GLOBAL VARIABLES                                    #
###########################################END##################################################

###########################################START################################################
#                                   PEER COMMAND FUNCTIONS                                     #
###########################################START################################################

# peer-tracker communication cmds:

def connect_tracker():  # done
    global tracker_connected, this_peer_tracker_socket
    this_peer_tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    this_peer_tracker_socket.connect(SERVER_ADDR)  # 1/ establish connection to tracker
    this_peer_tracker_socket.send(bencode(this_peer_info).encode(FORMAT))  # 2/ send bencoded peer_info to tracker
    received_msg = this_peer_tracker_socket.recv(2048).decode(
        FORMAT)  # 3/ tracker response "Tracker established connection to Peer[peer_ip]"
    print(bdecode(received_msg))
    tracker_connected = True  # 4/ tracker_connected = True
    get_peer_set()  # 5/ run /get_peer_set


def get_peer_set():  # done
    global Peer_set
    if not check_tracker_connected():  # 1/ run /check_tracker_connected. Go to step 2/ if returned True
        return
    this_peer_tracker_socket.send(
        bencode("/get_peer_set").encode(FORMAT))  # 2/ send "/get_peer_set" (string msg) to tracker.
    received_msg = this_peer_tracker_socket.recv(2048).decode(
        FORMAT)  # 3/ tracker response bencoded tracker's PEER_SET (string)
    Peer_set = bdecode(
        received_msg)  # 4/ bdecode tracker response (list if dictionaries [{},{},{}] ) and update peer's PEER_SET


def update_status_to_tracker():  # done
    if not check_tracker_connected():  # 1/ run /check_tracker_connected. Go to step 2/ if returned True
        return
    this_peer_tracker_socket.send(bencode("/update_status_to_tracker" + " " + bencode(this_peer_info)).encode(
        FORMAT))  # 2/ send "/update_status_to_tracker" [bencoded Peer_info] (string msg) to tracker
    received_msg = this_peer_tracker_socket.recv(2048).decode(
        FORMAT)  # 3/ Tracker response: "Tracker updated Peer[peer_ip] status"
    print(bdecode(received_msg))
    get_peer_set()


def disconnect_tracker():  # done
    global tracker_connected, this_peer_tracker_socket
    if not check_tracker_connected():  # 1/ run /check_tracker_connected. Go to step 2/ if returned True
        return
    this_peer_tracker_socket.send(bencode("/disconnect_tracker").encode(
        FORMAT))  # 2/ send bencoded "/disconnect_tracker" (string msg) to tracker
    received_msg = this_peer_tracker_socket.recv(2048).decode(
        FORMAT)  # 3/ tracker response "Peer[peer_id] disconnected from tracker"
    print(bdecode(received_msg))
    this_peer_tracker_socket.close()
    tracker_connected = False  # 4/ tracker_connected = False


def quit_torrent():  # done
    global running, tracker_connected, this_peer_tracker_socket
    if not check_tracker_connected():  # 1/ run /check_tracker_connected. Run /connect_tracker then Go to step 2/ if returned False
        connect_tracker()
    this_peer_tracker_socket.send(
        bencode("/quit_torrent").encode(FORMAT))  # 2/ send bencoded "/quit_torrent" (string msg) to tracker
    received_msg = this_peer_tracker_socket.recv(2048).decode(
        FORMAT)  # 3/ tracker response "Peer[peer_id] quited torrent"
    print(bdecode(received_msg))
    running = False  # 4/ leave the torrent and won't upload/ download chunks (peer.py program stops running)
    this_peer_tracker_socket.close()


# peer-peer communication request cmds:

def connect_peer(target_peer_IP, target_peer_port):  # done
    peer_peer_socket_dict[f"{target_peer_IP} {target_peer_port}"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_peer_addr = (target_peer_IP, target_peer_port)
    peer_peer_socket_dict[f"{target_peer_IP} {target_peer_port}"].connect(target_peer_addr)
    peer_peer_socket_dict[f"{target_peer_IP} {target_peer_port}"].send(
        bencode(this_peer_info).encode(FORMAT))  # 1/ establish connection to target peer
    received_msg = peer_peer_socket_dict[f"{target_peer_IP} {target_peer_port}"].recv(2048).decode(
        FORMAT)  # 2/ Target peer response: "Peer[target_peer_ip,target_peer_port] established connection to Peer[this_peer_ip]"
    print(bdecode(received_msg))
    connected_peers[f"{target_peer_IP} {target_peer_port}"] = True;


# def request_download(target_peer_IP, target_peer_port, missing_chunk):
#     if check_target_peer_connected(target_peer_IP, target_peer_port):
#         file_name = missing_chunk
#         peer_socket.connect((target_peer_IP,target_peer_port))
#         peer_socket.sendall(command.encode(FORMAT))
#
#         file_path = os.path.join(chunk_directory, file_name)
#         with open(file_path, 'wb') as file:
#             while True:
#                 data = peer_socket.recv(1024)
#                 if not data:
#                     break
#                 file.write(data)
#         peer_socket.close()
def request_download(target_peer_IP, target_peer_port, missing_chunk):
    if not check_target_peer_connected(target_peer_IP,
                                       target_peer_port):  # 1/ run /check_tracker_connected. Go to step 2/ if returned True
        return
    file_name = missing_chunk
    peer_socket.connect((target_peer_IP, target_peer_port))
    #1.bencode
    #2.encode

    request = bencode(f"/request_download {target_peer_IP},{target_peer_port},{file_name}")
    peer_socket.sendall(request.encode(FORMAT)) #2/ This peer todo: send bencoded "/request_download [target_peer_IP] [target_peer_port] [missing_chunks[i]]" (string msg) to [target_peer_IP].([missing_chunks[i]] is name of the chunk file)
    download_msg = peer_socket.recv(HEADER).decode(FORMAT) #3/ Target peer response: "Peer[target_peer_IP target_peer_port] starts uploading chunk [missing_chunks[i]] to Peer[this_peer_ip]"

    print(download_msg)

    file_path = os.path.join(chunk_directory, file_name) #4 This peer todo: Save new chunk to Memory_peer folder
    with open(file_path, 'wb') as file:
        while True:
            data = peer_socket.recv(1024)
            if not data:
                break
            file.write(data)

        peer_socket.close()


def upload(request_peer_ip, chunk_name):
    pass


def disconnect_peer(target_peer_IP, target_peer_port):  # done
    if not check_target_peer_connected(target_peer_IP,
                                       target_peer_port):  # 1/ run /check_tracker_connected. Go to step 2/ if returned True
        return
    peer_peer_socket_dict[f"{target_peer_IP} {target_peer_port}"].send(
        bencode(f"/disconnect_peer {target_peer_IP} {target_peer_port}").encode(
            FORMAT))  # 2/ send bencoded "/disconnect_peer [target_peer_IP] [target_peer_port]" to [target_peer_IP,target_peer_port]
    received_msg = peer_peer_socket_dict[f"{target_peer_IP} {target_peer_port}"].recv(2048).decode(FORMAT)
    print(bdecode(received_msg))
    del peer_peer_socket_dict[f"{target_peer_IP} {target_peer_port}"]
    connected_peers[f"{target_peer_IP} {target_peer_port}"] = False


# peer functionality cmds:

def check_tracker_connected():  # done
    if not tracker_connected:
        print("Peer is not connected to tracker")
    return tracker_connected


def check_target_peer_connected(target_peer_IP, target_peer_port):  # done
    if not connected_peers[f"{target_peer_IP} {target_peer_port}"]:
        print(
            f"Target Peer[{target_peer_IP},{target_peer_port}] is not connected to current Peer[{this_peer_info['ip']} {this_peer_info['port']}]")
    return connected_peers[f"{target_peer_IP} {target_peer_port}"]


def check_chunk(chunk_name):
    pass


def see_peer_set():  # done
    print(Peer_set)  # 1/ print Peer_set


def see_connected():  # done
    print(connected_peers)


def see_current_chunks():
    pass


def see_missing_chunks():
    pass


def merge_chunks():
    pass


###########################################END##################################################
#                                   PEER COMMAND FUNCTIONS                                     #
###########################################END##################################################

###########################################START################################################
#                                   PEER LISTENING FUNCTIONS                                   #
###########################################START################################################

# def handle_request_peer_connection(conn, this_peer_ip):  # done
#
#     request_peer_info_msg = conn.recv(HEADER).decode(FORMAT)
#     request_peer_info = bdecode(request_peer_info_msg)
#     request_peer_ip = request_peer_info['ip']
#     request_peer_port = request_peer_info['port']
#     print(f"\n[NEW CONNECTION] {request_peer_ip} connected.")  # 1/ establish connection to [request_peer_ip]
#
#     # 2/ send "Peer[this_peer_ip,this_peer_port] established connection to Peer[request_peer_ip,request_peer_port]" (string msg) to [request_peer_ip]
#     conn.send(bencode(
#         f"Peer[{this_peer_info['ip']},{this_peer_info['port']}] disconnected from Peer[{request_peer_ip},{request_peer_port}]").encode(
#         FORMAT))
#
#     # send to peer
#     # 3/ connected_peers[requested_peer_IP]=True
#     connected_peers[f"{request_peer_ip} {request_peer_port}"] = True
#
#     # 4/ Start a while-loop thread to listen to [requested_peer_ip,request_peer_port]
#     while connected_peers[f"{request_peer_ip} {request_peer_port}"]:
#         received_msg = conn.recv(HEADER).decode(FORMAT)
#         if received_msg:
#             msg = bdecode(received_msg)
#             print(f"[{request_peer_ip},{request_peer_port}] {msg}")
#
#             msg_parts = msg.split()
#             match msg_parts[0]:
#                 case "/disconnect_peer":  # [target_peer_IP] [target_peer_port] # done
#                     # 1/ check if input is valid
#                     if (len(msg_parts) != 3):
#                         print("Invalid format! Please provide both request peer IP and port.")
#                         return
#                     if (not msg_parts[1] or not msg_parts[2]):
#                         print("Invalid format! Please provide both request peer IP and port.")
#                     else:
#                         print(f"[REQUEST PEER DISCONNECTED THIS PEER] {msg_parts[1]}")
#                         # 2/ send "Peer[this_peer_id,this_peer_port] disconnected from Peer[target_peer_ip,target_peer_port]"
#                         conn.send(bencode(
#                             f"Peer[{this_peer_info['ip']},{this_peer_info['port']}] disconnected from Peer[{request_peer_ip},{request_peer_port}]").encode(
#                             FORMAT))
#
#                         connected_peers[f"{request_peer_ip} {request_peer_port}"] = False  # 3/
#                 case _:
#                     conn.send(bencode("Invalid command").encode(FORMAT))
#     conn.close()

def send_file(client_socket, file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        client_socket.sendall(data)
def handle_request_peer_connection(conn, this_peer_ip):  # done
    request_peer_info_msg = conn.recv(HEADER).decode(FORMAT)
    print("Received message:", request_peer_info_msg)  # Add a print statement to show the received message
    request_peer_info = bdecode(request_peer_info_msg)
    request_peer_ip = request_peer_info['ip']
    request_peer_port = request_peer_info['port']
    print(f"\n[NEW CONNECTION] {request_peer_ip} connected.")  # 1/ establish connection to [request_peer_ip]

    # 2/ send "Peer[this_peer_ip,this_peer_port] established connection to Peer[request_peer_ip,request_peer_port]" (string msg) to [request_peer_ip]
    conn.send(bencode(
        f"Peer[{this_peer_info['ip']},{this_peer_info['port']}] connected from Peer[{request_peer_ip},{request_peer_port}]").encode(
        FORMAT))

    # send to peer
    # 3/ connected_peers[requested_peer_IP]=True
    connected_peers[f"{request_peer_ip} {request_peer_port}"] = True

    # 4/ Start a while-loop thread to listen to [requested_peer_ip,request_peer_port]
    while connected_peers[f"{request_peer_ip} {request_peer_port}"]:
        received_msg = conn.recv(HEADER).decode(FORMAT)
        if received_msg:
            msg = bdecode(received_msg)
            print(f"[{request_peer_ip},{request_peer_port}] {msg}")

            msg_parts = msg.split()
            match msg_parts[0]:
                case "/disconnect_peer":  # [target_peer_IP] [target_peer_port] # done
                    # 1/ check if input is valid
                    if (len(msg_parts) != 3):
                        print("Invalid format! Please provide both request peer IP and port.")
                        return
                    if (not msg_parts[1] or not msg_parts[2]):
                        print("Invalid format! Please provide both request peer IP and port.")
                    else:
                        print(f"[REQUEST PEER DISCONNECTED THIS PEER] {msg_parts[1]}")
                        # 2/ send "Peer[this_peer_id,this_peer_port] disconnected from Peer[target_peer_ip,target_peer_port]"
                        conn.send(bencode(
                            f"Peer[{this_peer_info['ip']},{this_peer_info['port']}] disconnected from Peer[{request_peer_ip},{request_peer_port}]").encode(
                            FORMAT))

                        connected_peers[f"{request_peer_ip} {request_peer_port}"] = False  # 3/

                case _:
                    conn.send(bencode("Invalid command").encode(FORMAT))

    conn.close()

###########################################END##################################################
#                                   PEER LISTENING FUNCTIONS                                   #
###########################################END##################################################

###########################################START################################################
#                                       OTHER FUNCTIONS                                        #
###########################################START################################################

# def save_chunk(chunk_number, chunk_data):
#     this_peer_data[chunk_number] = chunk_data

# def get_chunk(chunk_number):
#     return this_peer_data.get(chunk_number, None)

# def set_chunk_directory(chunk_directory):
#     chunk_directory = chunk_directory

# def send(msg,target_ip):
#     message = bencode(msg).encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))
#     this_peer_socket.send(send_length)
#     this_peer_socket.send(message)

#     # chunk_dir_length = len(chunk_directory)
#     # peer_socket.send(str(chunk_dir_length).encode(FORMAT))
#     # peer_socket.send(chunk_directory.encode(FORMAT))


#     received_msg = this_peer_socket.recv(2048).decode(FORMAT)
#     print(received_msg)
#     print(type(received_msg))
#     if received_msg == "Disconnected":
#         return False
#     #################################################
#     # RECEIVE PEER SET HANDLER
#     # TODO
#     #################################################
#     return True

# def save_chunks_to_peer(chunk_directory): # check file in [chunk_directory], then split file into chunks and save them to [chunk_directory]
#     saved_chunks = 0  # Initialize counter for saved chunks
#     for filename in os.listdir(chunk_directory):
#         if filename.startswith('File_split.mp4.part'):  # Check if the file is a chunk
#             chunk_number = int(filename.split('part')[1])  # Extract chunk number from filename
#             file_path = os.path.join(chunk_directory, filename)
#             with open(file_path, 'rb') as f:
#                 chunk_data = f.read()  # Read chunk data
#                 save_chunk(chunk_number, chunk_data)  # Save chunk to peer_data
#                 saved_chunks += 1  # Increment the counter for saved chunks
#     if saved_chunks == 70:
#         print("All 70 chunks have been successfully saved.")

###########################################END##################################################
#                                       OTHER FUNCTIONS                                        #
###########################################END##################################################