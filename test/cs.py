import socket, threading, datetime,logging                                          #Libraries import
host = '127.0.0.1'                                                      #LocalHost
port = 8899                                                            #Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()

location = (host, port)
checkstatus = server.connect_ex(location)                               #check that port is using or not
date = datetime.datetime.now()
if checkstatus != 0:
    print(date.strftime("%c"))
    print ("Mara's Chatroom server is working!")
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
    words = '{} Nickname : {} disconnected!\n'.format(date.strftime("%X"),nickname).encode('utf-8')
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

            elif msg=='#show':
                listnames = "\n".join(nicknames)
                user.send(listnames.encode('utf-8'))
                thread = threading.Thread(target=handle, args=(user,))
                thread.start()
                break

            elif '#dm' in msg:
                splitmsg= msg.split("#dm") #result = ['','nickname,message']
                splitNameAndWords = splitmsg[1].split(',') #result = ['nickname','words']
                nickname = str(splitNameAndWords[0]) 
                words = str(splitNameAndWords[1]) 
                if nickname in nicknames:
                    print(nickname)
                    print('inlist')
                    print(users)
                    print(nicknames)
                    index = nicknames.index(nickname) #find index of nickname
                    reciever = users[index] #set receiver address
                    sindex = users.index(user)
                    sendername = nicknames[sindex]
                    print('The index of sender nicknames:', sindex)
                    print('The index of receiver nicknames:', index)
                    #ipsender = user.getpeername()
                    #ipreciever = users[index].getpeername() #get peername = get ip address
                    user.send('You dm to {} [{}]: {}'.format(nickname,date.strftime("%X"),words).encode('utf-8'))
                    #print('Sender : ',ipsender)
                    #print('Receiver : ',ipreciever)
                    #user.send('You\'re chatting with {} now!\ninput #e or #exit for back to main chatroom'.format(msg).encode('utf-8'))
                    dm = '{} dm to you [{}]: {}'.format(sendername,date.strftime("%X"),words)
                    reciever.send(dm.encode('utf-8'))
                    thread = threading.Thread(target=handle, args=(user,))
                    thread.start()
                else:
                    user.send("Sorry, We did't find {} !".format(msg).encode('utf-8'))        
                    thread = threading.Thread(target=handle, args=(user,))
                    thread.start()
                break
            else:
                broadcast(message)
                print(msg) #convert byte tostring 
    
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
            print("\n{} Nickname : {} ".format(date.strftime("%X"),nickname))                        #send in server
            print("Connected with {}\n".format(str(address)))               #send in server
            user.send('Connected to server! Let\'s chat!'.encode('utf-8'))  #send for user
            broadcast("{} joined!".format(nickname).encode('utf-8'))        #brodcast to all users
            thread = threading.Thread(target=handle, args=(user,))
            thread.start()
    except socket.error:
        print("Shutting down")
    finally:
        user.close() 
acceptuser()


        
