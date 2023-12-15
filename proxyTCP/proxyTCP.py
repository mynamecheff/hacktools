import socket
import threading
import binascii

LOCAL_ADDR = "localhost"
LOCAL_PORT = 9999
REMOTE_ADDR = "localhost"
REMOTE_PORT = 80

def main():
    print(f"Listening: {LOCAL_ADDR}:{LOCAL_PORT}\nProxying: {REMOTE_ADDR}:{REMOTE_PORT}\n")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((LOCAL_ADDR, LOCAL_PORT))
    server.listen(5)

    pending, complete = [], []

    for i in range(5):
        threading.Thread(target=handle_conn, args=(pending, complete)).start()

    threading.Thread(target=close_conn, args=(complete,)).start()

    while True:
        conn, addr = server.accept()
        pending.append(conn)

def proxy_conn(conn):
    try:
        remote_addr = (REMOTE_ADDR, REMOTE_PORT)
        remote_conn = socket.create_connection(remote_addr)

        buf = b''
        while True:
            data = conn.recv(256)
            if not data:
                break
            buf += data

            if b'\r\n' in data:
                break

        remote_conn.sendall(buf)
        print(f"sent:\n{binascii.hexlify(buf).decode('utf-8')}")

        data = remote_conn.recv(1024)
        print(f"received:\n{binascii.hexlify(data).decode('utf-8')}")

        conn.sendall(data)

    except Exception as e:
        print(e)

    finally:
        conn.close()
        remote_conn.close()

def handle_conn(in_queue, out_queue):
    while True:
        conn = in_queue.pop(0)
        proxy_conn(conn)
        out_queue.append(conn)

def close_conn(in_queue):
    for conn in in_queue:
        conn.close()

if __name__ == "__main__":
    main()
