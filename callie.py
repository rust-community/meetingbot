#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This will eventually become a class to identify if there's any work for 
meetingbot to do.
"""
import os
from datetime import datetime, timedelta, timezone

from icalendar import Calendar

import pytz
from pytz import timezone as pytz
import pytz

import requests

"""
references:
- https://cloud.google.com/translate/docs/reference/libraries#client-libraries-install-python
- https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
- https://en.wikipedia.org/wiki/ICalendar
"""


def main():
    """
    - icalendar usage - https://github.com/pybites/bday-app/blob/master/bdays.py
    - convert local time to utc - http://stackoverflow.com/a/25662061/105282
    - RRULE explained - http://www.grokkingandroid.com/recurrence-rule-and-duration-formats/
    - icalendar spec (RRULE) - http://www.kanzaki.com/docs/ical/rrule.html
    """
    calendar_file = os.path.join('dontcommitmebro', 'basic.ics')
    with open(calendar_file, 'rb') as f:
        gcal = Calendar.from_ical(f.read())

    for comp in gcal.walk():
        if comp.name == "VEVENT":
            name = comp.get('SUMMARY')
            if name != "Rust Community Team Meeting":
                continue
            rrule = comp.get('RRULE')
            if not rrule:
                continue
            until = rrule.get('UNTIL')
            if until:
                if until[0] < datetime.now(timezone.utc):
                    continue
            start_time = comp.get('DTSTART').dt
            our_time = get_our_time(start_time)
            print("Calendar entry time: {}\nOur local time     : {}".format(
                start_time, our_time))

            # turn this into next meeting date computation
            blighty=pytz.timezone('Europe/London')
            print('timediff:',datetime.now(tz=blighty)-our_time)
            print(our_time.timetuple().tm_mon)
            if our_time < datetime.now(tz=blighty):
                print("date in the past")
            else:
                print("okay")
            
            next_meeting = (our_time + timedelta(weeks=4)) + timedelta(days=7)
            print("Next meeting will be: {}".format(next_meeting))

            print("Raw RRULE:", rrule)
            print("--------------")


def get_our_time(start_time):
    """
    Convert datetime with tzinfo to local time
    Args:
        start_time - datetime with tzinfo
    Returns:
        date time with our tzinfo
    """
    config = get_config()
    our_timezone = pytz.timezone(config['timezone'])
    # print('\tour timezone: {}'.format(our_timezone))

    their_dt = start_time
    our_dt = their_dt.astimezone(our_timezone)
    # print('\ttheir time: {} our time: {}'.format(their_dt, our_dt))

    return our_dt


def get_config():
    return {'timezone': 'Europe/London'}

if __name__ == "__main__":
    main()
