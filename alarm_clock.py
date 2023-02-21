import time,datetime,threading

class alarm:
    def __init__(self,gpio,horas=6,minutos=0,state_timer=True) -> None:
        self.gpio = gpio
        self.horas = horas
        self.minutos = minutos
        self.state_timer = state_timer
        self.close = False
        self.thread = threading.Thread(target=self.timer)
        self.thread.start()

    def timer(self):
        while True:
            if self.close: return 0
            hora = datetime.datetime.now()
            if hora.hour == self.horas and hora.minute == self.minutos and self.state_timer:
                self.gpio.on()
                time.sleep(60)
            time.sleep(1)
    def close_thread(self):
        self.close = True
    def set_time(self,horas,minutos):
        self.horas = horas
        self.minutos = minutos
    def set_state_timer(self,state_timer):
        self.state_timer = state_timer
    def get_time(self):
        return self.horas,self.minutos
    def get_state_timer(self):
        return self.state_timer
    def __str__(self) -> str:
        return str(self.horas)+":"+str(self.minutos)
    