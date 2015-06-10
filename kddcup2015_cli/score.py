# -*- coding: utf-8 -*-
from cliff.lister import Lister
from robobrowser import RoboBrowser
from pyquery import PyQuery as pq
import os
try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser


class Score(Lister):
    'Watch your own scores from https://www.kddcup2015.com/submission.html.'

    def get_parser(self, prog_name):
        parser = super(Score, self).get_parser(prog_name)
        parser.add_argument('-n', '--topN', help='topN scores, default=10')
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

        if parsed_args.topN:
            topN = int(parsed_args.topN)
        else:
            topN = 10

        base = 'https://www.kddcup2015.com'
        login_url = '/'.join([base, 'user-ajaxlogin.html'])
        score_url = '/'.join([base, 'submission.html'])
        edit_url = '/'.join([base, 'submission-edit.html'])

        browser = RoboBrowser()

        response = browser.session.post(
            login_url, dict(email=username, pwd=password)).json()

        if response['rs'] == 'error':
            self.app.stdout.write(response['msg'])

        browser.open(score_url)

        html_str = str(browser.parsed)
        html = pq(html_str)

        scores = list(
            map(lambda x: x.text.strip(), html('.td_result')[:(topN * 2)]))[::2]
        file_names = list(
            map(lambda x: x.text.strip(), html('.td_path').children()[:topN]))
        times = list(map(
            lambda x: x.text.strip(), html('.td_result +td+td+td+td')))

        submission_ids = list(map(
            lambda a: a.values()[0][25:],
            html('.aa').children()))

        descriptions = []

        for i in submission_ids:
            browser.open(edit_url + '?id=' + i)
            html = pq(str(browser.parsed))

            description = html('.cont_r').children()[2].text

            if description:
                descriptions.append(description)
            else:
                descriptions.append('')

        return (
            ('Public Score', 'Submitted File', 'Time(UTC)',
                'Description'),
            (list(zip(scores, file_names, times, descriptions)))
        )
