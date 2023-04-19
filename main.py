import time,datetime,socket,threading,IO,timer

l_inp = [2]
l_out = [17]

# Inicializa IO
gpio = IO('BCM',l_inp,l_out)
#Inicializa Função de despertador
time = timer.alarm_clock(gpio,input_dados(),True)
#Inicializa Servidor
mutex = Lock()
t0  = threading.Thread(target=server,args=(mutex))
t0.start()

while True:
    mutex.acquire()
    if gpio.verif_in(2) and botao:
        botao = False
        IO.switch()
    elif not gpio.verif_in(2) and not botao:
        botao = True
        IO.switch()
    else: time.sleep(0.02)
    mutex.release() 


t.join()
gpio.close()

def input_dados():
    return input("Digite o horário que deseja que a luz seja ligada(00:00): ")
    
    