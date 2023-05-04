TCP Scanner
======

This is a simple TCP scanner that can be used to find open ports on a given host. It takes in a hostname or IP address, as well as a range of ports to scan.

## Usage

To use the TCP scanner, simply run the `scanner.py` script with the desired arguments. The available arguments are:

- `--host`: The hostname or IP address to scan. Defaults to `localhost`.
- `--bottom`: The bottom range of ports to scan. Defaults to `1`.
- `--top`: The top range of ports to scan. Defaults to `65535`.

For example, to scan ports 80 through 100 on `example.com`, you would run:

```bash
python3 scanner.py --host example.com --bottom 80 --top 100
```

To check localhost open ports:

```bash
python3 scanner.py
```
