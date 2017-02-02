#!/usr/bin/env python
"""meetingbot - a helpful bot for meetings
# mvp
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
from simpledate import SimpleDate
from github import Github

def main():
    """driver
    """
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

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
    logging.debug("pre-checks")

    meeting_date = '2017-01-25'
    logging.warn("for testing purposes override meeting day to {}".format(meeting_date))

    last_week = (SimpleDate(meeting_date) + dt.timedelta(days=-7)).strftime("%Y-%m-%d")
    logging.debug("last week was: {}".format(last_week))

    logging.debug("searching for minutes")
    token = os.environ['CATHULHU_GH_PAT']
    g = Github(token)
    team_repo =  g.get_organization('rust-community').get_repo('team')
    # last_commit =team_repo.get_commits()[0]
    # logging.debug("last file commit: {}".format(last_commit.files[0].filename))
    last_commit_filename='meeting-minutes/2016-12-21.txt'
    logging.debug("cache filename: {}".format(last_commit_filename))
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
        logging.warn("Creating this week's agenda!")

if __name__ == '__main__':
    print("Interactive mode!")
    main()
