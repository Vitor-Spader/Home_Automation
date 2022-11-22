import RPi.GPIO as GPIO

class IO:
    def __init__(self,mode='BCM',l_inp=[],l_out=[]):
        self.mode = mode
        self.l_inp = l_inp
        self.l_out = l_out

        if mode == 'BCM': GPIO.setmode(GPIO.BCM)
        else: GPIO.setmode(GPIO.BOARD)
        self.setup(self)
    
    def setup(self):
        for x in self.l_inp:
            GPIO.setup(x,GPIO.IN)
        for x in self.l_out:
            GPIO.setup(x,GPIO.OUT)
    
    def verif_in(inp):
        return GPIO.input(inp)
        
    def on(self,out):
        GPIO.output(out, GPIO.LOW)

    def off(self,out):
        GPIO.output(out, GPIO.HIGH)

    def switch(self,out):
        #se a saida estiver acionada desliga
        self.on(out) if GPIO.input(out) == 0 else self.off(out)
    
    def state(self):
        state_list = {'on':[],'off':[]}
        for x in self.l_out:
            if GPIO.input(x) == 0:
                state_list['off'].append(x)
            else: state_list['on'].append(x)
        return state_list

    def close(self):
        GPIO.cleanup()
    def __str__(self) -> str:
        return "IO object"

