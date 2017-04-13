#!/usr/bin/env python
import logging
import os
from github import Github


class MeetingBot:

    def __init__(self, config):
        logging.basicConfig(level=logging.DEBUG)

        self.config = config
        self.github = Github(os.environ[config['gh_token']])

    def _find_agenda(self, when):
        logging.debug('Looking for agenda: %s', when)
        return False

    def _find_minutes(self, when):
        logging.debug('Looking for minutes: %s', when)
        return False

    def pre_check(self):
        """
        Checks for this meeting's agenda and last meeting minutes.
        """
        logging.debug('precheck')

        when = '2017-02-15'
        if not self._find_agenda(when):
            logging.info('Creating agenda!')

        when = '2017-02-01'
        if not self._find_minutes(when):
            logging.info('Creating minutes!')


def get_config():
    """
    Meeting config settings will eventually live in a config file.

    Returns dict with config settings
    """
    return dict(
        meeting_day="Wednesday",
        meeting_time="17:00",
        team_org="rust-community",
        team_repo="team",
        gh_token="CATHULHU_GH_PAT"
    )


def save_minutes(when):
    """
    fetches m
    """

if __name__ == '__main__':
    # logger = logging.getLogger(__name__)

    print('hello')
    meetingbot = MeetingBot(get_config())
    meetingbot.pre_check()

    print('goodbye')

    # if day_before_meeting: # what if you want several reminders?
    #     do_pre_check()
    # if meeting_day():
    #     if now():
    #         announce()
    #     if ended(): # 2 hrs after meeting
    #         save_minutes(when)

    # config = get_config()
    # token = os.environ[config['gh_token']]
    # g = Github(token)

    # precheck(load_issues())
    # save_minutes()
    # save_issues(g)
    # logging.info('cached issues')
    # issues = load_issues(g)
    # logging.info('loading from cache! %s', issues[0])
