import socket,threading,IO
class server_tcp:
    def __init__(self,HOST: str,PORT: int,gpio,timer):
        self.HOST = HOST
        self.PORT = PORT
        self.gpio = gpio
        self.close = False
        self.timer = timer
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.thread_server = threading.Thread(target=self.server)
        self.thread_server.start()

    def server(self):
        with self.s: 
            self.s.bind((self.HOST,self.PORT))
            while True:
                self.s.listen(1)
                if self.close: return 0 
                conn, addr = self.s.accept()
                print('connected by: ', addr)
                while True:
                    if self.close: return 0
                    data = conn.recv(20)
                    conn.send(data)
                    data = data.decode('utf-8')
                    
                    if 'GET' in data:
                        if 'all' in data:
                            list_state = self.gpio.state()
                            conn.send('on'.encode('utf-8'))
                            data = conn.recv(1024)
                            data = ''
                            for x in list_state['on']:
                                data = str(x) + ','
                            conn.send(data.encode('utf-8'))
                        elif  'out' in data:
                            pass
                        elif 'in' in data:
                            pass
                        elif 'alarm' in data:
                            pass
                        else: 
                            data = ''
                            continue
                    elif 'SET' in data:
                        if 'out' in data:
                            if 'on' in data:
                                data = data.replace('SET out','')
                                data = data.replace('on','')
                                self.gpio.on(int(data))
                                data = ''
                            else:
                                data = data.replace('SET out','')
                                data = data.replace('off','')
                                self.gpio.off(int(data))
                                data = ''
                        elif 'alarm' in data:
                            pass
                        elif 'shutdown':
                            pass
                        else :
                            data = ''
                            continue
                    elif 'CLOSE' in data:
                        break
                    
    def close_thread(self):
        self.close = True