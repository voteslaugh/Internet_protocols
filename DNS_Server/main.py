from app import Server
import logging


def main():
    try:
        Server().run()
    except Exception as e:
        logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(e, exc_info=True)


if __name__ == "__main__":
    main()
