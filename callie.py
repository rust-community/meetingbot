#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This will eventually become a class to identify if there's any work for 
meetingbot to do.
"""
import os
from datetime import datetime, timezone
from dateutil import tz

from icalendar import Calendar

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
            print("dtstart: {}\ndescription: {}".format(
                start_time, comp.get('DESCRIPTION')))

            print(rrule)
            print("--------------")

if __name__ == "__main__":
    main()
