from ics import Calendar
import  requests

"""
references:
- https://cloud.google.com/translate/docs/reference/libraries#client-libraries-install-python
- https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
- https://en.wikipedia.org/wiki/ICalendar
"""

def old_main():
    url = "https://calendar.google.com/calendar/ical/apd9vmbc22egenmtu5l6c5jbfc%40group.calendar.google.com/private-5c6397513ba5958def67f9dde521e6f4/basic.ics" # private 
    c = Calendar(requests.get(url).text)
    event_list = c.events.today()
    print("Found {} events for today".format(len(event_list)))
    event_name = "Rust Community Team Meeting"
    event_name = "Rust Utrecht"
    
    for e in event_list:
        if e.name == event_name:
            local_time = e.begin.to("Europe/London")
            if e.begin.humanize() == "in an hour":
                print("send out reminder!")
                print("Event '{}' start {}".format(e.name, e.begin.humanize()))
                print("\tlocal begin time: ", local_time)
                print("\traw begin {}\n\traw end {}".format(e.begin, e.end))
            else:

                print("\tnot yet time, sleeping...({})".format(local_time.humanize()))

if __name__ == "__main__":
    old_main()
