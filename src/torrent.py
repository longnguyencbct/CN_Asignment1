from bencode import bencode,bdecode
class TorrentFile:
    def __init__(self,
                 announce="",
                 create_by="",
                 creation_date="",
                 encoding="",
                 comment="",
                 info = {   "name":"",
                            "files":[
                             {"length":1*1024*1024, # in byte 1MB length: 1024*1024
                              "mdssum":0, # 
                              "path":[""]},
                              {"length":512*1024,
                              "mdssum":0,
                              "path":[""]},
                              {"length":2*1024*1024,
                              "mdssum":0,
                              "path":[""]}],
                            "piece_length":512*1024, 
                            "pieces":7
                        }
                ):
        self.announce = announce
        self.create_by = create_by
        self.creation_date = creation_date
        self.encoding = encoding
        self.comment = comment
        self.info = info




# a=10
# b="hello"
# c=[1,"hello",3]
# d={"a":1,"b":2}

# bencoded_a=bencode(a)
# bencoded_b=bencode(b)
# bencoded_c=bencode(c)
# bencoded_d=bencode(d)
# print(bencoded_a)
# print(bencoded_b)
# print(bencoded_c)
# print(bencoded_d)
# decoded_bencoded_a=bdecode(bencoded_a)
# decoded_bencoded_b=bdecode(bencoded_b)
# decoded_bencoded_c=bdecode(bencoded_c)
# decoded_bencoded_d=bdecode(bencoded_d)



# print((decoded_bencoded_a))
# print((decoded_bencoded_b))
# print((decoded_bencoded_c))
# print((decoded_bencoded_d))

# print(a==(decoded_bencoded_a))
# print(b==(decoded_bencoded_b))
# print(c==(decoded_bencoded_c))
# print(d==(decoded_bencoded_d))