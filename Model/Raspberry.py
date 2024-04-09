import RPi.GPIO as GPIO
import time
import datetime
from Interface import IBoard, ILoger

class Raspberry(IBoard.IBoard):

    def __init__(self, _mode='BCM', _list_input=[], _list_output=[], _list_relationship=[], _loger:ILoger.ILoger=ILoger.ILoger()):
        self.list_input = _list_input
        self.list_output = _list_output
        self.list_relationship = _list_relationship
        self.loger = _loger
        self.last_updated_state = datetime.datetime.now()

        if _mode == 'BCM': GPIO.setmode(GPIO.BCM)
        else: GPIO.setmode(GPIO.BOARD)
        self.__setup_IO__()
        self.list_input_state = {id:GPIO.input(id) == 1 for id in self.list_input}
        self.add_callback(self.callback)
    
    def __setup_IO__(self):
        GPIO.setup(self.list_input,GPIO.IN)
        GPIO.setup(self.list_output,GPIO.OUT, initial=GPIO.HIGH)
    
    def add_callback(self, callback):
        GPIO.add_event_detect(self.list_input[0], GPIO.BOTH, callback=callback, bouncetime=200)

    def callback(self,_id):
        time.sleep(0.001)
        if self.list_input_state[_id] != self.get_state(_id):
            self.list_input_state[_id] = not self.list_input_state[_id]
            self.switch(self.list_relationship[_id])
        print(_id)
        print('callback')

    def set_on(self, _id) -> None:
        self.loger.write_log(f'set_on {_id}')
        GPIO.output(_id, GPIO.LOW)

    def set_off(self, _id) -> None:
        GPIO.output(_id, GPIO.HIGH)

    def get_state(self, _id:int) -> bool:
        print(_id)
        if abs(datetime.datetime.now() - self.last_updated_state) > datetime.timedelta(minutes=30):
            self.list_input_state = {id:GPIO.input(id) == 1 for id in self.list_input}

        return self.list_input_state[_id]

    def get_mode(self, _id) -> str:
        return 'Input' if _id in self.list_input else 'Output'

    def switch(self, _id:list) -> None:
        for id in _id:
            self.set_on(id) if self.get_state(id) else self.set_off(id)

    def set_input(self, _id:int) -> bool:
        try:
            self.list_input.append(
                                    self.list_output.pop(
                                                            self.list_output.index(_id)
                                                        )
                                  )
        except:
            return False
        self.__setup_IO__()
        return True

    def set_output(self, _id:int) -> None:
        try:
            self.list_output.append(
                                    self.list_input.pop(
                                                            self.list_input.index(_id)
                                                        )
                                  )
        except:
            return False
        self.__setup_IO__()
        return True

    def list_input(self) -> list:
        return self.list_input

    def list_output(self) -> list:
        return self.list_output

    def close(self):
        GPIO.cleanup()
