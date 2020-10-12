nickname = 'mara'
typing = input("Typing : ")       
if typing == '#dm'+nickname:
    print('yes')
print (typing+nickname)

#name = typing.split("#dm")
#namestr = str(name[1])
#if namestr in nickname:
    #print('yes')
#else:
    #print('no')

#You dm to m [23:03:54]: sd
#msg = "#dmmara,hello jiadj ok"
#msgcut = msg.split('#dm') #['','message']
#cutwords = msgcut[1].split(',')
#cutwords2 = msg.split(',')
msg = "You dm to m [23:03:54]#sd"
msgcut = msg.split('to ') #cut1 ['You dm ', 'm [23:03:54]# sd']
cutname = msgcut[1].split(' [')  #cutnickname ['m', '23:03:54]# sd']
cutwords2 = cutname[1].split('#') #cutyime and msg['23:03:54]', ' sd']
print(msgcut)
print(cutname)
print(cutwords2)
if '#dm'+nickname in msg :
    print ('itin')
else:
    print('itnot')