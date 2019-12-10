
from systematic.shell import ScriptCommand

from vyos.configuration.vyos import VyOSConfig


class VyOSCliCommand(ScriptCommand):
    """
    VyOS config CLI command base class
    """

    def parse_args(self, args):

        self.config = VyOSConfig()
        if 'path' in args:
            self.config.load(args.path)

        return args
