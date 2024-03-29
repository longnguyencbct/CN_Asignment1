
class response_struct:
    def __init__(self,tracker_id=9999,
                 peer_set=[
                        {
                            "peer_id":1234,     # peer's self-selected ID
                            "ip":"DNS...",      # peer's IP address (DNS name)
                            "port":5678         # peer's port number
                        },
                        {
                            "peer_id":9341,     
                            "ip":"DNS...",      
                            "port":8269         
                        }
                     ]):
        self.tracker_id=tracker_id
        self.peer_set=peer_set
    def update_peer_set(self):
        pass

class request_struct:
    def __init__(self,magnet_text,request_state="STARTED",bytes_downloaded=0):
        self.magnet_text=magnet_text
        self.request_state=request_state
        self.bytes_downloaded=bytes_downloaded

class Tracker:
    def __init__(self,currTorrent=response_struct(),request_queue=[]):
        self.currTorrent=currTorrent
        self.request_queue=request_queue
        pass
    def request_sniffing(self): # a loop that checks incomming requests from clients to add them to request queue
        pass
    def tracker_response(self): # a loop that keeps poping the request queue to respond back to them
        pass