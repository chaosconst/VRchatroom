import signal
import socket
import threading
import SocketServer
import json

world = {}

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        global world
        while True :
            try :
                 data = self.request.recv(128)
                 msg = json.loads(data)
                 print "get",msg
                 
                 avatar_key = self.client_address[0] + ":" + str(self.client_address[1])
                 if avatar_key in world :
                   status = world[avatar_key]
                   status[0] = msg["HeadVector"][0]
                   status[1] = msg["HeadVector"][1]
                   status[2] = msg["HeadVector"][2]
                   status[3] += 0.1
                   status[4] += 0.1
                   status[5] += 0.1
                 else:
                   status = [msg["HeadVector"][0], msg["HeadVector"][1], msg["HeadVector"][2], 0.0, 0.0, 0.0]
                   world[avatar_key] = status

                 world["self"] = avatar_key
                 
                 response = json.dumps(world) + "\n"
                 print "ans",response 
                 self.request.sendall(response)

            except Exception as e:
                 avatar_key = self.client_address[0] + ":" + str(self.client_address[1])
                 world.pop(avatar_key, None)
                 print e
                 print "break!"
                 break

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def initWorld():
  pass

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "swarma.net", 1920

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    #init world
    initWorld()

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print "Server loop running in thread:", server_thread.name, ip, port

    try:
        signal.pause()  # wait for a signal, perhaps in a loop?
    except:
        server.shutdown()  # graceful quit

