# -*- coding: utf-8 -*-
import sys
from cliff.app import App
from cliff.commandmanager import CommandManager


class KDDCup2015CLI(App):

    def __init__(self):
        super(KDDCup2015CLI, self).__init__(
            description='An unofficial command line tool for KDD Cup 2015.',
            version='0.1.0',
            command_manager=CommandManager('kddcup2015_cli'),
        )


def main(argv=sys.argv[1:]):
    app = KDDCup2015CLI()

    return app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
