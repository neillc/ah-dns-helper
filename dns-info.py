#!/usr/bin/env python3

import argparse
from urllib.parse import urlparse
import sys
import textwrap

import dns.name
import dns.resolver


def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('domain', help='The domain to show info about')

    parser.add_argument(
        '--nameserver', '-n',
        action='store_true',
        help='show nameserver info'
    )
    parser.add_argument(
        '--mailexchange', '-m',
        action='store_true',
        help='show MX info'
    )
    parser.add_argument(
        '--ip', '-i',
        action='store_true',
        help='show IP address info'
    )

    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='List all information'
    )

    args = parser.parse_args()

    if args.all:
        args.nameserver = True
        args.ip = True
        args.mailexchange = True

    return args


class QueryObject(object):
    def __init__(self, query_string):
        self.query_string = query_string
        self.domain = None
        self.scheme = None

        self.convert_query_string_to_host()
        self.get_NS()
        self.get_MX()
        self.get_A()
        self.get_AAAA()
        self.get_PTR()

    def __repr__(self):
        result = 'You asked about %s\n\n' % self.query_string

        if self.domain == self.query_string:
            result += 'That is actually a domain. Well done!\n\n'
        elif self.domain == self.hostname:
            result += (
                'That\'s actually a hostname rather than a domain. '
                'As far as I can tell the domain that matches '
                'is {0}\n'.format(self.hostname)
            )
        elif self.scheme is not None:
            result += '\n'.join(
                textwrap.wrap(
                    'That actually looks like a url. My best guess at the '
                    'matching hostname is {0} and the domain looks like '
                    '{1}'.format(
                        self.hostname,
                        self.domain
                    ),
                    break_on_hyphens=False
                )
            )

        result += '\n\n'

        if self.nameservers:
            if self.nameservers[0].to_text().endswith('googledomains.com.'):
                result += (
                    'It looks like that domain has been delegated to '
                    'Google\'s cloud DNS\n'
                )
            elif self.nameservers[0].to_text().endswith('ace-hosting.com.au'):
                result += (
                    'It looks like that domain has been delegated to '
                    'Ace Hosting\'s DNS\n'
                )

        result += '\n\nDetails:\n'

        result += (
            '  query_string: {query}\n'
            '  domain: {domain}\n'
            '  hostname: {hostname}'.format(
                query=self.query_string,
                domain=self.domain,
                hostname=self.hostname
            )
        )

        result += '\n  Nameservers:\n'

        for ns in self.nameservers:
            result += '    ' + ns.to_text() + '\n'

        return result

    def convert_query_string_to_host(self):
        url = urlparse(self.query_string)

        if url.scheme:
            self.hostname = url.hostname
            self.scheme = url.scheme
        elif url.hostname:
            self.hostname = url.hostname
        else:
            self.hostname = url.path

        try:
            import pdb;pdb.set_trace()
            answer = dns.resolver.query(self.hostname, 'NS')
            if answer:
                self.domain = self.hostname
        except dns.resolver.NXDOMAIN:
            print('{host} is not a valid hostname'.format(host=self.hostname))
            sys.exit(1)
        except dns.resolver.NoAnswer:
            try:
                parent = dns.name.from_text(self.hostname).parent().to_text()
                answer = dns.resolver.query(
                    parent, 'NS'
                )
                if answer:
                    self.domain = parent
            except ValueError:
                pass

        self.get_NS()

    def get_NS(self):
        self.nameservers = dns.resolver.query(self.domain, 'NS')

    def get_MX(self):
        pass

    def get_A(self):
        pass

    def get_AAAA(self):
        pass

    def get_PTR(self):
        pass

    def get_details_as_text(self):
        return ""

    def get_details_as_html(self):
        return '<p></p>'


def main():
    args = parse_command_line()

    query_object = QueryObject(args.domain)

    print(query_object)


if __name__ == '__main__':
    main()