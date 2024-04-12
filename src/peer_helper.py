import os
import socket
from bencode import bencode,bdecode
#from split_file import *

#from split_file import *
HEADER = 1024
FORMAT = 'utf-8'
PORT=5050

TRACKER_IP = "127.0.1.1" # get from torrent file
SERVER_ADDR = (TRACKER_IP, PORT)

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





# peer-tracker communication cmds: 

def connect_tracker():
    pass

def get_peer_set():
    pass

def update_status_to_tracker():
    pass

def disconnect_tracker():
    pass

def quit_torrent():
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
    pass

def check_target_peer_connected(target_peer_IP):
    pass

def check_chunk(chunk_name):
    pass

def see_peer_set():
    pass

def see_connected():
    pass

def see_current_chunks():
    pass

def see_missing_chunks():
    pass

def merge_chunks():
    pass