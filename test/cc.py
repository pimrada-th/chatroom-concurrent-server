import socket, threading, datetime

date = datetime.datetime.now()
timenow = date.strftime('%X')
def menulist():
    print("""
********************************** Welcome to Mara's Chatroom *********************************
            These are command that you can use in Chatroom
            #show or #s- For show all online users
            #dm - Difect message to user 
            Dm's Syntax: #dm[nicknameTarget],[your message] Example: #dmken,Hi
            #help or #h - Show all menu
            #exit or #e- Exit from this Chatroom
********************************* Hope you enjoy with my program! *****************************""")

menulist()
while True:
    nickname = input("What's your Nickname?: ")
    if nickname == '#show' or nickname == '#s' or nickname == '#help' or nickname == '#h' or nickname == '#exit' or nickname == '#e' or '#' in nickname: #check name
         print("You can't use command and # to be name, Please try again")              
    else:
        host = '127.0.0.1'                                                     #LocalHost
        port = 8899   
        user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
        user.connect((host, port))                                      #connecting user to server
        break    

def receive():
    while True:                                                 #making valid connection
        try:
            message = user.recv(1024).decode('utf-8')
            if message == 'NICKNAME': #ถ้า NICKNAME ตรงก็ให้ส่งชื่อไปที่เซิฟ
                user.send(nickname.encode('utf-8')) #send nick name
            
            elif "You dm to" in message:
                print(message)
                msgcut = message.split('to ') #cut message result = ['You dm ', 'nickname etc']
                cutname = msgcut[1].split(' [')  #cutname result =['nickname', 'etc']
                receivername = cutname[0]
                #cutwords = cutname[1].split('# ')
                #words = cutwords[1]
                #print(msgcut)
                #print(cutwords)
                #print(words)
                #typing = input('Typing to {} : '.format(receiverNickname))
                #user.send("#dm{},{}".format( receiverNickname,typing).encode('utf-8'))
                typing = input('Typing to {} : '.format(receivername))
                if '#b2c' not in typing:    
                    user.send("#dm{},{}".format(receivername,typing).encode('utf-8'))              
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
                        if '#b2c' in typing:
                            print("You can\'t type command #b2c in message!!")
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


