import threading
import socket
import time
import Bots
from _thread import *

host = '127.0.0.1'
port = 1235

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []
aliases = []


def broadcast(message, sender):
    for client in clients:
        if client == sender:
            continue
        else:
         client.send(message)

""""
def multi_threaded_client(connection):
        verb = Bots.generate_verb()
        message = f'Host: Do you guys want to {verb} \n'
        connection.send(message.encode('utf-8'))
"""





def handel_client(client):

    while True:
        try:
             #multi_threaded_client(client)
             message = client.recv(1024)
             broadcast(message, client)
             print(message)

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'), client)
            aliases.remove(alias)
            break




def receive():
    while True:
        print("server is running and listning...")
        client, address = server.accept()
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}')
        #start_new_thread(multi_threaded_client, (client, ))
        broadcast(f'{alias} has connected to the chat room'. encode(), client)
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handel_client, args=(client,))
        thread.start()

if __name__ == '__main__':
    receive()