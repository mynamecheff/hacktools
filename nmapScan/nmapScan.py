import sys
import subprocess

arg = 2

def main():
    # Check for the correct number of command line arguments
    if len(sys.argv) != arg:
        print(f"Usage: {sys.argv[0]} ip-addr")
        sys.exit(1)

    # Set the location of NMAP
    binary = "/usr/bin/nmap"

    # Set the arguments
    args = [binary, "-v", "-A", sys.argv[1]]

    # Execute the command
    try:
        subprocess.run(args, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

if __name__ == "__main__":
    main()
