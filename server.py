import threading
import socket
import time
import sys


host = '127.0.0.1'
port = int(sys.argv[1])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []                                                                   # list of clients
aliases = []                                                                   # list of clients names

# function for broadcasting message to clients except the sender
def broadcast(message, sender):
    for client in clients:
        if client is sender:
            continue
        else:
            client.send(message)




# function for handling clients communication
def handel_client(client):
    while True:
        try:
             message = client.recv(1024)
             receivedmsg = message.decode().split(": ")

             if (receivedmsg[1] == "QUIT"):                                   # message from host shutting down the chatroom
                 #time.sleep(1)
                 print("Disconnecting clients")
                 for i in clients:
                     i.close()                                                #Clossing every clients socket
                 print("server is running and listning...")
                 exit()
             else:
                 time.sleep(0.5)                                          # if message is not shutdown,
                 broadcast(message, client)                               # wait and forward all messages to all clients


        except:                                                           # drop client
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'), client)
            aliases.remove(alias)
            break



# connects incoming clients to the chat room
def receive():
    while True:
        print("server is running and listning...")
        client, address = server.accept()                                   # accepts connection and saves the client
        print(f'connection is established with {str(address)}')             # object in client and its ip and port in address
        client.send('alias?'.encode('utf-8'))                               # asks for the name of connected client
        alias = client.recv(1024)                                           # receives and adds name and client
        aliases.append(alias)                                               # to name list and client list
        clients.append(client)
        print(f'The alias of this client is {alias}')                       # inform what client just got connected
        broadcast(f'{alias} has connected to the chat room'. encode(), client)    # broadcast that to all connected clients
        client.send('you are now connected!'.encode('utf-8'))
        thread = threading.Thread(target=handel_client, args=(client,))
        thread.start()                                                      # start a thread for the client

if __name__ == '__main__':
    receive()                                                               # run receive function