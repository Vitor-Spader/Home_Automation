#servidor python teste
import socket

HOST = ''
PORT = 5000
data = ''
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
with s:
    s.bind((HOST,PORT))
    s.listen(1)
    conn,addr = s.accept()
    print(f"connected by: {addr}")
    data_length0 = (conn.recv(1)).encode('utf-8')
    data_length0 += (conn.recv(1)).encode('utf-8')
    data_length1 = []
    
    print(data_length0)
    for x in range(0,int(data_length0)):
        data_length1.append(conn.recv(1))
    data_length = b''.join(data_length1)
    data_length = data_length.decode('utf-8')
    data1 = []
    data = b''
    print(data_length)
    for x in range(0,int(data_length)):
        data1.append(conn.recv(1))
        print(data1)
    data = data.join(data1)
    print(data.decode('utf-8'))
    print(data)
    conn.send(data)
