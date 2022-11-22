import time,datetime,socket,threading,IO

l_inp = [2]
l_out = [17]
gpio = IO('BCM',l_inp,l_out)
#global var
horas = "6"
minutos = "0"
state_timer = True



def time_clock(var1,var2):
    global horas, minutos
    return str(horas)+":"+str(minutos)

def server():
    HOST = ''
    PORT = 50000
    while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST,PORT))
                s.listen(1)
                conn, addr = s.accept()
                print('connected by: ', addr)
                
                while True:
                    data = conn.recv(1024)
                    data = data.decode('utf-8')
                    request = data.split(' ')
                    if request[0] == 'GET':
                        #send the state of inputs and outputs
                        if request[1] == 'state':
                            state_list = gpio.state()
                            for k,v in state_list.items():
                                conn.send(k)
                                conn.recv(1024)
                                for x in v:
                                    y = str(x)
                                    conn.send(y.encode('utf-8'))
                                    conn.recv(1024)
                        elif request[1] == 'timer':  
                            time = time_clock()
                            conn.send(time.encode('utf-8'))
                    elif request[0] == 'SET':
                        #turn on output
                        if request[1] == "on":
                            gpio.on(int(request[2]))
                            conn.send(b'100 ok')

                        #turn off output
                        elif request[1] == "off":
                            gpio.off(int(request[2]))
                            conn.send(b'100 ok')

                        elif request[1] == "timer":
                            global state_timer
                            conn.send(b'100 ok')
                            data = conn.recv(1024)
                            data = data.decode('utf-8')
                            request = data.split(' ')
                            if request[0] == 'TRUE':
                                state_timer = True
                                h,m = request[1].split(':')
                                global horas,minutos
                                horas = str(int(h))
                                minutos = str(int(m))
                            else:
                                state_timer = False
        
def timmer(gpio,horas,minutos,state_timer):
    while True:
        hora = datetime.datetime.now()

        if hora.hour == int(horas) and hora.minute == int(minutos) and state_timer:
            gpio.on()
            time.sleep(60)

t0  = threading.Thread(target=server,args=())
t1  = threading.Thread(target=timmer,args=(gpio,horas,minutos,state_timer))
t0.start()
t1.start()


while True:
    ## continue please future vitor
    if gpio.verif_in(2) and botao:
        botao = False
        IO.switch()
    elif not gpio.verif_in(2) and not botao:
        botao = True
        IO.switch()
    else: time.sleep(0.02) 


t.join()
gpio.close()
