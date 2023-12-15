import sys
import re
import requests

def extract_emails(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}', response.text)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def format_maltego_response(emails):
    print("<MaltegoMessage>")
    print("<MaltegoTransformResponseMessage>")
    print("  <Entities>")

    for email in emails:
        print("    <Entity Type=\"maltego.EmailAddress\">")
        print(f"      <Value>{email}</Value>")
        print("    </Entity>")

    print("  </Entities>")
    print("</MaltegoTransformResponseMessage>")
    print("</MaltegoMessage>")

def main():
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Extracting links from url to Maltego.")
        print(f"Usage: {sys.argv[0]} <url>")
        print("You need a URL, for example: http://domain.com")
        sys.exit(1)

    url = sys.argv[1]
    emails = extract_emails(url)
    format_maltego_response(emails)

if __name__ == "__main__":
    main()
