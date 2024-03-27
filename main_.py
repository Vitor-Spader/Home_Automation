import time,IO as io,timer as timer,server_rp as servidor
from threading import Lock

l_inp = [2]
l_out = [17]

def input_dados():
    return input("Digite o horário que deseja que a luz seja ligada(00:00): ")
# Inicializa IO
gpio = io.IO('BCM',l_inp,l_out)
#Inicializa Função de despertador
time_clock = timer.alarm_clock(gpio,state_active = True)
#Inicializa Servidor
mutex = Lock()
server = servidor.server(gpio,time,mutex)
botao = gpio.verif_in(2)

while True:
    mutex.acquire()
    if gpio.verif_in(2) != botao:
        gpio.switch(17)
        botao = gpio.verif_in(2)
        mutex.release()
    else:
        mutex.release()
        time.sleep(0.1)

gpio.close()

    
    
