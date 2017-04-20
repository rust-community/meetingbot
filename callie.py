from ics import Calendar
import  requests

"""
references:
- https://cloud.google.com/translate/docs/reference/libraries#client-libraries-install-python
- https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
- https://en.wikipedia.org/wiki/ICalendar
"""

def main():
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
        

def old_main():
    # url = "https://calendar.google.com/calendar/ical/apd9vmbc22egenmtu5l6c5jbfc%40group.calendar.google.com/public/basic.ics" # public
    url = "https://calendar.google.com/calendar/ical/apd9vmbc22egenmtu5l6c5jbfc%40group.calendar.google.com/private-5c6397513ba5958def67f9dde521e6f4/basic.ics" # private 
    c = Calendar(requests.get(url).text)

    when = "20170421 00:00:00" # next weds (nothing)
    when = "20170405 00:00:00" # 1st meeting of the month
    when = "20170419 00:00:00"
    event_list = c.events.on(when) # normally this would .today()
    print("Found {} events for {}".format(when, len(event_list)))
    for e in event_list:
        if e.name == "Rust Community Team Meeting":
            print("Event '{}' started {}".format(e.name, e.begin.humanize()))
            print("\tlocal begin time: ", e.begin.to("Europe/London"))
            print("\traw begin {}\n\traw end {}".format(e.begin, e.end))

    last_event = c.events[-1]
    print("last event: ", last_event.name, last_event.begin.humanize())
    display_eventlist_variations(c)
    # first_twenty(c)

def display_eventlist_variations(c):
    print("total events:", len(c.events))
    today = c.events.today()[0]
    print("today:", today.name)
    print("\tbegin {}\n\tlocal {}\n\thumanize: {}".format(today.begin, today.begin.to("Europe/London"), today.begin.humanize()))
    

def first_twenty(c):
    # first twenty
    for i in range(20):
        e = c.events[i]
        print("Event '{}' started {}".format(e.name, e.begin.humanize()))

if __name__ == "__main__":
    main()