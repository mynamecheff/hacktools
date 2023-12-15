import paramiko
import socket
import threading
import os

class Endpoint:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __str__(self):
        return f"{self.host}:{self.port}"

class SSHtunnel:
    def __init__(self, local, server, remote, config):
        self.local = local
        self.server = server
        self.remote = remote
        self.config = config

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.local.host, self.local.port))
        server_socket.listen(5)

        while True:
            local_conn, _ = server_socket.accept()
            threading.Thread(target=self.forward, args=(local_conn,)).start()

    def forward(self, local_conn):
        with paramiko.SSHClient() as ssh:
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.server.host, port=self.server.port, **self.config)

            try:
                remote_conn = ssh.get_transport().open_channel(
                    "direct-tcpip", (self.remote.host, self.remote.port), local_conn.getpeername()
                )

                threading.Thread(target=self.copy_conn, args=(local_conn, remote_conn)).start()
                threading.Thread(target=self.copy_conn, args=(remote_conn, local_conn)).start()

            except paramiko.SSHException as e:
                print(f"SSH error: {e}")

    def copy_conn(self, src_conn, dest_conn):
        try:
            while True:
                data = src_conn.recv(1024)
                if not data:
                    break
                dest_conn.sendall(data)
        except Exception as e:
            print(f"Copy connection error: {e}")
        finally:
            src_conn.close()
            dest_conn.close()

def ssh_agent():
    try:
        agent = paramiko.Agent()
        agent_keys = agent.get_keys()
        return paramiko.AuthenticationString(username=None, key=agent_keys[0]) if agent_keys else None
    except paramiko.SSHException:
        return None

def main():
    local_endpoint = Endpoint("localhost", 9000)
    server_endpoint = Endpoint("example.com", 22)
    remote_endpoint = Endpoint("localhost", 8080)

    ssh_config = {
        "username": "vcap",
        "auth": [ssh_agent()],
    }

    tunnel = SSHtunnel(local=local_endpoint, server=server_endpoint, remote=remote_endpoint, config=ssh_config)

    try:
        tunnel.start()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
