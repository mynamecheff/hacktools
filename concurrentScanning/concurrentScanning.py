import argparse
import socket
import threading
import queue
from colorama import init, Fore
from rich.console import Console

def usage(name):
    print(f"Usage:\t{name} scanme.nmap.org")
    print("Scanning scanme.nmap.org")
    exit(1)

def worker(ports, results, target):
    while True:
        p = ports.get()
        if p is None:
            break

        address = f"{target}:{p}"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)

        try:
            sock.connect((target, p))
            sock.close()
            results.put(p)
        except (socket.timeout, ConnectionRefusedError):
            results.put(0)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Target to scan (e.g., scanme.nmap.org)")
    args = parser.parse_args()

    console = Console()
    init(autoreset=True)

    spinner = console.spinner("[red]Scanning...[/red]")
    spinner.start()

    target = args.target
    ports = queue.Queue(maxsize=100)
    results = queue.Queue()

    open_ports = []

    for _ in range(100):
        threading.Thread(target=worker, args=(ports, results, target), daemon=True).start()

    for i in range(1, 1025):
        ports.put(i)

    for _ in range(1024):
        port = results.get()
        if port != 0:
            open_ports.append(port)

    ports.join()

    open_ports.sort()
    print()

    for port in open_ports:
        console.print(f"{port} open", style=Fore.GREEN)

    spinner.stop()

if __name__ == "__main__":
    main()
