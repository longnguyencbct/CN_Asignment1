import os
import socket
from bencode import bencode,bdecode
#from split_file import *

###########################################START################################################
#                                   PEER'S GLOBAL VARIABLES                                    #
###########################################START################################################

# Constants
HEADER = 1024
FORMAT = 'utf-8'
PORT=7000
TRACKER_IP = "192.168.1.181" # get from torrent file
SERVER_ADDR = (TRACKER_IP, PORT)

# Variables
running=True
tracker_connected=False


Peer_set=[]

missing_chunks = []
curr_chunks=[]

this_peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

this_peer_info={
    # "peer_id": peer_id,
    "ip": socket.gethostbyname(socket.gethostname()),
    "port": PORT,
    "downloaded": 0,
    "uploaded": 0
}

this_peer_data={}
chunk_directory="Memory"

###########################################END##################################################
#                                   PEER'S GLOBAL VARIABLES                                    #
###########################################END##################################################


###########################################START################################################
#                                   PEER COMMAND FUNCTIONS                                     #
###########################################START################################################

# peer-tracker communication cmds: 

def connect_tracker(): # done
    global tracker_connected
    this_peer_socket.connect(SERVER_ADDR)                           # 1/ establish connection to tracker
    this_peer_socket.send(bencode(this_peer_info).encode(FORMAT))                  # 2/ send bencoded peer_info to tracker
    received_msg = this_peer_socket.recv(2048).decode(FORMAT)       # 3/ tracker response "Tracker established connection to Peer[peer_ip]"
    print(received_msg)
    tracker_connected = True                                        # 4/ tracker_connected = True 
    get_peer_set()                                                  # 5/ run /get_peer_set

def get_peer_set(): # done
    global Peer_set
    if not check_tracker_connected():                               # 1/ run /check_tracker_connected. Go to step 2/ if returned True
        return
    this_peer_socket.send(bencode("/get_peer_set").encode(FORMAT))                 # 2/ send "/get_peer_set" (string msg) to tracker.
    received_msg = this_peer_socket.recv(2048).decode(FORMAT)       # 3/ tracker response bencoded tracker's PEER_SET (string)
    Peer_set=bdecode(received_msg)                                  # 4/ bdecode tracker response (list if dictionaries [{},{},{}] ) and update peer's PEER_SET

def update_status_to_tracker():
    pass

def disconnect_tracker(): # done
    global tracker_connected
    if not check_tracker_connected():                               # 1/ run /check_tracker_connected. Go to step 2/ if returned True
        return
    this_peer_socket.send(bencode("/disconnect_tracker"))           # 2/ send bencoded "/disconnect_tracker" (string msg) to tracker 
    received_msg = this_peer_socket.recv(2048).decode(FORMAT)       # 3/ tracker response "Peer[peer_id] disconnected from tracker"
    print(received_msg)
    this_peer_socket.close()
    tracker_connected = False                                       # 4/ tracker_connected = False

def quit_torrent(): # done
    global running
    if not check_tracker_connected():                               # 1/ run /check_tracker_connected. Run /connect_tracker then Go to step 2/ if returned False
        connect_tracker()
    this_peer_socket.send(bencode("/quit_torrent").encode(FORMAT))                 # 2/ send bencoded "/quit_torrent" (string msg) to tracker 
    received_msg = this_peer_socket.recv(2048).decode(FORMAT)       # 3/ tracker response "Peer[peer_id] quited torrent"
    print(received_msg)
    running=False                                                   # 4/ leave the torrent and won't upload/ download chunks (peer.py program stops running)
    pass


# peer-peer communication request cmds:

def connect_peer(target_peer_IP):
    pass

def request_download(target_peer_IP,missing_chunk):
    pass

def upload(request_peer_ip,chunk_name):
    pass

def disconnect_peer(target_peer_IP):
    pass


# peer functionality cmds:

def check_tracker_connected():
    if not tracker_connected:
        print("Peer is not connected to tracker")
    return tracker_connected

def check_target_peer_connected(target_peer_IP):
    pass

def check_chunk(chunk_name):
    pass

def see_peer_set(): # done
    print(Peer_set) # 1/ print Peer_set

def see_connected():
    pass

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
#                                       OTHER FUNCTIONS                                        #
###########################################START################################################

def save_chunk(chunk_number, chunk_data):
    this_peer_data[chunk_number] = chunk_data

def get_chunk(chunk_number):
    return this_peer_data.get(chunk_number, None)

def set_chunk_directory(chunk_directory):
    chunk_directory = chunk_directory

def send(msg,target_ip):
    message = bencode(msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    this_peer_socket.send(send_length)
    this_peer_socket.send(message)

    # chunk_dir_length = len(chunk_directory)
    # peer_socket.send(str(chunk_dir_length).encode(FORMAT))
    # peer_socket.send(chunk_directory.encode(FORMAT))


    received_msg = this_peer_socket.recv(2048).decode(FORMAT)
    print(received_msg)
    print(type(received_msg))
    if received_msg == "Disconnected":
        return False
    #################################################
    # RECEIVE PEER SET HANDLER
    # TODO
    #################################################
    return True

def save_chunks_to_peer(chunk_directory): # check file in [chunk_directory], then split file into chunks and save them to [chunk_directory]
    saved_chunks = 0  # Initialize counter for saved chunks
    for filename in os.listdir(chunk_directory):
        if filename.startswith('File_split.mp4.part'):  # Check if the file is a chunk
            chunk_number = int(filename.split('part')[1])  # Extract chunk number from filename
            file_path = os.path.join(chunk_directory, filename)
            with open(file_path, 'rb') as f:
                chunk_data = f.read()  # Read chunk data
                save_chunk(chunk_number, chunk_data)  # Save chunk to peer_data
                saved_chunks += 1  # Increment the counter for saved chunks
    if saved_chunks == 70:
        print("All 70 chunks have been successfully saved.")

###########################################END##################################################
#                                       OTHER FUNCTIONS                                        #
###########################################END##################################################

