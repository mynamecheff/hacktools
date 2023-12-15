import os
import sys
import geoip2.database

pcap_file = ""
handle = None
err = None

def main():
    global pcap_file, handle, err

    # Help
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} PCAP_FILE")
        sys.exit(1)

    pcap_file = sys.argv[1]

    # Open file
    try:
        handle = open(pcap_file, 'rb')
    except FileNotFoundError:
        sys.exit(f"Error opening file {pcap_file}")

    # Header & Footer KML
    kml_header = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>"""
    kml_footer = """</Document>
</kml>"""

    # Data structures
    all_ip = {}
    all_kml = ""

    # Process all packets
    try:
        for line in handle:
            # Assuming each line in the file represents a packet
            # Replace this part with your packet processing logic
            # For simplicity, this code just prints the hex representation of each byte
            hex_line = ' '.join(format(byte, '02x') for byte in line)
            print(hex_line)
    except Exception as e:
        sys.exit(f"Error processing packets: {e}")
    finally:
        handle.close()

    # All IPs
    for k in all_ip.keys():
        kml, error = rec_kml(k)
        if error:
            sys.exit(error)
        all_kml += kml + "\n"

    print(kml_header + "\n" + all_kml + kml_footer)

def rec_kml(ip):
    if not ip:
        return "", "Not IP"

    abs_path = os.path.abspath("GeoLite2-City.mmdb")
    try:
        with geoip2.database.Reader(abs_path) as db:
            ip_new = ip
            record = db.city(ip_new)
            kml = f"""<Placemark>
<name>{ip}</name>
<Point>
<coordinates>{record.location.longitude},{record.location.latitude}</coordinates>
</Point>
</Placemark>"""
            return kml, None
    except Exception as e:
        return "", str(e)

if __name__ == "__main__":
    main()
