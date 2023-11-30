import geoip2.database

def main():
    targets = [
        "173.255.226.98",
        "81.2.69.142",
        "35.184.160.12",
    ]

    for target in targets:
        try:
            print_record(target)
        except Exception as e:
            print(f"Error: {e}")

def print_record(target):
    if not target:
        raise ValueError("Error: IP is empty")

    db_path = "GeoLite2-City.mmdb"

    with geoip2.database.Reader(db_path) as reader:
        response = reader.city(target)

        print(f"[*] Target: {target} Geo-located.")
        print(f"[+] {response.city.names.get('en', '')}, {response.subdivisions[0].names.get('en', '')}, {response.country.names.get('en', '')}")
        print(f"[+] ISO country code: {response.country.iso_code}")
        print(f"[+] Time zone: {response.location.time_zone}")
        print(f"[+] Coordinates: {response.location.latitude}, {response.location.longitude}")

if __name__ == "__main__":
    main()
