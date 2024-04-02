import requests
from bencode import bencode,bdecode
class Peer_Info:
    def __init__(self,peer_id="",ip="",port=9999):
        self.peer_id=peer_id
        self.ip=ip
        self.port=port
        self.downloaded=0
        self.uploaded=0
    def Bencode(self):
        return bencode({
            "peer_id":self.peer_id,
            "ip":self.ip,
            "port":self.port,
            "downloaded":self.downloaded,
            "uploaded":self.uploaded
        })
class Peer:
    def __init__(self,peer_info=Peer_Info(),peer_data=None,seeder_lst=[],leecher_lst=[]):
        self.peer_info=peer_info
        self.peer_data=peer_data
        self.seeder_lst=seeder_lst
        self.leacher_lst=leecher_lst
    def request_tracker(self):
        # request tracker to get seeder_lst
        pass
    def request_download(self, tracker_url):
        # request seeders in seeder_lst to download piece

        # Prepare the request data
        request_data = {
            "peer_id": self.peer_info.peer_id,
            "ip": self.peer_info.ip,
            "port": self.peer_info.port,
            "downloaded": self.peer_info.downloaded,
            "uploaded": self.peer_info.uploaded
        }

        # Send POST request to tracker with the request data
        response = requests.post(tracker_url, json=request_data)

        # Handle response
        if response.status_code == 200:
            print("Request sent successfully to tracker.")
        else:
            print("Failed to send request to tracker.")
        # pass
    def upload_response(self):
        # upload file to leachers in leecher_lst
        pass


# Example usage
# if __name__ == "__main__":
#     # Creating Peer_Info object
#     peer_info = Peer_Info(peer_id="peer123", ip="127.0.0.1", port=12345, downloaded=100, uploaded=50)
#
#     # Creating Peer object
#     peer = Peer(peer_info=peer_info)
#
#     # Tracker URL
#     tracker_url = "http://tracker_address:port"  # Replace with your tracker URL
#
#     # Sending request to tracker
#     peer.request_download(tracker_url)


