import re
import socket
import ssl
from base64 import b64encode

from smtp.smtp_exception import SMTPError

B_SIZE = 4096
CODE_PATTERN = re.compile('(\d{3})')


def create_connection_security(addr, port, user):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = ssl.wrap_socket(sock)
    sock.settimeout(1)
    sock.connect((addr, port))
    message = sock.recv(B_SIZE)
    if _get_code(message) != 220 and _get_code(message) != 250:
        raise SMTPError(f'Hello error: {message}')

    sock.send(bytes(f'EHLO {user}\n', 'UTF-8'))

    message = sock.recv(B_SIZE)

    ans_code = _get_code(message)
    if ans_code != 250 and ans_code != 220:
        raise SMTPError(f'Hello error: {message}')

    return sock


def create_connection(addr, port, user):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    sock.connect((addr, port))
    sock.send(bytes(f'EHLO {user}\n', 'utf-8'))

    message = sock.recv(B_SIZE)

    if _get_code(message) != 250:
        raise SMTPError(f'Hello error: {message}')

    return sock


def _get_code(answer):
    matcher = CODE_PATTERN.search(answer.decode('utf-8'))
    if matcher.group():
        return int(matcher.group())
    else:
        return -1


def send(sock, sender, receiver, msg):
    sock.send(b'mail from: ' + sender.encode('utf-8') + b'\n')
    message = sock.recv(B_SIZE)
    if _get_code(message) != 250:
        raise SMTPError(f'Error in the sender\'s mailbox: {message}')

    sock.send(b'rcpt to: ' + receiver.encode('utf-8') + b'\n')
    message = sock.recv(B_SIZE)
    if _get_code(message) != 250:
        raise SMTPError(f'Error in the recipient\'s mailbox: {message}')

    sock.send(b'data\n')
    message = sock.recv(B_SIZE)
    if _get_code(message) != 354:
        raise SMTPError(message)

    sock.send(msg.encode('utf-8') + b'\n')
    sock.send(b'.\n')


def authorization(sock, username, pswd):
    sock.send(b'AUTH LOGIN\n')
    message = sock.recv(B_SIZE)

    if _get_code(message) != 334:
        raise SMTPError(f'Auth error: {message}')

    sock.send(b64encode(username.encode('utf-8')) + b'\n')
    message = sock.recv(B_SIZE)

    if _get_code(message) != 334:
        raise SMTPError(f'Auth error: {message}')

    sock.send(b64encode(pswd.encode('utf-8')) + b'\n')
    message = sock.recv(B_SIZE)

    if _get_code(message) != 235:
        raise SMTPError(f'Auth error: {message}')


def close(sock):
    sock.send(b'QUIT\n')
    sock.close()
