import socket
import sys
import threading

args = 2
seconds = 10

def test_tcp_connection(ip, port, done_channel):
    try:
        # Create a socket object
        sock = socket.create_connection((ip, port), timeout=seconds)

        # If successful connection, print the open port
        print(f"Port {port}: Open")
        sock.close()

    except (socket.timeout, socket.error):
        pass

    finally:
        done_channel.set()

def main():
    # Check for correct number of command line arguments
    if len(sys.argv) != args:
        print(f"Using: {sys.argv[0]} ip-addr")
        sys.exit(1)

    target = sys.argv[1]

    active_threads = 0
    done_channel = threading.Event()

    for port in range(0, 65536):
        # Create a thread for each port test
        threading.Thread(target=test_tcp_connection, args=(target, port, done_channel)).start()
        active_threads += 1

    # Wait for all threads to finish
    done_channel.wait()

if __name__ == "__main__":
    main()
