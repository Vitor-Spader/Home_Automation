import socket,IO,threading

class server:

    def __init__(self,PORT,HOST,gpio,time):
        self.HOST = HOST
        self.PORT = PORT
        self.gpio = gpio
        self.time = time

    def __init__(self,gpio,time):
        self.HOST = ''
        self.PORT = 123
        self.gpio = gpio
        self.time = time
    def __init_server(self):
        thread_server = threading.Thread(target=rp_server,args=(mutex))
        thread_server.start()

    def __buffer_server(self, conn):
        buffer = ''
        while True:
            data = conn.recv(1)
            if not data:
                return buffer.decode("utf-8").split(' ')
            buffer += data
            
    
    def rp_server(self,mutex):
        try:
            while True:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.bind((HOST,PORT))
                        s.listen(1)
                        conn, addr = s.accept()
                        print('connected by: ', addr)
                        
                        while True:
                            buffer_request = self.__buffer_server(conn)
                            if buffer_request[0] == 'GET':
                                #send the state of inputs and outputs
                                if buffer_request[1] == 'state':
                                    state_list = gpio.state()
                                    #Verificar saida
                                    for k,v in state_list.items():
                                        conn.send(k)
                                        for x in v:
                                            y = str(x)
                                            conn.send(y.encode('utf-8'))
                                elif buffer_request[1] == 'timer':  
                                    conn.send(time.get_time_clock().encode('utf-8'))
                            elif buffer_request[0] == 'SET':
                                #turn on output
                                if buffer_request[1] == "on":
                                    try:
                                        gpio.on(int(buffer_request[2]))
                                        conn.send(b'100 ok')
                                    except:
                                        conn.send(b"101 error")

                                #turn off output
                                elif buffer_request[1] == "off":
                                    try:
                                        gpio.off(int(buffer_request[2]))
                                        conn.send(b'100 ok')
                                    except:
                                        conn.send(b"101 error")

                                elif buffer_request[1] == "timer":

                                    if buffer_request[2] == 'true':
                                        time.set_state(True)
                                        if len(buffer_request) > 2:
                                            time.set_time_clock(buffer_request[3])
                                    else:
                                        time.set_state(True)
        except:
            return