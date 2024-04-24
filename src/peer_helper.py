import os
import socket
from bencode import bencode,bdecode
import threading
import json
#from split_file import *

###########################################START################################################
#                                   PEER'S GLOBAL VARIABLES                                    #
###########################################START################################################

# Constants
HEADER = 1024
FORMAT = 'utf-8'
TRACKER_PORT=0
TRACKER_IP = "" # get from torrent file
CHUNK_SIZE = 0
TRACKER_ADDR = None
TORRENT_STRUCTURE={}
MEMORY_DIR="Memory"
TORRENT_FILE="torrent_file"

# Variables
running=True
tracker_connected=False
connected_peers={}



Peer_set=[]

this_peer_tracker_socket = None
peer_peer_socket_dict={}

this_peer_info={
    # "peer_id": peer_id,
    "ip": socket.gethostbyname(socket.gethostname()),
    "port": 5000,
    "chunk_status": {}, # {"filesplit_part1":True,"filesplit_part2":False,...} True=exist in memory; False=missing
    "downloaded": 0,
    "uploaded": 0
}
this_peer_listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
this_peer_listening_socket.bind((this_peer_info["ip"], this_peer_info["port"]))



###########################################END##################################################
#                                   PEER'S GLOBAL VARIABLES                                    #
###########################################END##################################################

###########################################START################################################
#                                   PEER COMMAND FUNCTIONS                                     #
###########################################START################################################

# peer-tracker communication cmds: 

def connect_tracker(): # done
    global tracker_connected,this_peer_tracker_socket
    this_peer_tracker_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    this_peer_tracker_socket.connect(TRACKER_ADDR)                           # 1/ establish connection to tracker
    this_peer_tracker_socket.send(bencode(this_peer_info).encode(FORMAT))                  # 2/ send bencoded peer_info to tracker
    received_msg = this_peer_tracker_socket.recv(2048).decode(FORMAT)       # 3/ tracker response "Tracker established connection to Peer[peer_ip]"
    print(bdecode(received_msg))
    tracker_connected = True                                        # 4/ tracker_connected = True 
    get_peer_set()                                                  # 5/ run /get_peer_set

def get_peer_set(): # done
    global Peer_set
    if not check_tracker_connected():                               # 1/ run /check_tracker_connected. Go to step 2/ if returned True
        return
    this_peer_tracker_socket.send(bencode("/get_peer_set").encode(FORMAT))                 # 2/ send "/get_peer_set" (string msg) to tracker.
    received_msg = this_peer_tracker_socket.recv(2048).decode(FORMAT)       # 3/ tracker response bencoded tracker's PEER_SET (string)
    Peer_set=bdecode(received_msg)                                  # 4/ bdecode tracker response (list if dictionaries [{},{},{}] ) and update peer's PEER_SET

def update_status_to_tracker(): # done
    if not check_tracker_connected():                               # 1/ run /check_tracker_connected. Go to step 2/ if returned True
        return
    this_peer_tracker_socket.send(bencode("/update_status_to_tracker"+" "+bencode(this_peer_info)).encode(FORMAT))                 # 2/ send "/update_status_to_tracker" [bencoded Peer_info] (string msg) to tracker
    received_msg = this_peer_tracker_socket.recv(2048).decode(FORMAT)       # 3/ Tracker response: "Tracker updated Peer[peer_ip] status"
    print(bdecode(received_msg))
    get_peer_set()

def disconnect_tracker(): # done
    global tracker_connected,this_peer_tracker_socket
    if not check_tracker_connected():                               # 1/ run /check_tracker_connected. Go to step 2/ if returned True
        return
    this_peer_tracker_socket.send(bencode("/disconnect_tracker").encode(FORMAT))           # 2/ send bencoded "/disconnect_tracker" (string msg) to tracker 
    received_msg = this_peer_tracker_socket.recv(2048).decode(FORMAT)       # 3/ tracker response "Peer[peer_id] disconnected from tracker"
    print(bdecode(received_msg))
    this_peer_tracker_socket.close()
    tracker_connected = False                                       # 4/ tracker_connected = False

def quit_torrent(): # done
    global running,tracker_connected,this_peer_tracker_socket
    if not check_tracker_connected():                               # 1/ run /check_tracker_connected. Run /connect_tracker then Go to step 2/ if returned False
        connect_tracker()
    this_peer_tracker_socket.send(bencode("/quit_torrent").encode(FORMAT))                 # 2/ send bencoded "/quit_torrent" (string msg) to tracker 
    received_msg = this_peer_tracker_socket.recv(2048).decode(FORMAT)       # 3/ tracker response "Peer[peer_id] quited torrent"
    print(bdecode(received_msg))
    running=False                                                   # 4/ leave the torrent and won't upload/ download chunks (peer.py program stops running)
    this_peer_tracker_socket.close()
    


# peer-peer communication request cmds:

def connect_peer(target_peer_IP,target_peer_port): # done
    peer_peer_socket_dict[f"{target_peer_IP} {target_peer_port}"] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_peer_addr= (target_peer_IP,target_peer_port)
    peer_peer_socket_dict[f"{target_peer_IP} {target_peer_port}"].connect(target_peer_addr) 
    peer_peer_socket_dict[f"{target_peer_IP} {target_peer_port}"].send(bencode(this_peer_info).encode(FORMAT))                           # 1/ establish connection to target peer
    received_msg = peer_peer_socket_dict[f"{target_peer_IP} {target_peer_port}"].recv(2048).decode(FORMAT)           # 2/ Target peer response: "Peer[target_peer_ip,target_peer_port] established connection to Peer[this_peer_ip]"
    print(bdecode(received_msg))
    connected_peers[f"{target_peer_IP} {target_peer_port}"]=True; 
    
def request_download(target_peer_ip,target_peer_port,missing_chunk):
    this_peer_info["downloaded"]+=1

# def upload(request_peer_ip,request_peer_port,chunk_name):
#     this_peer_info["uploaded"]+=1

def disconnect_peer(target_peer_IP,target_peer_port): # done
    if not check_target_peer_connected(target_peer_IP,target_peer_port):                               # 1/ run /check_tracker_connected. Go to step 2/ if returned True
        return
    peer_peer_socket_dict[f"{target_peer_IP} {target_peer_port}"].send(bencode(f"/disconnect_peer {target_peer_IP} {target_peer_port}").encode(FORMAT))  # 2/ send bencoded "/disconnect_peer [target_peer_IP] [target_peer_port]" to [target_peer_IP,target_peer_port]
    received_msg = peer_peer_socket_dict[f"{target_peer_IP} {target_peer_port}"].recv(2048).decode(FORMAT)
    print(bdecode(received_msg))
    del peer_peer_socket_dict[f"{target_peer_IP} {target_peer_port}"]
    connected_peers[f"{target_peer_IP} {target_peer_port}"]=False


# peer functionality cmds:

def check_tracker_connected(): # done
    if not tracker_connected:
        print("Peer is not connected to tracker")
    return tracker_connected

def check_target_peer_connected(target_peer_IP,target_peer_port): #done
    if not connected_peers[f"{target_peer_IP} {target_peer_port}"]:
        print(f"Target Peer[{target_peer_IP},{target_peer_port}] is not connected to current Peer[{this_peer_info['ip']} {this_peer_info['port']}]")
    return connected_peers[f"{target_peer_IP} {target_peer_port}"]

def see_this_peer_info():
    print_dict(this_peer_info)

def check_chunk(chunk_name):
    pass

def see_peer_set(): # done
    for peer in Peer_set:
        print("==========================================")
        print_dict(peer) # 1/ print Peer_set
        print("==========================================")

def see_connected(): # done
    print(connected_peers)

def see_chunk_status():
    print("==================================")
    print_dict(this_peer_info["chunk_status"])
    print("==================================")

def merge_chunks():
    pass

###########################################END##################################################
#                                   PEER COMMAND FUNCTIONS                                     #
###########################################END##################################################

###########################################START################################################
#                                   PEER LISTENING FUNCTIONS                                   #
###########################################START################################################

def handle_request_peer_connection(conn): # done

    request_peer_info_msg=conn.recv(HEADER).decode(FORMAT)
    request_peer_info=bdecode(request_peer_info_msg)
    this_peer_ip=this_peer_info["ip"]
    this_peer_port=this_peer_info["port"]
    request_peer_ip=request_peer_info['ip']
    request_peer_port=request_peer_info['port']
    print(f"\n[NEW CONNECTION] {request_peer_ip} connected.") # 1/ establish connection to [request_peer_ip]

    # 2/ send "Peer[this_peer_ip,this_peer_port] established connection to Peer[request_peer_ip,request_peer_port]" (string msg) to [request_peer_ip]
    conn.send(bencode(f"Peer[{this_peer_ip},{this_peer_port}] established connection to Peer[{request_peer_ip},{request_peer_port}]").encode(FORMAT)) # send to peer
    # 3/ connected_peers[requested_peer_IP]=True
    connected_peers[f"{request_peer_ip} {request_peer_port}"]=True

    # 4/ Start a while-loop thread to listen to [requested_peer_ip,request_peer_port]
    while connected_peers[f"{request_peer_ip} {request_peer_port}"]:
        received_msg = conn.recv(HEADER).decode(FORMAT)
        if received_msg:
            msg = bdecode(received_msg)
            print(f"Sender[{request_peer_ip},{request_peer_port}] {msg}")

            msg_parts=msg.split()
            match msg_parts[0]:
                case "/disconnect_peer":# [target_peer_IP] [target_peer_port] # done
                    # 1/ check if input is valid
                    if (len(msg_parts)!=3):
                        print("Invalid format! Please provide both request peer IP and port.")
                        return
                    if(not msg_parts[1] or not msg_parts[2]):
                        print("Invalid format! Please provide both request peer IP and port.")
                    else:
                        print(f"[REQUEST PEER DISCONNECTED THIS PEER] {msg_parts[1]}")
                        # 2/ send "Peer[this_peer_id,this_peer_port] disconnected from Peer[target_peer_ip,target_peer_port]"
                        conn.send(bencode(f"Peer[{this_peer_ip},{this_peer_port}] disconnected from Peer[{msg_parts[1]},{msg_parts[2]}]").encode(FORMAT))  # send to peer
                        connected_peers[f"{request_peer_ip} {request_peer_port}"] = False # 3/
                case _:
                    conn.send(bencode("Invalid command").encode(FORMAT))
    conn.close()

###########################################END##################################################
#                                   PEER LISTENING FUNCTIONS                                   #
###########################################END##################################################

###########################################START################################################
#                                       PEER INIT FUNCTION                                     #
###########################################START################################################

def peer_init():
    global TRACKER_IP, TRACKER_PORT, CHUNK_SIZE, TORRENT_STRUCTURE
    TRACKER_IP, TRACKER_PORT, CHUNK_SIZE = read_torrent_file_part1()
    TORRENT_STRUCTURE = read_torrent_file_part2()  # Move this line here
    this_peer_info["chunk_status"] = update_chunk_status()
    see_chunk_status()

###########################################END##################################################
#                                       PEER INIT FUNCTION                                     #
###########################################END##################################################

###########################################START################################################
#                                       OTHER FUNCTIONS                                        #
###########################################START################################################

def read_torrent_file_part1():
    global TRACKER_ADDR
    torrent_file=TORRENT_FILE
    memory_dir=MEMORY_DIR
    # Construct the full path to the torrent file
    torrent_file_path = os.path.join(memory_dir, torrent_file)

    # Read the first three lines of the torrent file
    with open(torrent_file_path, 'r') as file:
        lines = file.readlines()[:3]

        # Extract tracker_ip, tracker_port, and chunk_size
        tracker_ip = lines[0].strip()
        tracker_port = int(lines[1].strip())
        chunk_size = int(lines[2].strip())
    TRACKER_ADDR=(tracker_ip,tracker_port)
    # Return the extracted values
    return tracker_ip, tracker_port, chunk_size

def read_torrent_file_part2():
    torrent_file=TORRENT_FILE
    memory_dir=MEMORY_DIR
    # Construct the full path to the torrent file
    torrent_file_path = os.path.join(memory_dir, torrent_file)

    # Read the JSON data from the torrent file starting from line 4
    with open(torrent_file_path, 'r') as file:
        # Skip the first three lines
        for _ in range(3):
            next(file)
        # Load the JSON data
        torrent_structure = json.load(file)

    # Return the torrent structure dictionary
    return torrent_structure

def init_chunk_status():
    torrent_structure=TORRENT_STRUCTURE
    chunk_status={}
    for file_name in torrent_structure:
        for chunk_name in torrent_structure[file_name]:
            chunk_status[chunk_name]=0
    return chunk_status

def update_chunk_status():
    memory_dir=MEMORY_DIR
    chunk_status=init_chunk_status()
    for filename in os.listdir(memory_dir):
        filepath = os.path.join(memory_dir, filename)
        if os.path.isfile(filepath) and filename in chunk_status:  # 512kb in bytes
            chunk_status[filename]=1
    return chunk_status

def print_dict(dictionary):
    for key in dictionary:
        print(f"{key}: {dictionary[key]}")

###########################################END##################################################
#                                       OTHER FUNCTIONS                                        #
###########################################END##################################################