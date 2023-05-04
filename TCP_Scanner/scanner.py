#! /usr/bin/python
import socket
import argparse


def get_args():
    parser = argparse.ArgumentParser(description='TCP scanner.py to find open ports')
    parser.add_argument('--host', type=str, help='IP address or hostname', default='localhost')
    parser.add_argument('--bottom', type=int, help='bottom range of ports', default=1)
    parser.add_argument('--top', type=int, help='top range of ports', default=65535)
    return parser.parse_args()


def scan_ports(host, bottom, top):
    ip = socket.gethostbyname(host)
    for port in range(bottom, top + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(10)
        result = sock.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} is open")
        sock.close()


def main():
    args = get_args()
    scan_ports(args.host, args.bottom, args.top)


if __name__ == '__main__':
    main()
