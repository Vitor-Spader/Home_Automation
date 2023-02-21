import socket

HOST = '10.0.0.101'
PORT = 5000
data = ''

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    print("connected by: "+str(PORT))
    while True:
        choice = input("1-Ligar \n2-Desligar\n3-Sair")
        if choice == '1': 
            s.send('SET out 17 on'.encode('utf-8'))
            data = s.recv(1024)
        elif choice == '2': 
            s.send('SET out 17 off'.encode('utf-8'))
            data = s.recv(1024)
        elif choice == '3':
            s.send('CLOSE'.encode('utf-8'))
            break
        else: 
            print("Digite uma opção válida")
            continue
        print(data)
    s.close()