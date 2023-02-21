import time,alarm_clock,server_rp,threading,IO as io
#list of inputs/buttons
l_inp = [2]
#list of outputs
l_out = [17]
#object to treat with input and output
gpio = io.IO('BCM',l_inp,l_out)
#last state of button
#cada entrada deve ter um botao associado ao mesmo
botao = True if gpio.verif_in(2) else False
#object to treat when ligths will turn on
#quais luzes em quais horarios?
timer = alarm_clock.alarm(gpio)
#object to treat te tcp connection
server = server_rp.server_tcp(gpio=gpio,timer=timer,HOST='',PORT=5000)

try:
    #verify if the button switched 
    while True:
        if gpio.verif_in(2) and not botao:
            botao = True
            gpio.switch(17)
        elif not gpio.verif_in(2) and botao:
            botao = False
            gpio.switch(17)
        else: time.sleep(0.02) 
except KeyboardInterrupt:
    #close thread timmer
    timer.close_thread()
    #close thread server
    server.close_thread()
    #cleanup gpio configurat
    gpio.close()
    print("KeyboardInterrupt error!!!")


