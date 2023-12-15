import scapy.all as scapy

def list_network_devices():
    devices = scapy.get_if_list()

    if not devices:
        print("No network devices found.")
        return

    for device in devices:
        print(f"Device: {device}")
        addresses = scapy.get_if_addr(device)
        netmasks = scapy.get_if_raw_hw_addr(device)
        
        for address in addresses:
            print(f"    IP:      {address}")
        
        for netmask in netmasks:
            print(f"    Netmask: {netmask}")

        print()

if __name__ == "__main__":
    list_network_devices()
