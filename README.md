
# CN_Asignment1

**PEER CMDS: (peer.py)**  
- peer-tracker communication cmds:  
&emsp;&emsp;&emsp;/connect_tracker:   
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1/ Peer todo: establish connection to tracker  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;2/ Tracker response: "Tracker established connection to Peer[peer_ip]" (tracker runs a "listening peer cmds" while-loop thread)   
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;3/ Peer todo: tracker_connected = True  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;4/ run /get_peer_set  
&emsp;&emsp;&emsp;/get_peer_set:  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1/ run /check_tracker_connected. Go to step 2/ if returned True  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;2/ Peer todo: send "/get_peer_set" (string msg) to tracker.  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;3/ Tracker response: bencoded tracker's PEER_SET (string)  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;4/ Peer todo: bdecode tracker response (list if dictionaries [{},{},{}] ) and update peer's PEER_SET  
&emsp;&emsp;&emsp;/update_status_to_tracker:  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1/ run /check_tracker_connected. Go to step 2/ if returned True  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;2/ Peer todo: send "/update_status_to_tracker" [bencoded Peer_info] (string msg) to tracker  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;3/ Peer todo: send "[bencoded Peer_info]" (string msg) to tracker  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;4/ Tracker response: "Tracker updated Peer[peer_ip] status" (tracker updates peer set in tracker, but  other peers' PEER_SET will not update unless /get_peer_set is run)  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;5/ run /get_peer_set  
&emsp;&emsp;&emsp;/disconnect_tracker:  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1/ run /check_tracker_connected. Go to step 2/ if returned True  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;2/ Peer todo: send "/disconnect_tracker" (string msg) to tracker   
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;3/ Tracker response: "Peer[peer_id] disconnected from tracker"  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;4/ Peer todo: disconnect from tracker but can still upload/download chunks to/from peers (tracker_connected = False, tracker stops "listening peer cmds" thread)  
&emsp;&emsp;&emsp;/quit_torrent:  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1/ run /check_tracker_connected. Run /connect_tracker then Go to step 2/ if returned False  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;2/ Peer todo: send "/quit_torrent" (string msg) to tracker  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;3/ Tracker response: "Peer[peer_id] quited torrent"  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;4/ Peer todo: leave the torrent and won't upload/ download chunks (peer.py program stops running)  
- peer-peer communication cmds:  
&emsp;&emsp;&emsp;/connect_peer [target_peer_IP]:  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1/ establish connection to target peer  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;2/ Target peer response: "Target Peer[target_peer_IP] established connection to This Peer" (target peer runs a "listening peer cmds" while-loop thread)  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;3/ This peer todo: connected_peers={"[target_peer_IP1]":True|False, "[target_peer_IP2]":True|False,...} (only peer ip from PEER_SET)  
&emsp;&emsp;&emsp;/request_download [target_peer_IP] [missing_chunks[i]]:  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1/ run /check_target_peer_connected [target_peer_IP]. Go to step 2/ if returned True   
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;2/ This peer todo: send "/request_download" (string msg) to [target_peer_IP].  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;3/ This peer todo: send "[missing_chunks[i]]" (string msg) to [target_peer_IP]. ([missing_chunks[i]] is name of the chunk file)  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;4/ Target peer response: "Target Peer[target_peer_IP] starts uploading chunk [missing_chunks[i]] to This peer"   
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;5/ This peer todo: Save new chunk to Memory_peer folder  
&emsp;&emsp;&emsp;/upload_chunk [target_peer_IP][curr_chunks[i]]:  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1/ run /check_target_peer_connected [target_peer_IP]. Go to step 2/ if returned True  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;2/ This peer todo: send "/request_download" (string msg) to [target_peer_IP]. 
&emsp;&emsp;&emsp;/disconnect_peer [target_peer_IP]:  
- peer functionality cmds:  
&emsp;&emsp;&emsp;/check_tracker_connected:  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1/ check if tracker_connected==??:  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;+ True:	Return True  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;+ False: Peer todo: print "Peer is not connected to tracker". Return False  
&emsp;&emsp;&emsp;/check_target_peer_connected [target_peer_IP] :  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;1/ check if connected_peers[target_peer_IP]==??:  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;+ True:	Return True  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;+ False: Peer todo: print "This peer is not connected to Peer[target_peer_IP]". Return False  
&emsp;&emsp;&emsp;/see_peer_set  
&emsp;&emsp;&emsp;/see_connected_seeders  
&emsp;&emsp;&emsp;/see_connected_leechers  
&emsp;&emsp;&emsp;/see_current_chunks  
&emsp;&emsp;&emsp;/merge_chunks  
**TRACKER FUNCTIONALITY: (tracker.py)**
