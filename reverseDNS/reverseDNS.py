import sys
import socket

def main():
    # Usage check
    if len(sys.argv) == 1 or sys.argv[1] == "-h":
        usage(sys.argv[0])

    arg = sys.argv[1]

    # Parse the IP for validation
    try:
        ip = socket.gethostbyname(arg)
    except socket.error:
        sys.exit(f"Valid IP not detected. Value provided: {arg}")

    print(f"{arg}\t", end='')

    try:
        hostnames, _, _ = socket.gethostbyaddr(ip)
    except socket.herror as e:
        sys.exit(f"Error looking up hostnames: {e}")

    for hostname in hostnames:
        print(hostname, end='')

def usage(name):
    print(f"Usage:\t{name} ip")
    print("Looking up hostnames for IP address")
    sys.exit(1)

if __name__ == "__main__":
    main()
