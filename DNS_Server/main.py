import sys
import traceback

from app.server import Server


def main():
    try:
        Server().run()
    except KeyboardInterrupt as e:
        print(f"Server stopped^ {e}")
    except Exception as e:
        traceback.print_tb(sys.exc_info()[2])
        print(f"Unhandled error: {e}")


if __name__ == "__main__":
    main()
