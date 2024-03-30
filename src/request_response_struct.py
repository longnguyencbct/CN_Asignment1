from peer import Peer_Info
from random import randint
from bencode import bencode,bdecode

class request_struct:
    def __init__(self, magnet_text, request_state="STARTED", bytes_downloaded=0):
        self.magnet_text = magnet_text
        self.request_state = request_state
        self.bytes_downloaded = bytes_downloaded

class response_struct:
    def __init__(self, tracker_id=9999,
                 peer_set=[]):
        self.tracker_id = tracker_id
        self.peer_set = peer_set

    def GetPeers(self):
        Peer_Lst=[]
        ###################################
        # GET CURRENT STATE OF TORRENT
        #   get list of all active peers
        #   get total ammount of downloaded/uploaded data for each peer
        # TODO
        # Dummy implementation to show how it should work
        ###########FOR TESTING ONLY##########
        for i in range(5):
            Peer_Lst.append(bdecode(Peer_Info(peer_id=randint(1000,9999)).Bencode()))
        #####################################
        return Peer_Lst

    def update_peer_set(self):
        self.peer_set.clear()
        self.peer_set=self.GetPeers()
    

    
        
