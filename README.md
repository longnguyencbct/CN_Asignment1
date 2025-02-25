# P2P File Sharing Application

This project is a peer-to-peer (P2P) file-sharing application implemented in Python. It allows multiple peers to share and download file chunks, coordinated by a central tracker.

## Documentation

For detailed project documentation, please refer to the [project documentation](documentation/ASS1_P1_2153535-2153395-2153380.pdf) in the `documentation` folder.

## Project Structure

The project directory contains the following files and directories:

- `Assignment 1-Network Application P2P File Sharing.pdf`: Project assignment document.
- `plan_btl1.txt`: Detailed plan and command descriptions for the P2P file-sharing application.
- `README.md`: Project documentation.
- `src/`: Source code directory containing the implementation of the P2P file-sharing application.
  - `bencode.py`: Implementation of bencoding and bdecoding functions.
  - `Memory/`: Directory containing file chunks for the first peer.
  - `Memory2/`: Directory containing file chunks for the second peer.
  - `Memory3/`: Directory containing file chunks for the third peer.
  - `peer_helper.py`: Helper functions for the first peer.
  - `peer_helper2.py`: Helper functions for the second peer.
  - `peer_helper3.py`: Helper functions for the third peer.
  - `peer.py`: Main script for the first peer.
  - `peer2.py`: Main script for the second peer.
  - `peer3.py`: Main script for the third peer.
  - `split_file.py`: Script for splitting files into chunks.
  - `tracker.py`: Implementation of the tracker that coordinates the peers.

## Components

### Tracker

The tracker is implemented in [`tracker.py`](src/tracker.py). It listens for connections from peers, maintains a list of connected peers (`PEER_SET`), and responds to various commands from peers.

### Peers

Each peer is represented by a Python script and corresponding helper files:
- [`peer.py`](src/peer.py) and [`peer_helper.py`](src/peer_helper.py)
- [`peer2.py`](src/peer2.py) and [`peer_helper2.py`](src/peer_helper2.py)
- [`peer3.py`](src/peer3.py) and [`peer_helper3.py`](src/peer_helper3.py)

Peers can connect to the tracker, request and download file chunks from other peers, and upload file chunks to other peers.

### File Handling

Files are split into chunks for sharing, as seen in [`split_file.py`](src/split_file.py). The `Memory`, `Memory2`, and `Memory3` directories contain the file chunks for different peers. The `torrent_file` in each `Memory` directory describes the structure of the files being shared.

### Bencoding

The project uses bencoding for encoding and decoding messages between peers and the tracker, implemented in [`bencode.py`](src/bencode.py).

## Commands and Functionality

### Peer-Tracker Communication Commands

- `/connect_tracker`: Establish connection to the tracker.
- `/get_peer_set`: Retrieve the list of connected peers from the tracker.
- `/update_status_to_tracker`: Update the peer's status to the tracker.
- `/disconnect_tracker`: Disconnect from the tracker.
- `/quit_torrent`: Quit the torrent and stop the peer.

### Peer-Peer Communication Commands

- `/connect_peer [target_peer_IP] [target_peer_port]`: Connect to another peer.
- `/ping [target_peer_IP] [target_peer_port]`: Ping another peer.
- `/request_download [target_peer_IP] [target_peer_port] [missing_chunk]`: Request a file chunk from another peer.
- `/disconnect_peer [target_peer_IP] [target_peer_port]`: Disconnect from another peer.

### Peer Functionality Commands

- `/check_tracker_connected`: Check if the peer is connected to the tracker.
- `/check_target_peer_connected [target_peer_IP] [target_peer_port]`: Check if the peer is connected to another peer.
- `/see_this_peer_info`: Display the current peer's information.
- `/see_peer_set`: Display the list of connected peers.
- `/see_connected`: Display the list of currently connected peers.
- `/see_torrent_struct`: Display the structure of the torrent.
- `/see_chunk_status`: Display the status of file chunks.
- `/merge_chunks [file_name]`: Merge file chunks into a complete file.
- `/merge_all`: Merge all file chunks into complete files.

## Running the Application

1. Start the tracker:
    ```sh
    python src/tracker.py
    ```

2. Start the peers:
    ```sh
    python src/peer.py
    python src/peer2.py
    python src/peer3.py
    ```

3. Use the commands listed above to interact with the tracker and other peers.

