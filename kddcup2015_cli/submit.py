# -*- coding: utf-8 -*-
from cliff.command import Command
from robobrowser import RoboBrowser
from pyquery import PyQuery as pq
from dateutil import parser as datetime_parser
from time import sleep
import os
try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser


class Submit(Command):
    'Submit an entry.'

    def get_parser(self, prog_name):
        parser = super(Submit, self).get_parser(prog_name)

        parser.add_argument('entry', help='entry file')

        parser.add_argument('-m', '--message', help='message')
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

        entry = parsed_args.entry
        message = parsed_args.message

        base = 'https://www.kddcup2015.com'
        login_url = '/'.join([base, 'user-ajaxlogin.html'])
        submit_url = '/'.join([base, 'submission-make.html'])
        submission_url = '/'.join(([base, 'submission.html']))

        browser = RoboBrowser()

        response = browser.session.post(
            login_url, dict(email=username, pwd=password)).json()

        if response['rs'] == 'error':
            self.app.stdout.write(response['msg'])

        browser.open(submit_url)

        form = browser.get_form()

        form['_f'].value = open(entry)

        if message:
            form['description'] = message

        browser.submit_form(form)

        sleep(5)

        browser.open(submission_url)

        html_str = str(browser.parsed)
        html = pq(html_str)

        times = list(map(
            lambda x: datetime_parser.parse(x.text),
            html('.td_result +td+td+td+td')))

        newest_index = times.index(max(times))

        score = html('.td_result')[newest_index].text.strip()
        self.app.stdout.write(score + '\n')
