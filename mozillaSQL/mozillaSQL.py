import sqlite3
import argparse

class SQLiteReader:
    def __init__(self, db_location, param_cookie):
        self.db_location = db_location
        self.param_cookie = param_cookie

    def read_cookies(self):
        with sqlite3.connect(self.db_location) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT host, name, value FROM moz_cookies")
            rows = cursor.fetchall()

            print("[*] -- Found Cookies --")
            for row in rows:
                host, name, value = row
                print(f"[+] Host: {host}, Cookie: {name}, Value: {value}")

    def read_history(self):
        with sqlite3.connect(self.db_location) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT url, datetime(visit_date/1000000, 'unixepoch') FROM moz_places, moz_historyvisits WHERE visit_count > 0 AND moz_places.id == moz_historyvisits.place_id;")
            rows = cursor.fetchall()

            print("[*] -- Found History --")
            for row in rows:
                url, date = row
                print(f"[+] {date} - Visited: {url}")

def main():
    parser = argparse.ArgumentParser(description="Read cookies or places from SQLite database.")
    parser.add_argument("-l", dest="db_location", help="Locate SQLite file", required=True)
    parser.add_argument("-p", dest="param_cookie", action="store_true", help="Cookies or Places? Default - Cookie.")
    args = parser.parse_args()

    sqlite_reader = SQLiteReader(args.db_location, args.param_cookie)

    if args.param_cookie:
        sqlite_reader.read_cookies()
    else:
        sqlite_reader.read_history()

if __name__ == "__main__":
    main()
