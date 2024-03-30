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
    def request_download(self):
        # request seeders in seeder_lst to download piece
        pass
    def upload_response(self):
        # upload file to leachers in leecher_lst
        pass

    