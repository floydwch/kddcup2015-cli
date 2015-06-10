# -*- coding: utf-8 -*-
from cliff.command import Command
from robobrowser import RoboBrowser
try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser
import os


class Download(Command):
    'Download data files from https://www.kddcup2015.com/submission-data.html'

    def get_parser(self, prog_name):
        parser = super(Download, self).get_parser(prog_name)

        parser.add_argument('-u', '--username', help='username(email)')
        parser.add_argument('-p', '--password', help='password')

        return parser

    def take_action(self, parsed_args):
        config_dir = '~/.kddcup2015-cli'
        config_dir = os.path.expanduser(config_dir)

        if os.path.isdir(config_dir):
            config = ConfigParser.ConfigParser(allow_no_value=True)
            config.readfp(open(config_dir + '/config'))

            if parsed_args.username:
                username = parsed_args.username
            else:
                username = config.get('user', 'username')

            if parsed_args.password:
                password = parsed_args.password
            else:
                password = config.get('user', 'password')

        base = 'https://www.kddcup2015.com'
        login_url = '/'.join([base, 'user-ajaxlogin.html'])
        data_url = '/'.join([base, 'submission-data.html'])

        browser = RoboBrowser()

        response = browser.session.post(
            login_url, dict(email=username, pwd=password)).json()

        if response['rs'] == 'error':
            self.app.stdout.write(response['msg'])

        browser.open(data_url)

        src_urls = list(map(lambda x: x['href'], browser.select('tr .blue')))

        for url in src_urls:
            self.app.stdout.write('downloading %s\n' % url)
            request = browser.session.get(url, stream=True)
            with open(url[59:], "wb") as data_files:
                data_files.write(request.content)
