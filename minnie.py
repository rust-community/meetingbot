#!/usr/bin/env python
"""
minute maker - finds missing rust community team minutes
via meeting agendas raised in "team" repo's issues
"""
import logging
import os
import re
import pickle
from pathlib import Path
from simpledate import SimpleDate
from github import Github

def get_issues():
    """
    Looks for meeting related issues
    Returns: list of GitHub issues
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    token = os.environ['CATHULHU_GH_PAT']
    gh = Github(token) # pylint: disable=invalid-name
    repo = gh.get_organization('rust-community').get_repo('team')
    issues = repo.get_issues(state="close")
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}).*meeting', re.IGNORECASE)
    meetings = []
    for issue in issues:
        issue_match = pattern.match(issue.title)
        if issue_match:
            meeting_date = issue_match.group(1)
            logger.debug("#%d: %s => %s", issue.number, issue.title, meeting_date)
            meetings.append(issue)

    return meetings

def get_existing_minutes():
    """
    test code
    Returns: a set of minutes already in the repo
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    files = sorted(Path('/Users/booyaa/Desktop/team/meeting-minutes').glob('*.txt')) # FIXME hard coded
    minutes = [f.parts[-1] for f in files]

    return minutes

def save_data(data, filename):
    """saves pickled dict of opening times to home dir

    Args:   data - dict of opening times
            filename - name of saved file
    """
    # pylint: disable=invalid-name
    savedir = os.environ["HOME"] + '/.minnie/'
    with open(savedir + filename + '.pickle', 'wb') as f:
        pickle.dump(data, f)

def load_data(filename):
    """
    Args:   data - dict of opening times
            filename - name of saved file

    Returns: issues
    """
    # pylint: disable=invalid-name
    savedir = os.environ["HOME"] + '/.minnie/'
    with open(savedir + filename + '.pickle', 'rb') as f:
        data = pickle.load(f)
        f.close()

    return data

def get_irclog_urls():
    """
    Create a list of urls that can be used to down irc logs from logs.glob.uno

    Returns: list of urls
    """
    urls = []
    # issues = get_issues()
    issues = load_data("issues")

    minutes = get_existing_minutes()
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}).*meeting', re.IGNORECASE)
    for issue in issues:
        issue_match = pattern.match(issue.title)
        if issue_match:
            meeting_date = issue_match.group(1)
            minute_file = meeting_date+'.txt'
            if minute_file not in minutes:
                # http://logs.glob.uno/?c=mozilla%23rust-community&s=25+Jan+2017&e=25+Jan+2017&t=text
                glob_log_date = SimpleDate(meeting_date, format="%d+%b+%Y")
                url = "http://logs.glob.uno/?c=mozilla%23rust-community&s={}&e={}&t=text".format(glob_log_date, glob_log_date)
                urls.append(url)

    return urls

    def download_logs():
        """
        Saves irc logs to the file system
        """


if __name__ == "__main__":
    # urls = get_irclog_urls()
    # save_data(urls, 'urls')
    print(load_data("urls")) # TODO: need to create a list with struct containing filename and url
    # issues = get_issues()
    # save_data(issues, 'issues')
    # print("saved issues locally")
    # print(load_data("issues"))