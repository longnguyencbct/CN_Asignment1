import os
import socket
from bencode import bencode,bdecode
#from split_file import *
HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "/quit"
SERVER = "127.0.1.1"
CLIENT = socket.gethostbyname(socket.gethostname())
SERVER_ADDR = (SERVER, PORT)
missing_pieces = []
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(SERVER_ADDR)

def send(msg):
    message = bencode(msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    chunk_dir_length = len(chunk_directory)
    client.send(str(chunk_dir_length).encode(FORMAT))
    client.send(chunk_directory.encode(FORMAT))


    received_msg = client.recv(2048).decode(FORMAT)
    print(received_msg)
    print(type(received_msg))
    if received_msg == "Disconnected":
        return False
    #################################################
    # RECEIVE PEER SET HANDLER
    # TODO
    #################################################
    return True


# class Peer:
#     def __init__(self,peer_info={
#         "peer_id":"",
#         "ip":socket.gethostbyname(socket.gethostname()),
#         "port":PORT,
#         "downloaded":0,
#         "uploaded":0,
#     },
#         peer_data=None,seeder_lst=[],leecher_lst=[]):
#         self.peer_info=peer_info
#         self.peer_data = peer_data if peer_data is not None else {}
#         self.seeder_lst=seeder_lst
#         self.leacher_lst=leecher_lst
#     def save_chunk(self, chunk_number, chunk_data):
#         self.peer_data[chunk_number] = chunk_data
#     def get_chunk(self, chunk_number):
#         return self.peer_data.get(chunk_number, None)
class Peer:
    def __init__(self, peer_id="", ip=socket.gethostbyname(socket.gethostname()), port=PORT,
                 downloaded=0, uploaded=0, chunk_directory=""):
        self.peer_info = {
            "peer_id": peer_id,
            "ip": ip,
            "port": port,
            "downloaded": downloaded,
            "uploaded": uploaded
        }
        self.peer_data = {}
        self.seeder_lst = []
        self.leacher_lst = []
        self.chunk_directory = chunk_directory

    def save_chunk(self, chunk_number, chunk_data):
        self.peer_data[chunk_number] = chunk_data

    def get_chunk(self, chunk_number):
        return self.peer_data.get(chunk_number, None)

    def set_chunk_directory(self, chunk_directory):
        self.chunk_directory = chunk_directory

    # Other methods...

    # def request_tracker(self):
    #     # request tracker to get seeder_lst
    #     pass
    # def request_download(self, tracker_url):
    #     # request seeders in seeder_lst to download piece

    #     # Prepare the request data
    #     request_data = self.peer_info

    #     # Send POST request to tracker with the request data
    #     response = requests.post(tracker_url, json=request_data)

    #     # Handle response
    #     if response.status_code == 200:
    #         print("Request sent successfully to tracker.")
    #     else:
    #         print("Failed to send request to tracker.")
    #     # pass
    # def upload_response(self):
    #     # upload file to leachers in leecher_lst
    #     pass
def save_chunks_to_peer(peer, chunk_directory):
    saved_chunks = 0  # Initialize counter for saved chunks
    for filename in os.listdir(chunk_directory):
        if filename.startswith('File_split.mp4.part'):  # Check if the file is a chunk
            chunk_number = int(filename.split('part')[1])  # Extract chunk number from filename
            file_path = os.path.join(chunk_directory, filename)
            with open(file_path, 'rb') as f:
                chunk_data = f.read()  # Read chunk data
                peer.save_chunk(chunk_number, chunk_data)  # Save chunk to peer_data
                saved_chunks += 1  # Increment the counter for saved chunks
    if saved_chunks == 70:
        print("All 70 chunks have been successfully saved.")



if __name__ == "__main__":
    connected = True
    chunk_directory = 'Memory'
    this_peer = Peer(chunk_directory=chunk_directory)
    save_chunks_to_peer(this_peer, chunk_directory)

    send(this_peer.peer_info)
    while connected:
        print(f"[{CLIENT},{PORT}] ",end='')
        connected = send(input())

#
#
#
