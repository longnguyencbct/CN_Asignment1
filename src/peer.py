from peer_helper import *
connected_peers={}

def command_handler(user_input):
    global running, tracker_connected, connected_peers
    user_input_parts=user_input.split()

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
        case "/connect_peer":# [target_peer_IP] [target_peer_port]
            if (len(user_input_parts)!=3):
                print("Invalid format! Please provide both request peer IP and port.")
                return
            if(not user_input_parts[1] or not user_input_parts[2]):
                print("Invalid format! Please provide both target peer IP and port.")
            else:
                connect_peer(user_input_parts[1],user_input_parts[2])
        case "/request_download":# [target_peer_IP] [target_peer_port] [missing_chunk]
            if (len(user_input_parts)!=4):
                print("Invalid format! Please provide both request peer IP and port.")
                return
            if(not user_input_parts[1] or not user_input_parts[2] or not user_input_parts[3]):
                print("Invalid format! Please provide both target peer IP and port.")
            else:
                request_download(user_input_parts[1],user_input_parts[2],user_input_parts[3])
        case "/upload":# [request_peer_ip] [chunk_name]
            if (len(user_input_parts)!=3):
                print("Invalid format! Please provide both request peer IP and port.")
                return
            if(not user_input_parts[1] or not user_input_parts[2]):
                print("Invalid format! Please provide both target peer IP and port.")
            else:
                upload(user_input_parts[1],user_input_parts[2])
        case "/disconnect_peer":# [target_peer_IP] [target_peer_port]
            if (len(user_input_parts)!=3):
                print("Invalid format! Please provide both request peer IP and port.")
                return
            if(not user_input_parts[1] or not user_input_parts[2]):
                print("Invalid format! Please provide both target peer IP and port.")
            else:
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

def command_thread():
    while running:
        peer_ip=this_peer_info["ip"]
        peer_port=this_peer_info["port"]
        print(f"[{peer_ip},{peer_port}] ",end='')
        user_input = input()
        command_handler(user_input)


if __name__ == "__main__":
    command_thrd = threading.Thread(target=command_thread)
    command_thrd.start()
    this_peer.listen()
    while True:
        conn,this_peer_ip = this_peer.accept() # detect a target peer connect
        thread = threading.Thread(target=handle_request_peer_connection,args=(conn,this_peer_ip)) # create a "listening peer" thread
        thread.start()
        print(f"this_peer_ip??:{this_peer_ip}") # temp
        print(f"[ACTIVE CONNECTION] {threading.active_count()-1}")

