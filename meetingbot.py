#!/usr/bin/env python
"""meetingbot - a helpful bot for meetings
# mvp
- sequence of events
    - day before reminder and pre-check that agenda / previous meetings exist
    - on the day
        - T-1 hour reminder
        - announcement
        - T+1.5 save minutes
- unit tests or gtfo
- config file
    - day of meeting
    - time of meeting
    - irc details channel etc
    - github pat to check for issues (agendas and create if necessary) and minutes
- should be able to run every minute or as near to the time as possible
- creates agenda if it doesn't already exist
- creates minutes after the meeting has ended (searches for thanks/gavel/meetingbot stop)

# stretch
- online prescence (negates the need for cron?)
- able to confirm decisions made in previous minutes, or if items were discussed
- create action items in the agenda
"""
import logging
import datetime as dt
import os
import pickle
import requests
from simpledate import SimpleDate
from github import Github

def old_main():
    """driver
    """

    logger.info('Starting...')
    meeting_day = "Friday"
    meeting_time = (SimpleDate()).strftime("%H:%M")

    today = dt.date.today().strftime("%A")

    is_meeting_day = meeting_day == today
    if is_meeting_day:
        logging.debug("meeting day")
        pre_check = (SimpleDate() + dt.timedelta(hours=-1)).strftime("%H:%M")
        # for testing pre_check = "20:00"
        now = SimpleDate().strftime("%H:%M")
        if now >= pre_check:
            meeting_checklist()
        else:
            logging.debug("\tnot time yet")

    logger.info('Finished!')

def meeting_checklist():
    """
    blah
    """
    logging.debug("pre-checks")

    meeting_date = '2017-01-25'
    logging.warning(
        "for testing purposes override meeting day to %s", meeting_date)

    last_week = (SimpleDate(meeting_date) +
                 dt.timedelta(days=-7)).strftime("%Y-%m-%d")
    logging.debug("last week was:%s", last_week)

    logging.debug("searching for minutes")
    token = os.environ['CATHULHU_GH_PAT']
    g = Github(token) # pylint 
    team_repo = g.get_organization('rust-community').get_repo('team')
    # last_commit =team_repo.get_commits()[0]
    # logging.debug("last file commit: {}".format(last_commit.files[0].filename))
    last_commit_filename = 'meeting-minutes/2016-12-21.txt'
    logging.debug("cache filename: %s", last_commit_filename)
    if last_week in last_commit_filename:
        logging.debug("found last weeks minutes")
    else:
        logging.debug("didn't find minutes, do something else...")

    logging.debug("searching for this week's agenda")
    issues = team_repo.get_issues()
    found = False
    for issue in issues:
        if meeting_date in issue.title:
            found = True
            break

    if found:
        logging.debug("Found meeting!")
    else:
        logging.warning("Creating this week's agenda!")

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

def precheck(issues):
    config = get_config()
    logging.info('precheck: %s', config)

    check_for_agenda(config, issues)

    last_meeting_date = '2017-02-17'
    logger.info("can we see previous meeting minutes?")

    if _find_minutes(last_meeting_date):
        logging.info("Found last weeks minutes")
    else:
        logging.warning("Creating minutes! Checking logs.glob.uno")
        _get_minutes(last_meeting_date)

def _get_minutes(last_meeting_date):
    """
    https://developer.github.com/v3/repos/contents/#create-a-file
    http://docs.python-requests.org/en/master/user/quickstart/#response-content
    """
    r = requests.get('http://logs.glob.uno/?c=mozilla%23rust-community&s=11+Feb+2017&e=11+Feb+2017&t=text')
    logging.info('contents: %s', r.text)

def check_for_agenda(config, issues):
    this_meeting_date = _get_this_meeting_date(config)
    this_meeting_date = '2017-02-08'
    logger.info("has agenda been defined (%s)?", this_meeting_date)

    found = False
    for issue in issues:
        if this_meeting_date in issue.title:
            logging.info(issue.title)
            found = True
            break
    if found:
        logging.info("Found meeting!")
    else:
        logging.warning("Creating this week's agenda!")

def _get_this_meeting_date(config):
    meeting_date = dt.date.today().strftime("%Y-%m-%d")
    return meeting_date

def _get_repo(config):
    token = os.environ[config['gh_token']]
    return Github(token).get_organization(config['team_org']).get_repo(config['team_repo'])

def _find_minutes(meeting_date):
    r = requests.\
    head('https://github.com/rust-community/team/tree/master/meeting-minutes/' + \
    meeting_date + '.txt')
    return r.status_code != 404


def save_issues(g):
    """
    Caches open issues. Can't pickle paginatedlist, so we extract to a list first.
    Args: Github instance
    """
    issues_paginated = g.get_organization(config['team_org']).\
                            get_repo(config['team_repo']).\
                            get_issues()

    issues = []
    for issue in issues_paginated:
        issues.append(issue)

    savedir = os.environ["HOME"] + '/.meetingbot/'
    with open(savedir + 'issues' + '.pickle', 'wb') as f:
        pickle.dump(issues, f)

def load_issues():
    """
    Reads cached issues.
    Returns: list of issues
    """
    savedir = os.environ["HOME"] + '/.meetingbot/'
    with open(savedir + 'issues' + '.pickle', 'rb') as f:
        return pickle.load(f)


def save_minutes():
    """
    saves minutes to repo
    """
    r = requests.get('http://logs.glob.uno/?c=mozilla%23rust-community&s=11+Feb+2017&e=11+Feb+2017&t=text')
    logging.info('contents: %s', r.text)
    repo = g.get_repo('booyaa/hello-homu')
    logging.info(repo)
    logging.info(repo.create_file('/minutes/2017-02-11.txt', 'test file', r.text, 'master'))
    logging.info('saved new file')


def create_agenda(g):
    repo = g.get_repo('booyaa/hello-homu')
    logging.info(repo)
    try:
        logging.info('creating issue %s', repo.create_issue(title='Meeting 2017-02-13', body="""
        this is a multi lined test.

        please add you items below.

        - foo
        - bar

        last week's minutes can be found here: http://foo/bar/minutes/2017-02-08.txt"""))
    except:
        logging.error('failed to open repo!')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    config = get_config()
    token = os.environ[config['gh_token']]
    g = Github(token)

    # precheck(load_issues())

    # save_minutes()

    # save_issues(g)
    # logging.info('cached issues')
    # issues = load_issues(g)
    # logging.info('loading from cache! %s', issues[0])


