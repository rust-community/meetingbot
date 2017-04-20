#!/usr/bin/env python
"""
minute maker - finds missing rust community team minutes
via meeting agendas raised in "team" repo's issues
"""
import logging
import os
import re
import pickle
import requests
from pathlib import Path
from simpledate import SimpleDate
from github import Github


def get_issues():
    """
    Looks for meeting related open issues
    Returns: list of GitHub issues
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    token = os.environ['CATHULHU_GH_PAT']
    gh = Github(token)  # pylint: disable=invalid-name
    repo = gh.get_organization('rust-community').get_repo('team')
    issues = repo.get_issues(state="close")
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}).*meeting', re.IGNORECASE)
    meetings = []
    for issue in issues:
        issue_match = pattern.match(issue.title)
        if issue_match:
            meeting_date = issue_match.group(1)
            logger.debug("#%d: %s => %s", issue.number,
                         issue.title, meeting_date)
            meetings.append(issue)

    return meetings


def get_existing_minutes():
    """
    test code
    Returns: a set of minutes already in the repo
    """
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # FIXME hard coded
    files = sorted(
        Path('/Users/booyaa/dev/github/rust-community/team/meeting-minutes').glob('*.txt'))
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
    urls = dict()

    issues = load_data("issues")

    minutes = get_existing_minutes()
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2}).*meeting', re.IGNORECASE)
    for issue in issues:
        issue_match = pattern.match(issue.title)
        if issue_match:
            meeting_date = issue_match.group(1)
            minute_file = meeting_date + '.txt'
            if minute_file not in minutes:
                # http://logs.glob.uno/?c=mozilla%23rust-community&s=25+Jan+2017&e=25+Jan+2017&t=text
                glob_log_date = SimpleDate(meeting_date, format="%d+%b+%Y")
                url = "http://logs.glob.uno/?c=mozilla%23rust-community&s={}&e={}&t=text".format(
                    glob_log_date, glob_log_date)
                urls[meeting_date] = url

    return urls


def download_logs(dry_run=False):
    """
    Saves irc logs to the file system
    """
    urls = load_data("urls")

    for issue in urls.keys():
        url = urls[issue]
        print("downloading... ", url)

        r = requests.get(url)
        minutes = r.text
        if r.status_code == 200 and len(minutes):
            # saving minutes
            filename = issue+".txt"
            base_dir = "/Users/booyaa/dev/github/rust-community/team/meeting-minutes" # FIXME: hard coded
            save_to = os.path.join(base_dir, filename)
            if dry_run:
                print("dry run: minutes file: ", save_to)
                continue
            with open(save_to, 'w') as f:
                f.write(minutes)
            print("saved minutes as ", save_to)
        else:
            # failed to save report status_code and size of text
            print("failed to save minute! status: ", r.status_code, " body length: ", len(minutes))

if __name__ == "__main__":
    # 1 - get issues
    issues = get_issues()
    save_data(issues, 'issues')
    print("saved issues locally")
    # print(load_data("issues"))
    # for item in load_data("issues"):
        # print(item)

    # 2 - get urls
    urls = get_irclog_urls()
    save_data(urls, 'urls')
    print(load_data("urls")) 

    # 3 - download logs
    # download_logs(dry_run=True)
    download_logs()