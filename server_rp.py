import socket,time,IO,threading

def server():
    HOST = ''
    PORT = 50000
    try:
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((HOST,PORT))
                    s.listen(1)
                    conn, addr = s.accept()
                    with conn:
                        print('connected by: ', addr)
                        
                        while True:
                            data = conn.recv(1024)
                            if not data: time.sleep(1)
                            conn.sendall(data)
                            #ligar luz
                            if data.decode("utf-8") == "on":
                                IO.on()
                                data = ''
                            #desligar luz
                            elif data.decode("utf-8") == "off":
                                IO.off()
                                data = ''
                            elif data.decode("utf-8") == "timer":
                                global state_timer
                                conn.send(data)
                                print(data)
                                data = ''
                                time.sleep(0.1)
                                if state_timer: conn.send(b"1")
                                else: conn.send(b"0")
                                while True:
                                    data = conn.recv(1024)
                                    if not data: time.sleep(1)
                                    print(data)
                                    if data.decode() == "1":
                                        state_timer = True
                                        break
                                    elif data.decode() == "0":
                                        state_timer = False
                                        break
                            # definir timer
                            elif data.decode("utf-8") == "time":
                                global horario_t
                                conn.sendall(horario_t.encode('utf-8'))
                                while True:
                                    data = conn.recv(1024)
                                    if not data: time.sleep(1)
                                    conn.sendall(data)
                                    horario = data.decode("utf-8")
                                    var1,var2 = horario.split(":")
                                    if var1.isdigit() and var2.isdigit():
                                        if (int(var1) > 0 and int(var1) < 24) and (int(var2) >= 0 and int(var2) < 60):
                                            time_clock(var1,var2)
                                            data = ""
                                            conn.sendall(b'ok')
                                            break
                            elif data.decode("utf-8") == "dsc_off":
                                s.close()
                                break
            except socket.timeout:
                s.close()
                continue
    except KeyboardInterrupt:
        print("Thread finished -1")
        s.close()
        return -1
    except OSError:
        print("OSError")
        s.close()
        main.reborn()
        return -1

def reconect(s):
    s.bind(('',50000))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('connected byy: ', addr)

def reborn():
    t.join()
    t = threading.Thread(target=server,args=())
    t.start()
        
def start():
    t  = threading.Thread(target=server,args=())
    t.start()

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