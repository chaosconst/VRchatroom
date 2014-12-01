import signal
import socket
import threading
import SocketServer
import json
import math
import numpy

world = {}
MIN_SPEED = 0.005
MAX_SPEED = 0.3

acce_value = 0

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        global world, acce_value
        while True :
            try :
                 data = self.request.recv(128)
                 msg = json.loads(data)
                 if "acce_value" in msg:
                     acce_value = msg["acce_value"]
                     print msg
                 else:
                     print "get",msg
                     
                     avatar_key = self.client_address[0] + ":" + str(self.client_address[1])
                     if avatar_key in world :
                       status = world[avatar_key]
                       status[0] = msg["HeadVector"][0]
                       status[1] = msg["HeadVector"][1]
                       status[2] = msg["HeadVector"][2]
                       
                       theta = math.pi /2 + math.pi
                       spine_x = math.cos(theta) * msg["HeadVector"][2] - math.sin(theta) * msg["HeadVector"][0]
                       spine_y = math.sin(theta) * msg["HeadVector"][2] + math.cos(theta) * msg["HeadVector"][0]

                       acce = numpy.zeros(shape=(3))

                       acce[0] = spine_x
                       acce[1] = msg["HeadVector"][1]
                       acce[2] = spine_y

                       acce = acce * acce_value


                       speed = numpy.array([status[x] for x in range(6,9)])
                       
                       
                       #auto decrease speed
                       if numpy.linalg.norm(speed)> MIN_SPEED : 
                         speed = speed - (speed / numpy.linalg.norm(speed)) * 0.001
                       
                       #accelerate
                       if MIN_SPEED < numpy.linalg.norm(speed + acce) < MAX_SPEED:  
                         speed = speed + acce
                       elif numpy.linalg.norm(speed + acce) <= MIN_SPEED:
                         speed = speed * 0

                       status[3] += speed[0]
                       status[4] -= speed[1]
                       status[5] += speed[2]

                       status[6] = speed[0]
                       status[7] = speed[1]
                       status[8] = speed[2]
                     
                     else:
                       status = [msg["HeadVector"][0], msg["HeadVector"][1], msg["HeadVector"][2], 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

                       world[avatar_key] = status

                     world["self"] = avatar_key
                     
                     response = json.dumps(world) + "\n"
                     print "ans",response 
                     self.request.sendall(response)

            except Exception as e:
                 avatar_key = self.client_address[0] + ":" + str(self.client_address[1])
                 acce_value = 0
                 world.pop(avatar_key, None)
                 print "avatar_key", e
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

