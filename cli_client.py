import Client
import json

def response_printer(resp):
    print json.dump(resp)

success = False
while(not success):
    ip = raw_input("please enter the server IP")
    port = int(raw_input("please enter the server port"))
    success = Client.connect(ip, port)

print "connection successful"

sl = Client.ServerListener(response_printer)
sl.start()

while 1:
    Client.send({"type" : "message",
                 "body" : raw_input("message > ")})