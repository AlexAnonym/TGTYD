import threading            # добавляем модуль многопоточности для одновременных приема и передачи
import socket               # добавляем модуль сокетов для коннекта
import rsa                  # добавляем модуль rsa для шифрования
from datetime import datetime       # добавляем модуль времени

print("This is TELEGRAM THAT YOU'VE DESERVED. You're the client")   # выводим надпись на экран
client_pubkey, client_privkey = rsa.newkeys(1024)    # генерируем пару ключей

sock = socket.socket()      # создаем сокет
print("Type IP ('127.0.0.1' or 'localhost' in order to connect to localhost):")  # выводим надпись на экран
ip = input()                # вводим айпи сервера
sock.connect((ip, 9090))    # коннектимся к серверу


def key_exchange():         # реализуем обмен публичными ключами
    # поскольку публичный ключ - дискретный объект, то просто передать или преобразовать
    # в двоичный код его не получится
    nnn = str(getattr(client_pubkey, 'n'))   # поэтому сначала мы извлекаем атрибуты
    eee = str(getattr(client_pubkey, 'e'))   # публичного ключа
    # в этот момент запущенный сервер принимает данные
    nnn1 = str.encode(nnn)   # здесь мы кодируем первый атрибут в двоичный код
    sock.send(nnn1)   # и передаём его

    server_pubkey_n = sock.recv(1024)    # здесь получаем первый аттрибут от сервера
    server_pubkey_n_str = server_pubkey_n.decode()    # декодируем в строку из двоичного кода
    nn = int(server_pubkey_n_str)   # переводим его в целое число

    eee1 = str.encode(eee)  # проделываем то же самое со вторым атрибутом
    sock.send(eee1)

    server_pubkey_e = sock.recv(1024)
    server_pubkey_e_str = server_pubkey_e.decode()
    ee = int(server_pubkey_e_str)

    global server_pubkey                          # полученный ключ должен быть глобальной переменной
    server_pubkey = rsa.key.PublicKey(nn, ee)     # создаём ключ с переданными нам атрибутами

key_exchange()     # обмениваемся ключами
print("CONNECTED", "\nThe encryption key is successfully received!", "\nType your message here...")


def receive():          # функция приёма сообщения
    while True:         # цикл приёма сообщения
        data = sock.recv(1024)      # принимаем дискретный пакет данных
        data_encrypted = rsa.decrypt(data, client_privkey)    # расшифровываем приватным ключом
        data_decoded = data_encrypted.decode()                # декодируем
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    # запрашиваем текущие дату и время
        print(now, 'Message:', data_decoded)        # высвечиваем дату, время и сообщение


def transmit():         # функция отправки сообщения
   while True:          # цикл отправки сообщения
        msg = input()       # вводим сообщение
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    # запрашиваем текущие дату и время и задаём их формат
        print(now, 'You:', msg)       # выводим время и то, что написали
        msg_as_bytes = str.encode(msg)        # кодируем из строчного формата в битовый
        msg_crypto = rsa.encrypt(msg_as_bytes, server_pubkey)   # зашифровываем публичным ключом
        sock.send(msg_crypto)             # отсылаем сообщение
      
t1 = threading.Thread(target=transmit)      # создаем потоки
t2 = threading.Thread(target=receive)
t1.start()                                  # запускаем потоки
t2.start()
t1.join()                                   # объединяем потоки
t2.join()
