# Darius Vincent Ardales    CSNETWK - S12   Server Side
# Project Group 7

import socket
import json

names = []
listen_addr = socket.gethostname() # '172.16.0.20'
listen_port = 8107

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((listen_addr, listen_port))

print('Starting up on address %s port %d' % (listen_addr, listen_port))
print('\nWaiting to receive message. . .')

while True:
    data, address = sock.recvfrom(1024)
    data = json.loads(data.decode())

    # FOR REGISTERING
    if data.get("command") == "register":
        if data.get("username"):
            if data.get("username") in names: # 502 user account exists
                send = json.dumps({"command":"ret_code", "code_no":502})
                sock.sendto(send.encode(), address)
            else: # 401 command accepted
                send = json.dumps({"command":"ret_code", "code_no":401})
                sock.sendto(send.encode(), address)
                names.append(data.get("username"))
                print('\nUsers in message board: ' + str(names)[1:-1])
        else: # 201 command parameters incomplete
            send = json.dumps({"command":"ret_code", "code_no":201})
            sock.sendto(send.encode(), address)

    # FOR DEREGISTERING
    elif data.get("command") == "deregister":
        if data.get("username"):
            if data.get("username") in names: # 401 command accepted
                send = json.dumps({"command":"ret_code", "code_no":401})
                sock.sendto(send.encode(), address)
                names.remove(data.get("username"))
                print(data.get("username") + ' : ' + "bye")
                print("User " + data.get("username") + " exiting. . .")
                print('\nUsers in message board: ' + str(names)[1:-1])
            else: # 501 user not registered
                send = json.dumps({"command":"ret_code", "code_no":501})
                sock.sendto(send.encode(), address)
        else: # 201 command parameters incomplete
            send = json.dumps({"command":"ret_code", "code_no":201})
            sock.sendto(send.encode(), address)

    # FOR MESSAGES
    elif data.get("command") == "msg":
        if data.get("username") and data.get("message"): 
            if data.get("username") in names: # 401 command accepted
                send = json.dumps({"command":"ret_code", "code_no":401})
                sock.sendto(send.encode(), address)
                print(data.get("username") + ' : ' + data.get("message"))
            else: # 501 user not registered
                send = json.dumps({"command":"ret_code", "code_no":501})
                sock.sendto(send.encode(), address)
        else: # 201 command parameters incomplete
            send = json.dumps({"command":"ret_code", "code_no":201})
            sock.sendto(send.encode(), address)

    # IF COMMAND IS UNKNOWN
    else: # 301 command unknown
        send = json.dumps({"command":"ret_code", "code_no":301})
        sock.sendto(send.encode(), address)