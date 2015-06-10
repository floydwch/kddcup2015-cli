# -*- coding: utf-8 -*-
from cliff.lister import Lister
from robobrowser import RoboBrowser
from pyquery import PyQuery as pq

import os


class Rank(Lister):
    'Watch current rank from https://www.kddcup2015.com/submission-rank.html'

    def get_parser(self, prog_name):
        parser = super(Rank, self).get_parser(prog_name)
        parser.add_argument('-n', '--topN', help='topN ranking, default=10')
        return parser

    def take_action(self, parsed_args):
        config_dir = '~/.kddcup2015-cli'
        config_dir = os.path.expanduser(config_dir)

        if parsed_args.topN:
            topN = int(parsed_args.topN)
        else:
            topN = 10

        base = 'https://www.kddcup2015.com'
        rank_url = '/'.join([base, 'submission-rank.html'])

        browser = RoboBrowser()
        browser.open(rank_url)

        html_str = str(browser.parsed)
        html = pq(html_str)

        country_teams = list(
            map(lambda x: x.text.strip(), html('.country_team')[:topN]))
        scores = list(
            map(lambda x: x.text.strip(), html('.td_result')[:topN]))
        entries = list(
            map(lambda x: x.text.strip(), html('.td_result + td')[:topN]))
        last_subs = list(
            map(lambda x: x.text.strip(), html('.td_result + td + td')[:topN]))

        return (
            ('Team', 'Score', 'Entries', 'Last Submission UTC'),
            (list(zip(country_teams, scores, entries, last_subs)))
        )
