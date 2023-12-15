import argparse
import ssl
import http.client
import urllib.parse
from typing import List
from urllib.request import Request, urlopen
from urllib.error import URLError

def do_req(location: str, timeout: int) -> List[str]:
    try:
        url_parts = urllib.parse.urlsplit(location)
        conn = http.client.HTTPSConnection(url_parts.netloc, timeout=timeout / 1000.0, context=ssl._create_unverified_context())
        conn.request("GET", url_parts.path)
        res = conn.getresponse()

        if res.status == 200:
            return [f"{location}: {c}" for c in res.getheader("Set-Cookie", "").split(",")]

    except URLError as e:
        print(e)

    return []

def main():
    parser = argparse.ArgumentParser(description="cookie-flags takes a URL and returns the cookie set.")
    parser.add_argument("-i", "--input", default="", help="URL")
    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        exit(1)

    print("Start")
    cookies = do_req(args.input, timeout=1000)

    if not cookies:
        print("Not cookies")
    else:
        for c in cookies:
            print(c)

    print("End")

if __name__ == "__main__":
    main()
