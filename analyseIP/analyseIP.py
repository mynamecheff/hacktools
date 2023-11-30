import aiohttp
import asyncio
import sys
import argparse
import json
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

async def shodan_lookup(ip_address, session, error_dict):
    url = f'https://internetdb.shodan.io/{ip_address}'

    try:
        async with session.get(url) as response:
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = await response.json()

            print(f"{Fore.WHITE}IP Address: {Fore.GREEN}{data.get('ip')}")
            print(f"{Fore.WHITE}Hostnames: {Fore.BLUE}{data.get('hostnames')}")
            print(f"{Fore.WHITE}Ports: {Fore.GREEN}{data.get('ports')}")
            print(f"{Fore.WHITE}Tags: {Fore.BLUE}{data.get('tags')}")
            print(f"{Fore.WHITE}Vulnerabilities: {Fore.RED}{data.get('vulns')}")

    except aiohttp.ClientError as e:
        error_dict.setdefault(str(e), []).append(ip_address)

async def process_ips(ip_addresses):
    async with aiohttp.ClientSession() as session:
        error_dict = {}
        tasks = [shodan_lookup(ip, session, error_dict) for ip in ip_addresses]
        await asyncio.gather(*tasks)
        
        # TODO group erros by type
        for error, ips in error_dict.items():
            print(f"{Fore.RED}Error {error} for IPs: {', '.join(ips)}")

def process_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f"{Fore.RED}File not found. Please check the file path.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add network information to IPs")
    parser.add_argument("input", nargs="?", help="IP address to look up. Can also be a TXT or JSON file.")
    parser.add_argument("--jsonfile", help="JSON file containing a list of IPs.")
    parser.add_argument("--txtfile", help="TXT file containing a list of IPs.")
    args = parser.parse_args()

    ip_addresses = []

    if args.input:
        if args.input.endswith('.txt'):
            ip_addresses.extend(process_file(args.input))
        else:
            ip_addresses.append(args.input)

    if args.jsonfile:
        try:
            with open(args.jsonfile, 'r') as json_file:
                json_data = json.load(json_file)
                if isinstance(json_data, list):
                    ip_addresses.extend(json_data)
                else:
                    print(f"{Fore.RED}Invalid JSON format. Please provide a list of IPs.")
                    sys.exit(1)
        except FileNotFoundError:
            print(f"{Fore.RED}JSON file not found. Please check the file path.")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"{Fore.RED}Error decoding JSON file. Please check the file content.")
            sys.exit(1)

    if args.txtfile:
        ip_addresses.extend(process_file(args.txtfile))

    if not ip_addresses:
        print(f"{Fore.RED}No IP addresses provided. Please provide at least one source of IP addresses.")
        sys.exit(1)

    asyncio.run(process_ips(ip_addresses))
