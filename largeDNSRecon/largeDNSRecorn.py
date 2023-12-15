import argparse
import concurrent.futures
import os
import socket
import tabulate

class Result:
    def __init__(self, hostname, ip_address):
        self.hostname = hostname
        self.ip_address = ip_address

def lookup_a(fqdn, server_addr):
    try:
        ip_addresses = [ip[4][0] for ip in socket.getaddrinfo(fqdn, None)]
        return ip_addresses
    except socket.gaierror:
        return []

def lookup_cname(fqdn, server_addr):
    try:
        cname_result = socket.gethostbyname_ex(fqdn)
        return cname_result[1]
    except socket.gaierror:
        return []

def lookup(fqdn, server_addr):
    results = []
    cfqdn = fqdn

    while True:
        cnames = lookup_cname(cfqdn, server_addr)

        if cnames:
            cfqdn = cnames[0]
            continue

        ips = lookup_a(cfqdn, server_addr)

        if not ips:
            break

        for ip in ips:
            results.append(Result(fqdn, ip))

        break

    return results

def worker(fqdns, server_addr):
    results = []

    for fqdn in fqdns:
        results.extend(lookup(fqdn, server_addr))

    return results

def main():
    parser = argparse.ArgumentParser(description='Perform DNS reconnaissance for a list of hostnames.')
    parser.add_argument('-domain', required=True, help='The target domain to perform guessing against.')
    parser.add_argument('-wordlist', required=True, help='The wordlist file containing hostnames for guessing.')
    parser.add_argument('-c', type=int, default=100, help='The number of worker threads to use.')
    parser.add_argument('-server', default='8.8.8.8', help='The DNS server to use.')
    args = parser.parse_args()

    if not os.path.isfile(args.wordlist):
        print(f"Error: Wordlist file '{args.wordlist}' not found.")
        return

    with open(args.wordlist, 'r') as wordlist_file:
        fqdns = [f"{line.strip()}.{args.domain}" for line in wordlist_file]

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.c) as executor:
        futures = [executor.submit(worker, fqdns_chunk, args.server) for fqdns_chunk in chunks(fqdns, args.c)]
        for future in concurrent.futures.as_completed(futures):
            results.extend(future.result())

    print_results(results)

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def print_results(results):
    headers = ["Hostname", "IP Address"]
    data = [(result.hostname, result.ip_address) for result in results]

    print(tabulate.tabulate(data, headers=headers))

if __name__ == "__main__":
    main()
