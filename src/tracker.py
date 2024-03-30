from time import sleep
import threading
from request_response_struct import request_struct,response_struct

class Tracker:
    def __init__(self, currTorrent=response_struct(), request_queue=[]):
        self.currTorrent = currTorrent
        self.request_queue = request_queue
        self.running = True
        self.display_requests = False  # Flag to control display of requests

    def request_sniffing(self):
        temp = 0
        while self.running:
            sleep(1)
            #####################################################################
            new_request = request_struct(f"Sample magnet link {temp}")
            # GET NEW REQUEST HERE
            # TODO
            # READ FROM CLIENT "request_struck" object
            #####################################################################
            self.request_queue.append(new_request)
            if self.display_requests:  # Check if display flag is set
                print("Added request to queue:", new_request.magnet_text)
            temp += 1

    def tracker_response(self):
        while self.running:
            while len(self.request_queue) != 0:
                head_request = self.request_queue.pop(0)
                #################################################################
                # RESPOND REQUEST HERE
                # TODO
                # ANALYZE HEAD REQUEST
                # SEND BACK CLIENT A "response_struct" OBJECT
                #################################################################
                if self.display_requests:  # Check if display flag is set
                    print("Responding request:", head_request.magnet_text)
                    peer_set_id=[]
                    for i in self.currTorrent.peer_set:
                        peer_set_id.append(i["peer_id"])
                    print("Current Peer Set ID:", peer_set_id)
            sleep(5)

    def handle_user_input(self):
        while True:
            command = input("Type '/quit' to terminate the program, '/display' to toggle display: ")
            if command.strip() == "/quit":
                self.running = False  # Set the running flag to False to terminate the threads
                break  # Break out of the loop to exit the program
            elif command.strip() == "/display":
                self.display_requests = not self.display_requests  # Toggle the display flag
    def UpdateTorrent(self):
        while self.running:
            print("################\nUpdated Peer Set\n################")
            self.currTorrent.update_peer_set()
            sleep(20)
    def tracker_main(self):
        update_Torrent_thread= threading.Thread(target=self.UpdateTorrent)
        request_sniffing_thread = threading.Thread(target=self.request_sniffing)
        tracker_response_thread = threading.Thread(target=self.tracker_response)
        user_input_thread = threading.Thread(target=self.handle_user_input)

        update_Torrent_thread.start()
        request_sniffing_thread.start()
        tracker_response_thread.start()
        user_input_thread.start()

        # Wait for threads to finish (which they never will in this example because of the infinite loops)
        update_Torrent_thread.join()
        request_sniffing_thread.join()
        tracker_response_thread.join()
        user_input_thread.join()

if __name__ == "__main__":
    t = Tracker()
    t.tracker_main()
