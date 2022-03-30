import threading
import socket
import random
import time
import sys




IP_address = str(sys.argv[1])  #provided ip address to connect to
Port = int(sys.argv[2])        # provided port number
name = str(sys.argv[3])        # clients name


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket object

client.connect((IP_address, Port))    # connect client to server


bots = ["sifan", "noah", "miki"]
# list of action verbs
verbs = ["study", "read", "fight", "sleep", "walk", "cry", "travel", "drink", "work", "exercise"]

# chat bot responses
def sifan(verb):
    if verb in verbs:
     responses = [
        "{}: I like {}, lets do it\n".format(name, verb + "ing"),
        "{}: {} sounds fun!!\n".format(name, verb + "ing")
     ]
     return random.choice(responses)
    else:
        return "{}: i don't know what that is, but it's fine with me\n".format(name)


def noah(verb):
    if verb in verbs:
     responses = ["{}: No, i don't want to {}. I think {} is boring\n".format(name, verb, verb + "ing"),
                 "{}: Yes, i love {}, can we also play nintendo after that\n". format(name, verb + "ing")]
     return random.choice(responses)
    else:
        return "{}: No, what the hell is that?\n".format(name)

def miki(verb):
    if verb in verbs:
        responses = ["{}: Sure, i am not that exited about {}. But we can do it\n".format(name, verb + "ing"),
                     "{}: Really again! Is {} the best suggestion you got?\n".format(name, verb + "ing")]
        return random.choice(responses)
    else:
        return "{}: It is all good, i like adventure.".format(name)


def client_receive():
    while True:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(name.encode('utf-8'))
            else:
             if ":" in message:
                msgsplit = message.split(": ")

                if msgsplit[0] not in bots:
                    word = ""
                    i = 0;
                    while i < len(verbs):
                        if verbs[i] in message.lower():
                            word = verbs[i]

                        i+=1
                    response =""
                    if name.lower() == "sifan":
                        response=sifan(word)

                    elif name.lower() == "noah":
                        response = noah(word)

                    elif name.lower() == "miki":
                        response = miki(word)

                    print(message)
                    client_send(response)
                else:
                    time.sleep(0.7)
                    print(message)
             else:
                print(message)




def client_send(message):
   print(message)
   client.send(message.encode('utf-8'))


def hostClient():
    while True:
        try:
            msg = f'{name}: {input()}'
            split = msg.split(": ")
            if split[1].isspace() or split[1] == "":
                print("Can't send an empty string. Please write something!")
                continue
            else:
                time.sleep(0.4)
                print(msg)
                client.send(msg.encode('utf-8'))
        except:
            print("\nYou have left the chat room\n")
            sys.exit()
            break



receive_thread = threading.Thread(target= client_receive)
receive_thread.start()

if name not in bots:
 host_thread = threading.Thread(target= hostClient())
 host_thread.start()


