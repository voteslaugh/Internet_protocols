from server import DNSServer
import socket

LOCALHOST = "127.0.0.1"
PORT = 53


def main():
    dns_server = DNSServer()
    dns_server.cache_handler.load("cache")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LOCALHOST, PORT))

    try:
        while True:
            query, addr = sock.recvfrom(2048)
            rdata = dns_server.process(query)
            if rdata:
                sock.sendto(rdata, addr)
    except KeyboardInterrupt:
        dns_server.cache_handler.save("cache_handler")
        sock.close()


if __name__ == "__main__":
    main()
