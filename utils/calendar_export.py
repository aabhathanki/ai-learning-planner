from ics import Calendar, Event
from datetime import datetime, timedelta

def create_calendar(plan):

    cal = Calendar()
    start = datetime.now()

    for day in plan["daily_plan"]:
        event = Event()
        event.name = day["title"]
        event.begin = start + timedelta(days=day["day"] - 1)
        event.duration = timedelta(hours=2)
        cal.events.add(event)

    return cal