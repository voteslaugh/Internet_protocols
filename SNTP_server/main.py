from app.sntp_server import SNTPServer


def main():
    try:
        SNTPServer().run()
    except Exception:
        pass


if __name__ == '__main__':
    main()
