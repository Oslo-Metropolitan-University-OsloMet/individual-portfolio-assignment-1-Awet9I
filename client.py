import threading
import socket
import Bots
import sys




IP_address = str(sys.argv[1])  #provided ip address to connect to
Port = int(sys.argv[2])        # provided port number
name = str(sys.argv[3])        # clients name


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket object

client.connect((IP_address, Port))                          # connect client to server




def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'alias?':
             client.send(name.encode('utf-8'))
            else:
               print(message)
               return message
        except:
          print('Error!')
          client.close()
          break

def host(message):
    while True:
        client_receive()
        #verb = Bots.generate_verb()
        #message = f'{name}:Do you want to {verb} \n'
        client.send(message.encode('utf-8'))
        print(message)
        data = client_receive()
        if not data:
            continue


def alice():
    while True:
        data = client_receive()
        if not data:
            continue
        words = data.split()
        index = len(words) - 1
        verb = words[index]
        res = Bots.alice(verb)
        message = f'{name}:{res} \n'
        client.send(message.encode('utf-8'))
        print(message)


def client_send():
 n = 4
 while n > 0:

  if name == "Host":
    while True:
     message = input("put you suggestion here")
     client.send(message.encode('utf-8'))
     print(message)
     data = client_receive()
     if not data:
         continue

  elif name == "Alice":
     alice()

  n = n - 1






receive_thread = threading.Thread(target= client_receive)
receive_thread.start()

send_thread = threading.Thread(target= client_send)
send_thread.start()


if __name__ == '__main__':
    client_receive()
    client_send()
