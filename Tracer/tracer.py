import re
import subprocess
from argparse import ArgumentParser
from ipwhois import IPWhois
from prettytable import PrettyTable


def trace(f):
    def wrapper(*args, **kwargs):
        print(f'\nTracing a route:\n')
        result = f(*args, **kwargs)
        print(result)
        print('\nTracing completed.')
        return result
    return wrapper


class Tracer:
    def __init__(self):
        self.ip_regex = r'(?:\d{1,3}\.){3}\d{1,3}'
        self.table = PrettyTable(['hop', 'ip', 'asn', 'country', 'provider'])

    @trace
    def get_table(self, host):
        addresses = re.findall(self.ip_regex, self._traceroute(host))[1:]
        res = [(self._get_ip_info(ip)) for ip in addresses]
        for n, row in enumerate(res, 1):
            self.table.add_row([n] + [(row.get(k) or '-') for k in row.keys()])
        return self.table

    @staticmethod
    def _get_ip_info(ip: str) -> dict:
        ip_info = {'ip': ip}
        try:
            res = IPWhois(ip).lookup_rdap()
        except:
            res = {}
        ip_info['asn'] = res.get('asn')
        ip_info['country'] = res.get('asn_country_code')
        ip_info['provider'] = res.get('network', {}).get('name')
        return ip_info

    @staticmethod
    def _traceroute(host: str) -> str:
        result = subprocess.run(['traceroute', '-n', '-m', '50', host], capture_output=True, text=True)
        return result.stdout


def get_arg_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('host',
                        help='IP address or domain name')
    return parser


def main():
    tracer = Tracer()
    args = get_arg_parser().parse_args()
    tracer.get_table(args.host)


if __name__ == '__main__':
    main()
