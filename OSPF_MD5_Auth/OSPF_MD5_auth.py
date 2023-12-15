import sys
from scapy.all import rdpcap

def main():
    if len(sys.argv) == 1:
        print(f"Use: {sys.argv[0]} PCAPFile")
    else:
        pcap_file = sys.argv[1]

        try:
            packets = rdpcap(pcap_file)

            for packet in packets:
                ospf_layer = packet.getlayer('OSPF')
                if ospf_layer:
                    ospf_version = ospf_layer.version
                    ospf_auth_type = ospf_layer.auth_type

                    if ospf_version == 2:
                        if ospf_auth_type == 1:
                            print(f"Simple version: {ospf_auth_type}")
                            print(f"OSPF Pass: {ospf_layer.auth_simple}")
                        elif ospf_auth_type == 2:
                            print(f"MD5 version: {ospf_auth_type}")
                            print(f"Authentication: {ospf_layer.auth_md5}")
        except Exception as e:
            print(f"Error reading PCAP file: {e}")

if __name__ == "__main__":
    main()