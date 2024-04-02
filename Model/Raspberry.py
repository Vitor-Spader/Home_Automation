import RPi.GPIO as GPIO
from Interface import IBoard

class Raspberry(IBoard.IBoard):

    def __init__(self, _mode='BCM', _list_input=[], _list_output=[], _list_relationship=[]):
        self.list_input = _list_input
        self.list_output = _list_output
        self.list_relationship = _list_relationship

        if _mode == 'BCM': GPIO.setmode(GPIO.BCM)
        else: GPIO.setmode(GPIO.BOARD)
        self.__setup_IO__()
        self.add_callback(self.callback)
    
    def __setup_IO__(self):
        GPIO.setup(self._list_input,GPIO.IN)
        GPIO.setup(self._list_output,GPIO.OUT, initial=GPIO.HIGH)
    
    def add_callback(self, callback):
        GPIO.add_event_detect(self.list_input, GPIO.RISING, callback=callback)

    def callback(self):
        self.switch(self.list_output)

    def set_on(self, _id:list) -> None:
        GPIO.output(_id, GPIO.LOW)

    def set_off(self, _id:list) -> None:
        GPIO.output(_id, GPIO.HIGH)

    def get_state(self, _id:list) -> bool:
        return GPIO.input(_id) == 1

    def get_mode(self, _id) -> str:
        return 'Input' if _id in self.list_input else 'Output'

    def switch(self, _id:list) -> None:
        for channel in _id:
            self.set_on(list(channel)) if get_state(list(channel)) else self.set_off(list(channel))

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