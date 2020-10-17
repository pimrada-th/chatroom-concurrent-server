import socket, threading, datetime,random                          #Libraries import

host = '127.0.0.1'                                                      #LocalHost
port = 8899   
users = []
nicknames = []                                                         #Choosing unreserved port
date = datetime.datetime.now()
timenow = date.strftime("%X")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()
print(date.strftime("%c"))
print ("Mara's Chatroom server is working!")
print("Waiting for connection\n")

def broadcast(message):                                                 #broadcast function declaration
    for user in users:
        user.send(message) 

def removeuser(user):
    index = users.index(user)
    users.remove(user)
    user.close()
    words = '\n{} Nickname : {} disconnected!\n'.format(date.strftime("%X"),nickname).encode('utf-8')
    print(str(words, 'utf-8')) #convert byte tostring
    broadcast('\n{} left!\n'.format(nickname).encode('utf-8'))
    nickname = nicknames[index]
    nicknames.remove(nickname)    

def dm(user,msg):
    splitmsg= msg.split("#dm") #result = ['','nickname,message']
    splitNameAndWords = splitmsg[1].split(',') #result = ['nickname','words']
    recievername = str(splitNameAndWords[0]) #result = nickname
    words = str(splitNameAndWords[1]) #result = words
    if recievername in nicknames:
        index = nicknames.index(recievername) #find index of recievername
        reciever = users[index] #set receiver address
        sindex = users.index(user)
        sendername = nicknames[sindex]
        sendermsg = 'You dm to {} [{}]# {}'.format(recievername,date.strftime("%X"),words)
        receivermsg = '{} dm to you [{}]: {}'.format(sendername,date.strftime("%X"),words)
        user.send(sendermsg.encode('utf-8'))
        reciever.send(receivermsg.encode('utf-8'))
        print(str(sendermsg))
        print(str(receivermsg))
    else:
        user.send("Sorry, We did't find {} !".format(recievername).encode('utf-8'))        

def userdtails(user,msg):
    index = users.index(user) #find index of recievername
    userindex = users[index]            #go user index
    username = nicknames[index]
    userdata = userindex.getpeername() #get IP and connecting port
    user.send('Your nickname : {}\nYour connection details : {}\n'.format(username,userdata).encode('utf-8'))

def handle(user):                                         
    while True:
        try:    
            message = user.recv(1024) #recieving valid messages from user
            msg = (str(message, 'utf-8'))
            if msg=='#exit':
                removeuser(user)
                break

            elif msg=='#show':
                listnames = "\n".join(nicknames)
                user.send(listnames.encode('utf-8'))
                thread = threading.Thread(target=handle, args=(user,))
                thread.start()
                break
            
            elif msg == '#me':
                userdtails(user,msg)
                thread = threading.Thread(target=handle, args=(user,))
                thread.start()
                break

            elif '#dm' in msg:
                dm(user,msg)
                thread = threading.Thread(target=handle, args=(user,))
                thread.start()
                break
            
            else:
                broadcast(message)
                print(msg) #convert byte tostring 
    
        except:                                                         #ex. user closed window
            removeuser(user)
            break


def appendnickname(user,address,nickname):
    if nickname in nicknames:
        rd = random.randint(5,99)
        number = str(rd)
        nickname = nickname+number
        nicknames.append(nickname)
        users.append(user)
        print("\n{} Nickname : {} ".format(date.strftime("%X"),nickname))                        #send in server
        print("Connected with {}\n".format(str(address))) 
        msg = 'Your new nickname is {}'.format(nickname)
        user.send(msg.encode('utf-8'))
        user.send('Connected to server! Let\'s chat!\n'.encode('utf-8'))
        broadcast("{} joined!".format(nickname).encode('utf-8')) 
        thread = threading.Thread(target=handle, args=(user,))
        thread.start()              
    else:    
        nicknames.append(nickname)
        users.append(user)
        print("\n{} Nickname : {} ".format(date.strftime("%X"),nickname))                        #send in server
        print("Connected with {}\n".format(str(address)))               #send in server
        user.send('Connected to server! Let\'s chat!\n'.encode('utf-8'))  #send for user
        broadcast("{} joined!".format(nickname).encode('utf-8')) 
        thread = threading.Thread(target=handle, args=(user,))
        thread.start()            #brodcast to all users


def acceptuser():   
    try:                                                       
        while True:                                                         #accepting multiple users
            user, address = server.accept() 
            user.send('NICKNAME'.encode('utf-8'))   
            nickname = user.recv(1024).decode('utf-8')
            appendnickname(user,address,nickname)
    except socket.error:
        print("Sorry, Socket error")
acceptuser()


