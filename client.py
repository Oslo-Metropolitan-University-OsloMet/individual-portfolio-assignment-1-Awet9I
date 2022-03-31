import threading
import socket
import random
import time
import sys




IP_address = str(sys.argv[1])                                           #provided ip address to connect to
Port = int(sys.argv[2])                                                 # provided port number
name = str(sys.argv[3])                                                 # clients name


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              # socket object

client.connect((IP_address, Port))                                      # connect client to server


bots = ["sifan", "noah", "miki"]                                        #list of bots

# list of action verbs
verbs = ["study", "read", "fight", "sleep", "walk", "cry", "travel", "drink", "work", "exercise"]

"""
chat response generator for sifan bot, that takes in a verb and returns a string formated with the verb
"""
def sifan(verb):
    if verb in verbs:
         responses = [
            "{}: I like {}, lets do it\n".format(name, verb + "ing"),
            "{}: {} sounds fun!!\n".format(name, verb + "ing")
             ]
         return random.choice(responses)

    else: #if provided verb is not in the list of action verbs then respond with this
         return "{}: i don't know what that is, but it's fine with me\n".format(name)



"""
chat response generator for noah bot, that takes in a verb and returns a string formated with the verb
"""
def noah(verb):
    if verb in verbs:
           responses = ["{}: No, i don't want to {}. I think {} is boring\n".format(name, verb, verb + "ing"),
                 "{}: Yes, i love {}, can we also play nintendo after that\n". format(name, verb + "ing")]
           return random.choice(responses)
    else: #if provided verb is not in the list of action verbs then respond with this
        return "{}: No, what the hell is that?\n".format(name)




"""
chat response generator for miki bot, that takes in a verb and returns a string formated with the verb
"""
def miki(verb):
    if verb in verbs:
        responses = ["{}: Sure, i am not that exited about {}. But we can do it\n".format(name, verb + "ing"),
                     "{}: Really again! Is {} the best suggestion you got?\n".format(name, verb + "ing")]
        return random.choice(responses)
    else: #if provided verb is not in the list of action verbs then respond with this
        return "{}: It is all good, i like adventure.".format(name)


"""
A function for receiving message and send appropriate response
"""
def client_receive():
    while True:
        message = client.recv(1024).decode('utf-8')             #receives message
        if message == "alias?":                                 #if the massage is asking for name send name
                client.send(name.encode('utf-8'))
        else:
             if ":" in message:                                 # checks if the message object is a message from clients
                msgsplit = message.split(": ")

                if msgsplit[0] not in bots:                     # checks if message is from host by looking at
                                                                # the first element of split list,
                    word = ""                                   # if the first element is in the bots name list
                    i = 0;
                                                                # then we jump to else,
                    while i < len(verbs):
                        if verbs[i] in message.lower():         # if message is from host we go through the verbs list
                            word = verbs[i]                     # and try to match its elements one by one with the

                        i+=1                                    # message object, if there is a match it is assigned to word variable
                                                                # if there is no match empty string is assigned to word
                    response =""
                    if name.lower() == "sifan":
                        response=sifan(word)                    #word is passed to bot functions

                    elif name.lower() == "noah":
                        response = noah(word)

                    elif name.lower() == "miki":
                        response = miki(word)

                    print(message)                            # message is printed and its response is sent
                    client_send(response)
                else:
                    time.sleep(0.7)                          # if message is from bots it is printed
                    print(message)
             else:
                print(message)                               # if it other text like quit it is printed



# Function for sending message
def client_send(message):
   print(message)
   client.send(message.encode('utf-8'))

# function for handling host client messages
def hostClient():
    while True:
        try:
            msg = f'{name}: {input()}'                     # input message from command line
            split = msg.split(": ")
            if split[1].isspace() or split[1] == "":       # check for empty string
                print("Can't send an empty string. Please write something!")
                continue
            else:
                time.sleep(0.4)                            # wait and send message
                print(msg)
                client.send(msg.encode('utf-8'))
        except:
            print("\nYou have left the chat room\n")      # print this and exit if something goes wrong
            sys.exit()
            break



receive_thread = threading.Thread(target= client_receive)   # receiver thread
receive_thread.start()

if name not in bots:
 host_thread = threading.Thread(target= hostClient())       # thread for host client
 host_thread.start()




