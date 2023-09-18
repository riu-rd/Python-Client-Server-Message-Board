# Darius Vincent Ardales    CSNETWK - S12   Client Side
# Project Group 7

import socket
import json

server_addr = socket.gethostname() # '172.16.0.20'
server_port = int(input('Enter port of message board server: ')) # 8107

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# FOR REGISTERING
namecheck = True
while namecheck:
    name = input("\nEnter preferred username: ")
    print('Registering username %s.' % name)

    send = json.dumps({"command":"register", "username":name})
    sock.sendto(send.encode(), (server_addr, server_port))
    data, address = sock.recvfrom(1024) 
    data = json.loads(data.decode())

    if data.get("code_no") == 502:
        print('Username already exists! Try another username.')
    elif data.get("code_no") == 401:
        print('Registered succesfully!')
        namecheck = False
    elif data.get("code_no") == 301:
        print('Command unknown')
    elif data.get("code_no") == 201:
        print('Command parameters incomplete')

# FOR MESSAGES AND DEREGISTERING
deregister = True
while deregister:  
    msg = input("\nEnter message: ")
    
    # MESSAGES
    if msg.upper() != "BYE":
        send = json.dumps({"command":"msg", "username":name, "message":msg})
        sock.sendto(send.encode(), (server_addr, server_port))
        data, address = sock.recvfrom(1024) 
        data = json.loads(data.decode())

        if data.get("code_no") == 501:
            print('User not registered!')
        elif data.get("code_no") == 401:
            print('Message sent succesfully!')
        elif data.get("code_no") == 301:
            print('Command unknown')
        elif data.get("code_no") == 201:
            print('Command parameters incomplete')
    
    # DEREGISTER
    else:
        send = json.dumps({"command":"deregister", "username":name})
        sock.sendto(send.encode(), (server_addr, server_port))
        data, address = sock.recvfrom(1024) 
        data = json.loads(data.decode())
        
        if data.get("code_no") == 501:
            print('User not registered!')
        elif data.get("code_no") == 401:
            print('Disconnecting. . .')
            deregister = False
        elif data.get("code_no") == 301:
            print('Command unknown')
        elif data.get("code_no") == 201:
            print('Command parameters incomplete')
sock.close()