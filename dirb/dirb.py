import concurrent.futures
import requests
import sys

def main():
    # Load command line arguments
    if len(sys.argv) != 4:
        print(f"{sys.argv[0]} - Perform an HTTP HEAD request to a URL")
        print(f"Usage: {sys.argv[0]} <wordlist_file> <URL> <maxThreads>")
        print(f"Example: {sys.argv[0]} wordlist.txt https://www.devdungeon.com 10")
        sys.exit(1)

    wordlist_filename = sys.argv[1]
    base_url = sys.argv[2]

    try:
        max_threads = int(sys.argv[3])
    except ValueError:
        print("Error converting maxThread value to an integer.")
        sys.exit(1)

    # Read word list file
    with open(wordlist_filename) as wordlist_file:
        # Create an executor for concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
            futures = []

            # Read each line and perform an HTTP HEAD
            for line in wordlist_file:
                # Schedule an HTTP HEAD request in a separate thread
                future = executor.submit(check_if_url_exists, base_url, line.strip())
                futures.append(future)

                # Wait until a done signal before starting the next thread if max threads reached
                if len(futures) >= max_threads:
                    concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
                    futures = []

            # Wait for all threads before exiting
            concurrent.futures.wait(futures)

def check_if_url_exists(base_url, file_path):
    # Create URL
    target_url = base_url.rstrip('/') + '/' + file_path

    try:
        # Perform a HEAD request to check if the path exists
        response = requests.head(target_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        # If server returns 200 OK, the file can be downloaded
        print(target_url)
    except requests.RequestException as e:
        # Log errors and continue
        print(f"Error fetching {target_url}: {e}")

if __name__ == "__main__":
    main()
