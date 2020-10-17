import socket, threading, datetime

nickname = ''
date = datetime.datetime.now()
timenow = date.strftime('%X')

def menulist():
    print("""
********************************** Welcome to Mara's Chatroom *********************************
            These are command that you can use in Chatroom
            #me or #m - For check your nickname and connection details
            #show or #s- For show all online users
            #dm - Difect message to user 
            Dm's Syntax: #dm[nicknameTarget],[your message] Example: #dmken,Hi
            #help or #h - Show all menu
            #exit or #e- Exit from this Chatroom
********************************* Hope you enjoy with my program! *****************************""")
menulist()

while True:
    print("xxx If your name already taken, We will add a random number after your nickname for identify yourself xxx")
    nickname = input("Hi! What's your Nickname?: ")
    if '#' in nickname: #check name
         print("You can't use # in your nickname, Please try again")              
    else:
        host = '127.0.0.1'                                                     #LocalHost
        port = 8899   
        user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
        user.connect((host, port))                                      #connecting user to server
        break    

def receive():
    global nickname
    while True:                                                 #making valid connection
        try:
            message = user.recv(1024).decode('utf-8')
            if message == 'NICKNAME': #ถ้า NICKNAME ตรงก็ให้ส่งชื่อไปที่เซิฟ
                user.send(nickname.encode('utf-8')) #send nick name
            elif "Your new nickname is " in message:
                print(message)
                msgcut = message.split('Your new nickname is ')
                nickname = msgcut[1]
            else:
                print(message)    
        except :    #case on wrong ip/port details
            print("Sorry, something is error!")  
            user.close()
            break                                             

def write():
    while True:
        typing = input("Typing : ")       
        if typing=='#exit' or typing == "#e" :
            check = input('Do you want to exit this chat room? (y,Y = yes, anything = no): ')
            if(check=='y' or check == 'Y' ): 
                user.send('#exit'.encode('utf-8'))         #ถ้าไม่มีมันจะไม่หยุดทำงงาน
                user.close()
                print("You left from chatroom") 
                break
            else:
                print("You back to chat room") 
                receive_thread = threading.Thread(target=receive)                  #recieving messages 
                receive_thread.start()     
        
        elif typing == '#help' or typing == '#h':
            menulist()
            receive_thread = threading.Thread(target=receive)                  #recieving messages 
            receive_thread.start()   
    
        elif typing == '#show' or typing == '#s': 
            user.send('#show'.encode('utf-8'))
            print("--- Online Users ---")
            receive_thread = threading.Thread(target=receive)                  #recieving messages 
            receive_thread.start()   
        
        elif typing == '#me' or typing == '#m': 
            user.send('#me'.encode('utf-8'))
            print("--- Your details ---")
            receive_thread = threading.Thread(target=receive)                  #recieving messages 
            receive_thread.start()   
        
        elif '#dm' in typing:
            if '#dm'+' ' in typing:
                print("Don't spacebar after #dm please")
                receive_thread = threading.Thread(target=receive)                  #recieving messages 
                receive_thread.start()
            else:
                if ',' in typing:
                    if '#dm'+nickname in typing:
                        print("You can\'t dm to yourself!!")
                        receive_thread = threading.Thread(target=receive)                  #recieving messages 
                        receive_thread.start()
                    else:
                        user.send(typing.encode('utf-8'))
                        receive_thread = threading.Thread(target=receive)                  #recieving messages 
                        receive_thread.start()

                else:
                    print("DM syntax must be #dm[nicknameTarget],[your message] Example: #dmken,Hi")
                    receive_thread = threading.Thread(target=receive)                  #recieving messages 
                    receive_thread.start()

        else:
            message = '{} [{}]: {}'.format(nickname, timenow, typing)          #message layout
            user.send(message.encode('utf-8'))   

receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)                   #sending messages to server
write_thread.start()



