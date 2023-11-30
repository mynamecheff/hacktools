import pexpect
import re
import time

def main():
    try:
        # Set the path for ssh
        ssh_path = "/usr/bin/ssh"

        # Create a new SSH connection
        child = pexpect.spawn(f"{ssh_path} user@127.0.0.1")

        # Input the password
        child.expect("password:")
        child.sendline("pass")

        # Input the command
        child.sendline("sudo cat /etc/shadow | grep root")

        # Wait for a short duration
        time.sleep(3)

        # Print the output
        print(child.before.decode())

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
