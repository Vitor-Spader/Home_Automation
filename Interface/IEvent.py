import datetime

class IEvent:
    def __init__(self, _date:datetime.date, _time:datetime.time, _frequency:int, _event):
        pass
    def cancel_event(self):
        pass
    def start_event(self):
        pass  
    def pause_event(self):
        pass
