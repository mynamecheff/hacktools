import os
from scapy.all import *
from geoip2 import database

def print_record(src, dst, db):
    if not src or not dst:
        raise ValueError("Error IP")

    record_src = db.city(src)
    record_dst = db.city(dst)

    print(f"[+] SRC: {record_src.city.names['en']}, {record_src.country.names['en']}")
    print(f"[+] DST: {record_dst.city.names['en']}, {record_dst.country.names['en']}")

def main():
    device = "wlp3s0"
    snapshot_len = 1024
    promiscuous = False
    timeout = 30

    # Opening the interface
    handle = sniff(iface=device, prn=lambda x: process_packet(x), store=0)

def process_packet(packet):
    # From whom to whom
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        print(f"[+] Src: {src}, --> Dst: {dst}")

        try:
            abs_path = os.path.abspath("GeoLite2-City.mmdb")
            reader = database.Reader(abs_path)
            print_record(src, dst, reader)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
