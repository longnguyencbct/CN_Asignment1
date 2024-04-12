from peer_helper import *
running=True
tracker_connected=False
connected_peers={}

def command_handler(user_input):
    global running, tracker_connected, connected_peers
    user_input_parts=[]

    match user_input_parts[0]:

        # peer-tracker communication cmds: 
        case "/connect_tracker":
            connect_tracker()
        case "/get_peer_set":
            get_peer_set()
        case "/update_status_to_tracker":
            update_status_to_tracker()
        case "/disconnect_tracker":
            disconnect_tracker()
        case "/quit_torrent":
            quit_torrent()

        # peer-peer communication request cmds:
        case "/connect_peer":# [target_peer_IP]
            connect_peer(user_input_parts[1])
        case "/request_download":# [target_peer_IP] [missing_chunk]
            request_download(user_input_parts[1],user_input_parts[2])
        case "/upload":# [request_peer_ip] [chunk_name]
            upload(user_input_parts[1],user_input_parts[2])
        case "/disconnect_peer":# [target_peer_IP]
            disconnect_peer(user_input_parts[1])
        
        # peer functionality cmds:
        case "/check_tracker_connected":
            check_tracker_connected()
        case "/check_target_peer_connected":# [target_peer_IP]
            check_target_peer_connected(user_input_parts[1])
        case "/check_chunk":# [chunk_name]
            check_chunk(user_input_parts[1])
        case "/see_peer_set":
            see_peer_set()
        case "/see_connected":
            see_connected()
        case "/see_current_chunks":
            see_current_chunks()
        case "/see_missing_chunks":
            see_missing_chunks()
        case "/merge_chunks":
            merge_chunks()
        case _:
            pass


if __name__ == "__main__":
    chunk_directory = 'Memory'
    save_chunks_to_peer(chunk_directory) # check file in [chunk_directory], then split file into chunks and save them to [chunk_directory]

    # send(this_peer_info)
    while running:
        print(f"[{this_peer_info["ip"]},{this_peer_info["port"]}] ",end='')
        user_input = input()
        command_handler(user_input)

