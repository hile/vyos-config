
import argparse
import sys

from .base import VyOSCliCommand


class ListCommand(VyOSCliCommand):
    """
    List configuration settings as VyOS CLI commands
    """
    name = 'list'
    help = 'List configuration as CLI commands'

    def __register_arguments__(self, parser):
        parser.add_argument('-p', '--prefix', help='Prefix to print')
        parser.add_argument('path', type=argparse.FileType('r'), default=sys.stdin, help='Configuration file path')
        return parser

    def run(self, args):
        for item in self.config:
            if args.prefix and str(item)[:len(args.prefix)] != args.prefix:
                continue
            try:
                print('set {}'.format(item))
            except BrokenPipeError:
                break
