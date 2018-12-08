"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
import json
from ECC import *


class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.members = {}

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def set_keypair(self):
        self.keypair = MyKeys(self.me)

    def get_keypair(self):
        return self.keypair

    def get_members(self):
        return self.members.keys()

    def showallqk(self):
        return self.members

    def connect_to(self, peer, e = False):
        msg = json.dumps({"action":"connect","from": self.me, "target":peer, "encryption": e})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + ''
            self.members = response["members"]
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)'
        elif response["status"] == "Security Error":
            self.out_msg += "Security Alart: wrong crypto state"
        else:
            self.out_msg += 'User is not online, try again later'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect", "from": self.me})
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + ''
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += str(logged_in)

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away'
                        self.out_msg += ''
                    else:
                        self.out_msg += 'Connection unsuccessful'

                elif my_msg[0] == 'e':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer, True) == True:
                        self.state = S_ENCRYPTED
                        self.out_msg += 'Connect to ' + peer + '. Chat away!'
                        self.out_msg += 'The conversation is encrypted by Elliptic-curve Cryptography. '
                        self.out_msg += 'No history will be recorded.'
                        self.out_msg += ''
                    else:
                        self.out_msg += 'Connection unsuccessful'

                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"search", "target":term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + ''
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found'

                elif my_msg[0] == 'p' and my_msg[2:].isdigit(): #Kris Nov 17 2018: 1 -> 2
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action":"poem", "target":poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    if (len(poem) > 0):
                        self.out_msg += poem + ''
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                try:
                    peer_msg = json.loads(peer_msg)
                except Exception as err :
                    self.out_msg += " json.loads failed " + str(err)
                    return self.out_msg
            
                if peer_msg["action"] == "connect":
                    if peer_msg["status"] == "request":
                        self.out_msg += peer_msg["from"] + " has joined the chat."
                        self.members[peer_msg["from"]] = peer_msg["qk"]
                        self.state = S_ENCRYPTED if peer_msg["encryption"] else S_CHATTING
                        if len(self.members) == 1:
                            self.out_msg += "The conversation is encrypted by Elliptic-curve Cryptography"
                            self.out_msg += 'No history will be recorded.'
                            self.out_msg += ''
                    elif peer_msg["status"] == "no-user":
                        self.peer = ''
                        self.out_msg += "[ChatSystem]: No such user."
                    else:
                        self.out_msg += "[ChatSystem]: How did you wind up here??"
                        print_state(peer_msg["status"])
                    
#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING or self.state == S_ENCRYPTED:
            if my_msg == "#!members":
                self.out_msg += str(self.get_members())
            elif my_msg == "#!AllQK":
                self.out_msg += str(self.showallqk()) + str(self.get_keypair().get_public_key())
            elif my_msg == "#!MyKeypair":
                self.out_msg += str(self.get_keypair().get_keypair())
            elif my_msg[:3] == "#!T":
                path = my_msg[3:]
                name = os.path.basename(path)
                try:
                    with open(path.strip(), 'rb') as file:
                        bins = str(file.read())
                        mysend(self.s, json.dumps(
                            {"action": "transfer", "content": bins, "filename": name, "from": self.me}))
                    self.out_msg += "Transfer finished"    
                except FileNotFoundError:
                    self.out_msg += "File doesn't exist."
            elif len(my_msg) > 0 and self.state == S_CHATTING:     # my stuff going out
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":my_msg, "encryption": False}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
            elif len(my_msg) > 0 and self.state == S_ENCRYPTED:
                temp = my_msg[:]
                for m, qk in self.members.items():
                    msg, tqk = MsgECC(my_msg, qk).encrypt()
                    mysend(self.s, json.dumps(
                        {"action": "exchange", "from":"[" + self.me + "]", "to": m, "message": msg, "tqk": tqk, "encryption": True}))
                if temp == "bye":
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    
            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                #print(peer_msg)
                try:
                    if peer_msg["status"] == "request":
                        self.out_msg += peer_msg["from"] + " has joined the chat."
                        self.members[peer_msg["from"]] = peer_msg["qk"]
                except KeyError:
                    if peer_msg["action"] == "transfer":
                        with open(peer_msg["filename"], 'wb') as file:
                            file.write(eval(peer_msg["content"]))
                        self.out_msg += peer_msg["from"] + " transfered file: '" + peer_msg["filename"] + "' to you."
                    elif peer_msg["action"] == "exchange" and self.state == S_CHATTING:
                        self.out_msg += peer_msg["from"] + ": " + peer_msg["message"]
                    elif peer_msg["action"] == "exchange" and self.state == S_ENCRYPTED:
                        msg = MsgECC(peer_msg["message"], peer_msg["tqk"], self.keypair.get_private_key()).decrypt()
                        self.out_msg += peer_msg["from"] + ": " + msg
                    elif peer_msg["action"] == "disconnect":
                        self.out_msg += peer_msg["msg"] + "\n"
                    else:
                        self.out_msg += "[ChatSystem]: How did you wind up here??\n"
                        print_state(peer_msg["action"])

#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += '[ChatSystem]: How did you wind up here??'
            print_state(self.state)

        return self.out_msg 
