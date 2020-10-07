#Coded by Yashraj Singh Chouhan
import socket, threading                                                #Libraries import

host = '127.0.0.1'                                                      #LocalHost
port = 8899                                                            #Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()

location = (host, port)
checkstatus = server.connect_ex(location)                               #check that port is using or not
if checkstatus != 0:
    print ("Chat room server is working!")
    print("Waiting for connecting\n")
else:
    print('Sorry! Server can not run\n')
    

users = []
nicknames = []

def broadcast(message):                                                 #broadcast function declaration
    for user in users:
        user.send(message) 

def removeuser(user):
    index = users.index(user)
    users.remove(user)
    user.close()
    nickname = nicknames[index]
    words = '{} disconnected!\n'.format(nickname).encode('utf-8')
    print(str(words, 'utf-8')) #convert byte tostring
    broadcast('{} left!\n'.format(nickname).encode('utf-8'))
    nicknames.remove(nickname)       

def handle(user):                                         
    while True:
        try:    
            message = user.recv(1024) #recieving valid messages from user
            msg = (str(message, 'utf-8'))  
            if msg=='#exit':
                removeuser(user)
                break
            
            else:
                broadcast(message)
                print(str(message, 'utf-8')) #convert byte tostring   
        except:                                                         #ex. user closed window
            removeuser(user)
            break

def acceptuser():   
    try:                                                       
        while True:                                                         #accepting multiple users
            user, address = server.accept()       
            user.send('NICKNAME'.encode('utf-8'))
            nickname = user.recv(1024).decode('utf-8')
            nicknames.append(nickname)
            users.append(user)
            print("Nickname : {} ".format(nickname))                        #send in server
            print("Connected with {}\n".format(str(address)))               #send in server
            broadcast("{} joined!".format(nickname).encode('utf-8'))        #brodcast to all users
            #user.send('Connected to server! Let\'s chat!'.encode('utf-8'))  #send msg for user
            menulist(user)
            thread = threading.Thread(target=handle, args=(user,))
            thread.start()
    except socket.error:
        print("Shutting down")
    finally:
        user.close()

def menulist(user):
    message = """******** Welcome to Mara's Chatroom ********
            This is command that you can use in Chatroom
            #help - show all menu
            #show - for show all online users
            #exit - exit from this Chatroom
        ******** Hope you enjoy with my program! ********""".encode('utf-8') #Correct place!! of encode
    user.send(message)

        
acceptuser()


        
