#Coded by Yashraj Singh Chouhan
import socket, threading, sys, datetime, pickle

date = datetime.datetime.now()
timenow = date.strftime('%X')
def menulist():
    print("""
        ******** Welcome to Mara's Chatroom ********
            These are command that you can use in Chatroom
            #show or #s- for show all online users
            #nickname - direct message Example : #ken = direct message to Ken
            #chatroom - back to chatroom
            #help or #h - show all menu
            #exit or #e- exit from this Chatroom
        ******** Hope you enjoy with my program! ********""")

menulist()
while True:
    nickname = input("What's your Nickname?: ")
    if nickname == '#show' or nickname == '#s' or nickname == '#help' or nickname == '#h' or nickname == '#show' or nickname == '#exit' or nickname == '#e': #check name
         print("You can't use command to be name, Please try again")              
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
            #elif message == 'SHOW':
                #listnames = pickle.loads(message)
                #listnames = eval(message)
                #print('Online users now : '+listnames)
                #receive_thread = threading.Thread(target=receive) 
                #receive_thread.start()  
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
                receive_thread = threading.Thread(target=receive)                  #sending messages 
                receive_thread.start()     
        
        elif typing == '#help' or typing == '#h':
            menulist()
            receive_thread = threading.Thread(target=receive)                  #sending messages 
            receive_thread.start()   
        
        elif typing == '#show' or typing == '#s':     
            user.send('#show'.encode('utf-8'))
            print("--- Online Users ---")
            receive_thread = threading.Thread(target=receive)                  #sending messages 
            receive_thread.start()   
        else:
            message = '{} [{}]: {}'.format(nickname, timenow, typing)          #message layout
            user.send(message.encode('utf-8'))   

receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)                   #sending messages 
write_thread.start()