import  RPi.GPIO as GPIO
import time
import datetime
import sys
import socket 
import threading 

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(2, GPIO.IN)
#global var
horas = "6"
minutos = "0"
horario_t = "6:0"
state_timer = True
#conexao = False

# flag 1 = off , flag 2 = on, flag 3 = on by time
def time_clock(var1,var2):
    global horas, minutos,horario_t
    horas = var1
    minutos = var2
    horario_t = str(var1)+":"+str(var2)

#def timeout():
    #global conexao
    #for x in range(120):
        #time.sleep(1)
        #if not conexao:
            #return -1
    #s.close()
    #reborn()

def server():
    global conexao
    HOST = ''
    PORT = 50000
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST,PORT))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                print('connected by: ', addr)
                #conexao = True
                #t = threading.Thread(target=timeout(),args=())
                #t.start()
                while True:
                    data = conn.recv(1024)
                    if not data: time.sleep(1)
                    conn.sendall(data)
                    #ligar luz
                    if data.decode("utf-8") == "on":
                        on()
                        data = ''
                    #desligar luz
                    elif data.decode("utf-8") == "off":
                        off()
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
                        conexao = False
                        s.bind(('',50000))
                        s.listen(1)
                        conn, addr = s.accept()
                        with conn:
                            print('connected byy: ', addr)
    except KeyboardInterrupt:
        print("Thread finished -1")
        s.close()
        return -1
    except OSError:
        print("OSError")
        s.close()
        reborn()
        return -1

def reborn():
    t = threading.Thread(target=server,args=())
    t.start()
        
def on():
    GPIO.output(17, GPIO.LOW)
    time.sleep(0.01)
def off():
    GPIO.output(17, GPIO.HIGH)
    time.sleep(0.01)

t  = threading.Thread(target=server,args=())
t.start()

def switch():
    #se a saida estiver acionada desliga
    if GPIO.input(17) != 0: on()

    else: off()

botao = (True if GPIO.input(2) == 0 else False)
try:
    while True:
        hora = datetime.datetime.now()

        if hora.hour == int(horas) and hora.minute == int(minutos) and state_timer:
            on()
            time.sleep(60)
        elif GPIO.input(2) == 0 and botao:
            botao = False
            switch()
        elif GPIO.input(2) != 0 and not botao:
            botao = True
            switch()
        else: time.sleep(0.02) 

except KeyboardInterrupt:
    GPIO.cleanup()
    t.join()
    sys.exit(0)

