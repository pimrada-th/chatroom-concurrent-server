#Coded by Yashraj Singh Chouhan
import socket, threading, sys
nickname = input("What's your Nickname?: ")
host = '127.0.0.1'                                                     #LocalHost
port = 8899   
user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
user.connect((host, port))                             #connecting user to server

def receive():
    while True:                                                 #making valid connection
        try:
            message = user.recv(1024).decode('utf-8')
            if message == 'NICKNAME': #ส่งแชทส่วนตัว
                user.send(nickname.encode('utf-8'))
            elif message == '#exit' :
                check = input('Do you want to exit this chat room? (y,Y = yes, anything = no): ')
                if(check=='y' or check == 'Y' ): 
                    #user.send('#exit'.encode('utf-8')) 
                    user.close()
                    print("You left from chatroom") 
                    break
                else:
                    print("You back to chat room") 
                    write_thread = threading.Thread(target=write)                   #sending messages 
                    write_thread.start()
                          
            #elif message == '#help' :
                #user.send('#help'.encode('utf-8'))
                #write_thread = threading.Thread(target=write)                   #sending messages 
                #write_thread.start() ##
            else:
                print(message)        
        except :    #case on wrong ip/port details
            print("Sorry, something is error!")  
            user.close()
            break                                             

def write():
    while True:
        typing = input("Typing : ")       
        if typing=='#exit' :
            user.send(typing.encode('utf-8'))
            break     
        #elif typing=='#help':    
            #user.send(typing.encode('utf-8'))                        
        else:
            message = '{}: {}'.format(nickname, typing)          #message layout
            user.send(message.encode('utf-8'))   
        #if typing !='#exit' or typing !='#help' or typing !='#show':
            #message = '{}: {}'.format(nickname, typing)          #message layout
            #user.send(message.encode('utf-8')) 
        #else:
            #user.send(typing.encode('utf-8'))          

#def checkexit(user):


receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)                   #sending messages 
write_thread.start()