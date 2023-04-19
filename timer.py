import IO,time,datetime
from threading import Thread,Lock

class alarm_clock:
    hour = 6
    minute = 0
    state_active = True
    mutex = None

    def __init__(self,gpio,start_time = "6:0",state_active = True):
        if gpio == None: return
        __test_hour(start_time.split(':'))
        self.state_active = state_active
        self.mutex = Lock()
        thread = Thread(target=alarm_clock, args=(self.mutex))
        thread.start()

    def get_state(self):
        return self.state_active

    def set_state(self,state):
        self.state_active = True if state else False
    
    def get_time_clock(self):
        return str(self.horas)+":"+str(self.minutos)

    def set_time_clock(self,time):
        return self.__test_hour(time.split(":"))

    def __test_hour(self,aux_hour,aux_min):
        try:
            aux_hour,aux_min = time.split(":")
            aux_hour = int(aux_hour)
            aux_min  = int(aux_min) 

            if not(aux_hour < 24 and aux_hour >= 0): return False
            if not(aux_min < 60 and aux_min >= 0): return False
            self.mutex.acquire()
            self.hour   = aux_hour
            self.minute = aux_min
            self.mutex.release()
            return True
        except:
            return False
    def close():
        raise Exception('Close')

    def alarm_clock(self,mutex):
        try:
            while True:
                current_time = datetime.datetime.now()
                mutex.acquire()
                if current_time.hour == self.hour and current_time.minute == self.minute and self.state_active:
                    self.gpio.on()
                mutex.release()
                time.sleep(60)
        except:
            mutex.release()
            return
