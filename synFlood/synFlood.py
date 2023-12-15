import os
import socket
import threading
import time
from scapy.all import sniff, IP, TCP

def capture(iface, target, results):
    def packet_callback(packet):
        if IP in packet and TCP in packet:
            src_host = packet[IP].src
            src_port = packet[TCP].sport

            if src_host != target:
                return

            results[src_port] += 1

    sniff(iface=iface, prn=packet_callback, store=0)

def main():
    if len(os.sys.argv) != 4:
        print("Usage: sudo python3 main.py <capture_iface> <target_ip> <port1,port2,port3>")
        os.sys.exit(1)

    iface = os.sys.argv[1]
    target = os.sys.argv[2]
    ports = explode(os.sys.argv[3])

    try:
        devices = os.popen('tcpdump -D').readlines()
        dev_found = any(iface in device for device in devices)
    except:
        dev_found = False

    if not dev_found:
        print(f"Device named '{iface}' does not exist")
        return

    results = {}
    capture_thread = threading.Thread(target=capture, args=(iface, target, results))
    capture_thread.start()

    time.sleep(1)

    for port in ports:
        target = f"{target}:{port}"
        print(f"Trying {target}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, 1))
        sock.close()

    time.sleep(2)

    for port, confidence in results.items():
        if confidence >= 1:
            print(f"Port {port} open (confidence: {confidence})")

def explode(port_string):
    return [p.strip() for p in port_string.split(',')]

if __name__ == "__main__":
    main()
