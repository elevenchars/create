from threading import Thread
import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect(ip, port):  # attempt to connect to server, returns True if connection is successful
    s.connect((ip, port))
    s.sendall(json.dumps({"type" : "status",
                         "body" : "newconn"}))
    resp = json.loads(recvall(s, 1024))
    if("type" in resp and "body" in resp):
        if(resp["type"] == "status" and resp["body"] == "confirm"):
            return True
    else:
        return False


def recvall(sock, buff):
    data = ""
    while 1:
        part = sock.recv(buff)
        data += part
        print part
        if len(part) < buff:
            break  # exit loop on last part of message
    return data


def send(content):
    s.sendall(json.dumps(content))


class ServerListener(Thread):  # class to receive messages from server, must connect first
    def __init__(self, callback):
        Thread.__init__(self)
        self.callback = callback

    def run(self):
        while 1:
            print "looking for message!"
            content = json.loads(recvall(s, 1024))
            if(type in content):
                if(content["type"] == "message"):
                    self.callback(content)
