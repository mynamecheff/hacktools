import sys
from dns import resolver, rdatatype, exception

def main():
    # usage
    if len(sys.argv) == 1 or sys.argv[1] == "-h":
        print(f"Usage:\t{sys.argv[0]} domainName")
        print(f"Ex:\t{sys.argv[0]} github.com")
        print("Output format: IP")
        sys.exit(1)

    domain_name = sys.argv[1]

    try:
        result = resolver.resolve(domain_name, rdatatype.A)
    except exception.DNSException as e:
        print(f"Error: {e}")
        sys.exit(1)

    if not result.rrset:
        print("No records")
        return

    for answer in result:
        if answer.rdtype == rdatatype.A:
            print(answer.address)

if __name__ == "__main__":
    main()
