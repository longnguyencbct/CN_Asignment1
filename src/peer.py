import socket
from bencode import bencode,bdecode

HEADER = 1024
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "/quit"
SERVER = "192.168.1.181"
CLIENT = socket.gethostbyname(socket.gethostname())
SERVER_ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(SERVER_ADDR)

def send(msg):
    message = bencode(msg).encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
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


class Peer:
    def __init__(self,peer_info={
        "peer_id":"",
        "ip":socket.gethostbyname(socket.gethostname()),
        "port":PORT,
        "downloaded":0,
        "uploaded":0
    },peer_data=None,seeder_lst=[],leecher_lst=[]):
        self.peer_info=peer_info
        self.peer_data=peer_data
        self.seeder_lst=seeder_lst
        self.leacher_lst=leecher_lst
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


if __name__ == "__main__":
    connected = True
    this_peer=Peer()
    send(this_peer.peer_info)
    while connected:
        print(f"[{CLIENT},{PORT}] ",end='')  # Display client's IP address and port
        connected = send(input())