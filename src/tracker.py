from time import sleep
import threading

class response_struct:
    def __init__(self, tracker_id=9999,
                 peer_set=[
                     {
                         "peer_id": 1234,     # peer's self-selected ID
                         "ip": "DNS...",      # peer's IP address (DNS name)
                         "port": 5678         # peer's port number
                     },
                     {
                         "peer_id": 9341,
                         "ip": "DNS...",
                         "port": 8269
                     }
                 ]):
        self.tracker_id = tracker_id
        self.peer_set = peer_set

    def update_peer_set(self):
        pass

class request_struct:
    def __init__(self, magnet_text, request_state="STARTED", bytes_downloaded=0):
        self.magnet_text = magnet_text
        self.request_state = request_state
        self.bytes_downloaded = bytes_downloaded

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
            new_request = request_struct(f"Sample magnet link {temp}")
            self.request_queue.append(new_request)
            if self.display_requests:  # Check if display flag is set
                print("Added request to queue:", new_request.magnet_text)
            temp += 1

    def tracker_response(self):
        while self.running:
            while len(self.request_queue) != 0:
                head_request = self.request_queue.pop(0)
                if self.display_requests:  # Check if display flag is set
                    print("Responding request:", head_request.magnet_text)
            sleep(5)

    def handle_user_input(self):
        while True:
            command = input("Type '/quit' to terminate the program, '/display' to toggle display: ")
            if command.strip() == "/quit":
                self.running = False  # Set the running flag to False to terminate the threads
                break  # Break out of the loop to exit the program
            elif command.strip() == "/display":
                self.display_requests = not self.display_requests  # Toggle the display flag

    def tracker_main(self):
        request_sniffing_thread = threading.Thread(target=self.request_sniffing)
        tracker_response_thread = threading.Thread(target=self.tracker_response)
        user_input_thread = threading.Thread(target=self.handle_user_input)

        request_sniffing_thread.start()
        tracker_response_thread.start()
        user_input_thread.start()

        # Wait for threads to finish (which they never will in this example because of the infinite loops)
        request_sniffing_thread.join()
        tracker_response_thread.join()
        user_input_thread.join()

if __name__ == "__main__":
    t = Tracker()
    t.tracker_main()
