import argparse
import socket
import sys

def main():
    parser = argparse.ArgumentParser(description="connect or listen")
    parser.add_argument("hostname", help="hostname to connect to or listen on")
    parser.add_argument("port", type=int, help="port number")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--listen-port", type=int, help="listen port number")

    args = parser.parse_args()

    if args.listen_port:
        listen(args.listen_port)
    else:
        dial(args.hostname, args.port)

def listen(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("", port))
            s.listen()
            print(f"Listening on port {port}")
            conn, addr = s.accept()
            with conn:
                print(f"Accepted connection from {addr}")
                data = conn.recv(4096)
                sys.stdout.buffer.write(data)
    except Exception as e:
        print(f"Error: {e}")

def dial(hostname, port):
    try:
        with socket.create_connection((hostname, port)) as s:
            data = sys.stdin.buffer.read()
            s.sendall(data)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
