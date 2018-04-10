import threading            #добавляем модуль многопоточности для одновременных приема и передачи
import socket               #добавляем модуль сокетов для коннекта
from datetime import datetime       #добавляем модуль времени

print("This is TELEGRAM THAT YOU'VE DESERVED. You're the client")

sock = socket.socket()      #создаем сокет
print("Type IP ('127.0.0.1' or 'localhost' in order to connect to localhost):")
ip = input()                #вводим айпи сервера
sock.connect((ip, 9090))    #коннектимся к серверу

print("Type your message here...")

def recieve():          #функция приёма сообщения
    while True:         #цикл приёма сообщения
        data = sock.recv(1024)      #принимаем дискретный пакет данных
        data_decoded = data.decode()    #переводим в строку из битового формата в строчный
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  #запрашиваем текущие дату и время
        print(now, 'Message:', data_decoded)        #высвечиваем дату, время и сообщение
        
def transmit():         #функция отправки сообщения
   while True:          #цикл отправки сообщения
        msg = input()       #вводим сообщение
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  #запрашиваем текущие дату и время и задаём их формат
        print(now, 'You:', msg)     #выводим время и то, что написали
        msg_as_bytes = str.encode(msg)      #кодируем из строчного формата в битовый
        sock.send(msg_as_bytes)             #отсылаем сообщение
      
t1 = threading.Thread(target=transmit)      #создаем потоки
t2 = threading.Thread(target=recieve)       
t1.start()                                  #запускаем потоки
t2.start()
t1.join()                                   #объединяем потоки
t2.join()
