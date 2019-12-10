
from systematic.shell import Script

from .commands.list import ListCommand


def main():
    """
    Main function  for vyos-config script
    """

    script = Script()

    script.add_subcommand(ListCommand())

    script.run()


if __name__ == '__main__':
    main()
