import socket,threading
class server_tcp:
    def __init__(self,HOST: str,PORT: int,gpio,close,timer):
        self.HOST = HOST
        self.PORT = PORT
        self.gpio = gpio
        self.close = close
        self.timer = timer
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.thread_server = threading.Thread(target=self.server)
        self.thread_server.start()

    def server(self):
        with self.s:
            self.s.bind((self.HOST,self.PORT))
            self.s.listen(1)
            if self.close: return 0 
            conn, addr = self.s.accept()
            print('connected by: ', addr)
            while True:
                if self.close: break
                data = conn.recv(1024)
                conn.send(data)
                data = data.decode('utf-8')
                
                if 'GET' in data:
                    if 'all' in data:
                        list_state = gpio.state()
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
                            print(data)
                            self.gpio.on(int(data))
                        else:
                            data = data.replace('SET out','')
                            data = data.replace('off','')
                            print(data)
                            self.gpio.on(int(data))
                    elif 'alarm' in data:
                        pass
                    elif 'shutdown':
                        pass
                    else :
                        data = ''
                        continue
    def close(self):
        self.close = True