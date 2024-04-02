from Interface import IEvent
from datetime import datetime
import asyncio

class Event(IEvent.IEvent):
    EVERY_DAY = 1
    EVERY_MONTH = 2
    ON_WEEK_EVERY_DAY = 3
    ON_WEEKEND_EVERY_DAY = 4

    def __init__(self, _date:datetime.date, _time:datetime.time, _frequency:int, _event):        
        self.date = _date if _frequency == 2 else None
        self.time = _time
        self.frequency = _frequency
        self.event = _event 
        self.active = True
    
    def cancel_event(self):
        self.active = False

    async def start_event(self):
        await asyncio.sleep((datetime.combine(self.date, self.time) - datetime.now()).total_seconds())
        if self.active == True:
            self.event()

    def pause_event(self):
        pass