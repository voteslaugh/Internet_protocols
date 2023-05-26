import smtp.smtp_functions as smtp_func
from parser import get_args

from smtp.message import Message


def main(args):
    try:
        client = smtp_func.create_connection_security(args.server, args.port, args.login)
        smtp_func.authorization(client, args.login, args.password)

        msg = Message()
        msg.configure_message(
            args.login,
            args.receiver,
            args.subject,
            args.text,
            args.path)

        smtp_func.send(client, args.login, args.receiver, msg.message)
        smtp_func.close(client)
    except smtp_func.SMTPError as e:
        print(e)


if __name__ == "__main__":
    args = get_args()
    main(args)
