import argparse
import csv
import socket
from threading import Thread

tcp_ports = []
udp_ports = []


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'target',
        help='Целевой адрес сканирования')
    parser.add_argument(
        '-p', '--ports',
        default='1-1024',
        help='Список портов для сканирования, указанных через ","; можно указывать диапазон (80, 144, 2303-2400)')
    return parser.parse_args()


def get_db():
    db = {
        'udp': {},
        'tcp': {}
    }
    with open('port_serv_names.csv') as csv_file:
        data = csv.reader(csv_file)
        for rec in data:
            if rec[0] != 'Service Name':
                try:
                    db[rec[2]].update({rec[1]: rec[0]})
                except KeyError:
                    pass
    return db


def scan_ports(target, ports, db):
    sock = None
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            sock.connect((target, port))
        except Exception:
            print(f"{port}/tcp \tclosed")
        else:
            try:
                print(f"{port}/tcp \t{db['tcp'][str(port)]} \topen")
            except KeyError:
                print(f"{port}/udp \topen")
            tcp_ports.append(port)
        finally:
            sock.close()


def main():
    args = get_args()

    if args.ports == 'all':
        args.ports = '1-65535'

    ranges = (x.split("-") for x in args.ports.split(","))
    ports = [i for r in ranges for i in range(int(r[0]), int(r[-1]) + 1)]

    db = get_db()

    print(f"Scanning {args.target}...")
    port_offset = len(ports)

    for i in range(10):
        t = Thread(
            target=scan_ports,
            args=(
                args.target,
                ports[port_offset * i:port_offset * (i + 1)], db,))
        t.start()


if __name__ == '__main__':
    main()
