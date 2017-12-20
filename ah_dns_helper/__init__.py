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
        self.get_NS_records()
        self.get_MX_records()
        self.get_A_records()
        self.get_AAAA_records()
        self.get_PTR_records()

    def __repr__(self):
        result = self.repr_query_string()

        result += '\n\n'

        result += (
            '  query_string: {query}\n'
            '  domain: {domain}\n'
            '  hostname: {hostname}'.format(
                query=self.query_string,
                domain=self.domain,
                hostname=self.hostname
            )
        )

        result += self.repr_nameservers()

        return result

    def repr_query_string(self):
        result = 'You asked about %s\n\n' % self.query_string

        if self.domain == self.query_string:
            result += 'That is actually a domain. Well done!\n\n'
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
        elif self.domain == self.hostname:
            result += (
                'That\'s actually a hostname rather than a domain. '
                'As far as I can tell the domain that matches '
                'is {0}\n'.format(self.hostname)
            )

        return result

    def repr_nameservers(self):
        result = '\n  Nameservers:\n'
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

        self.find_domain()
        self.get_NS_records()

    def find_domain(self):
        try:
            if dns.resolver.query(self.hostname, 'NS'):
                self.domain = self.hostname
        except dns.resolver.NXDOMAIN:
            print('{host} is not a valid hostname'.format(host=self.hostname))
            sys.exit(1)
        except dns.resolver.NoAnswer:
            try:
                parent = dns.name.from_text(self.hostname).parent().to_text()
                if dns.resolver.query(parent, 'NS'):
                    self.domain = parent
            except ValueError:
                pass

    def get_NS_records(self):
        self.nameservers = dns.resolver.query(self.domain, 'NS')

    def get_MX_records(self):
        pass

    def get_A_records(self):
        pass

    def get_AAAA_records(self):
        pass

    def get_PTR_records(self):
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
