import RPi.GPIO as GPIO
import time

def start():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(2, GPIO.IN)
    return (True if GPIO.input(2) == 0 else False)

def verif_in(num):
    return (True if GPIO.input(num) == 0 else False) 

def on():
    GPIO.output(17, GPIO.LOW)
    time.sleep(0.01)
def off():
    GPIO.output(17, GPIO.HIGH)
    time.sleep(0.01)
def switch():
    #se a saida estiver acionada desliga
    if verif_in(17) : on()

    else: off()

def close():
    GPIO.cleanup()