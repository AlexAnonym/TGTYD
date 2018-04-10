import threading         #добавляем модуль многопоточности для одновременных приема и передачи
import socket            #добавляем модуль сокетов для коннекта
from datetime import datetime          #добавляем модуль времени 

host_ip = socket.gethostbyname(socket.gethostname())    #получаем свой локальный айпишник
print("This is TELEGRAM THAT YOU'VE DESERVED\nYou're the host with local ip", host_ip, "\nWaiting for connection...")

sock = socket.socket()       #создаем сокет   
sock.bind((host_ip, 9090))      #биндим сервер к нашему локальному айпишнику и порту 9090
sock.listen(1)              #начинаем прослушку с одним возможным подключением
conn, addr = sock.accept()     #подключаемся к клиенту 

print("CONNECTED:", addr, "\nType your message here...")
                                #отсюда и далее так же, как в клиенте
def recieve():
    while True:
        data = conn.recv(1024)
        data_decoded = data.decode()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now, 'Message:', data_decoded)
        
def transmit():
   while True:
        msg = input()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now, 'You:', msg)
        msg_as_bytes = str.encode(msg)
        conn.send(msg_as_bytes)
        
t1 = threading.Thread(target=transmit)
t2 = threading.Thread(target=recieve)
t1.start()
t2.start()
t1.join()
t2.join()
