import argparse


def get_args():
    parser = argparse.ArgumentParser(description="SMTP client")
    parser.add_argument(
        "--server",
        default="smtp.yandex.ru",
        help="SMTP server")
    parser.add_argument(
        "--port",
        help="Port to use",
        default=465, type=int)
    parser.add_argument(
        "--username",
        help="Username",
        default='Fusty03')
    parser.add_argument(
        "login",
        help="Sender email address"
    )
    parser.add_argument(
        "password",
        help="Password"
    )
    parser.add_argument(
        "receiver",
        help="Receiver email address"
    )
    parser.add_argument(
        "--subject",
        "-s",
        help="Message subject"
    )
    parser.add_argument(
        "--text",
        "-t",
        help="Message text"
    )
    parser.add_argument(
        "--path",
        "-p",
        help="Path for attachment"
    )
    args = parser.parse_args()
    return args