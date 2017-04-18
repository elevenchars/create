from threading import Thread
import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def connect(ip, port, name):  # attempt to connect to server, returns True if connection is successful
    try:
        s.connect((ip, port))
        s.sendall(json.dumps({"type": "status",
                              "body": "newconn",
                              "name": name}))
        resp = json.loads(recvall(s, 1024))
        if ("type" in resp and "body" in resp):
            if (resp["type"] == "status" and resp["body"] == "confirm"):
                return True
        else:
            s.close()
            return False
    except (socket.timeout, Exception) as e:
        print e
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
            content = json.loads(recvall(s, 1024))
            if(type in content):
                if(content["type"] == "message"):
                    self.callback(content)
