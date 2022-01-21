#!/usr/bin/env python3
import socket, sys, time

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def get_remote_ip(host):
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print('Hostname invalid')
        sys.exit

    return remote_ip


def main():
    external_host = "www.google.com"
    external_port = 80

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Launching server")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            conn, addr = proxy_start.accept()
            print("Connected")

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(external_host)
                proxy_end.connect((remote_ip, external_port))
                data = conn.recv(BUFFER_SIZE)
                proxy_end.sendall(data)
                reply = proxy_end.recv(BUFFER_SIZE)
                print("Sending data to client")
                conn.send(reply)

            conn.close()


if __name__ == "__main__":
    main()
