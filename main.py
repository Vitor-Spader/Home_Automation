import time,datetime,sys,socket,threading,IO

botao = IO.start()
#global var
horas = "6"
minutos = "0"
horario_t = "6:0"
state_timer = True



def time_clock(var1,var2):
    global horas, minutos,horario_t
    horas = var1
    minutos = var2
    horario_t = str(var1)+":"+str(var2)

def server():
    HOST = ''
    PORT = 50000
    try:
        while True:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(10)
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
        reborn()
        return -1

def reconect(s):
    s.bind(('',50000))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('connected byy: ', addr)

def reborn():
    global t
    t = threading.Thread(target=server,args=())
    t.start()
        

t  = threading.Thread(target=server,args=())
t.start()


try:
    while True:
        hora = datetime.datetime.now()

        if hora.hour == int(horas) and hora.minute == int(minutos) and state_timer:
            IO.on()
            time.sleep(60)
        elif IO.verif_in(2) and botao:
            botao = False
            IO.switch()
        elif not IO.verif_in(2) and not botao:
            botao = True
            IO.switch()
        else: time.sleep(0.02) 

except KeyboardInterrupt:
    IO.close()
    t.join()
    sys.exit(0)

