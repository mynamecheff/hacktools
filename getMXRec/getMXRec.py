import sys
import dns.resolver

def main():
    # Check for command-line arguments
    if len(sys.argv) == 1 or sys.argv[1] == "-h":
        usage(sys.argv[0])

    domain = sys.argv[1]

    try:
        # Lookup MX records for the specified domain
        mx_records = dns.resolver.resolve(domain, 'MX')
        
        # Print the MX records
        for mx_record in mx_records:
            print(f"Host: {mx_record.exchange}\tPreference: {mx_record.preference}")

    except dns.resolver.NXDOMAIN:
        print(f"Error: Domain '{domain}' not found.")
    except dns.resolver.NoAnswer:
        print(f"No MX records found for domain '{domain}'.")
    except Exception as e:
        print(f"Error: {e}")

def usage(name):
    print(f"Usage:\t{name} hostname")
    print("Looking up MX records")
    sys.exit(1)

if __name__ == "__main__":
    main()
