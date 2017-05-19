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
# from ics import Calendar

import pytz
import requests

"""
references:
- https://cloud.google.com/translate/docs/reference/libraries#client-libraries-install-python
- https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
- https://en.wikipedia.org/wiki/ICalendar
"""

# def old_main():
#     url = "https://calendar.google.com/calendar/ical/apd9vmbc22egenmtu5l6c5jbfc%40group.calendar.google.com/private-5c6397513ba5958def67f9dde521e6f4/basic.ics" # pylint: disable=line-too-long
#     cal = Calendar(requests.get(url).text)
#     event_list = cal.events.today()
#     print("Found {} events for today".format(len(event_list)))
#     event_name = "Rust Community Team Meeting"
#     event_name = "Rust Utrecht"

#     for e in event_list:
#         if e.name == event_name:
#             local_time = e.begin.to("Europe/London")
#             if e.begin.humanize() == "in an hour":
#                 print("send out reminder!")
#                 print("Event '{}' start {}".format(e.name, e.begin.humanize()))
#                 print("\tlocal begin time: ", local_time)
#                 print("\traw begin {}\n\traw end {}".format(e.begin, e.end))
#             else:

#                 print("\tnot yet time, sleeping...({})".format(local_time.humanize()))


def main_ics():
    # url =
    # "https://calendar.google.com/calendar/ical/apd9vmbc22egenmtu5l6c5jbfc%40group.calendar.google.com/private-5c6397513ba5958def67f9dde521e6f4/basic.ics"
    # # pylint: disable=line-too-long
    url = "http://0.0.0.0:8080/basic.ics"
    cal = Calendar(requests.get(url).text)

    events = cal.events.on("2017-04-19")  # normally .today()
    # events = cal.events.today()
    if len(events) == 0:
        print("no data.")
        return

    for event in events:
        if event.name == "Rust Community Team Meeting":
            print(event.begin, event.begin.humanize())
            # print(event)

# def main_icalendar():
#     # source: http://stackoverflow.com/a/3408488/105282
#     # if you don't want to use icalendar, vobject is another useful one
#     # http://stackoverflow.com/a/6470135/105282
#     calendar_file = os.path.join('dontcommitmebro', 'basic.ics')
#     with open(calendar_file, 'rb') as fp:
#         data = fp.read()

#     cal = icalendar.Calendar.from_ical(data)

#     for comp in cal.walk('vevent'):
#         if comp.decoded('summary') == b'Rust Community Team Meeting':
#             repeat = comp.get('rrule')
#             if repeat is not None:
#                 rule = comp.decoded('rrule')
#             else:
#                 rule = "not supported"


def main_spike():
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
    # main_icalendar()
    # main_ics()
    main_spike()
