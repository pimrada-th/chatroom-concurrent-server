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

msg = "#dmmara,hello jiadj ok"
msgcut = msg.split('#dm') #['','message']
cutwords = msgcut[1].split(',')
cutwords2 = msg.split(',')
print(msgcut)
print(cutwords)
print(cutwords2)
if '#dm'+nickname in msg :
    print ('itin')
else:
    print('itnot')