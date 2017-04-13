import client
import json

def response_printer(resp):
    print json.dump(resp)

success = False
while(not success):
    ip = raw_input("please enter the server IP: ")
    port = int(raw_input("please enter the server port: "))
    name = raw_input("please enter your username: ")
    success = client.connect(ip, port, name)

print "connection successful"

sl = client.ServerListener(response_printer)
sl.start()

while 1:
    client.send({"type" : "message",
                 "body" : raw_input("message > ")})