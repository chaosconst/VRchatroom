import Tkinter as tk
import json
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST, PORT = "swarma.net", 1920

class FullScreenApp(object):
    button1_down = False

    def go_forward(self, a):
        global sock, HOST, PORT
        print time.time(), "start go forward"
        self.button1_down = True;

        msg={}
        msg["acce_value"] = 0.01

        try :
          sock.sendall(json.dumps(msg) + "\n")
        except:
          try:
            sock.close()
          except:
            pass
          sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          sock.connect((HOST, PORT))
          sock.sendall(json.dumps(msg) + "\n")

 

    def ButtonReleaseProcess(self, a):
        global sock, HOST, PORT
        print time.time(), "stop go forward"
        self.button1_down = False;
        msg={}
        msg["acce_value"] = 0.0
        try :
          sock.sendall(json.dumps(msg) + "\n")
        except:
          try:
            sock.close()
          except:
            pass
          sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          sock.connect((HOST, PORT))
          sock.sendall(json.dumps(msg) + "\n")
    
    def go_backward(self, a):
        global sock, HOST, PORT
        print time.time(), "go <-"
        msg={}
        msg["acce_value"] = -0.01
        try :
          sock.sendall(json.dumps(msg) + "\n")
        except:
          try:
            sock.close()
          except:
            pass
          sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          sock.connect((HOST, PORT))
          sock.sendall(json.dumps(msg) + "\n")

    def __init__(self, master, **kwargs):
        global sock, HOST, PORT
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))

        master.bind('<Escape>',self.toggle_geom)           
        master.bind('<Button-1>',self.go_forward)
        master.bind('<Prior>',self.go_forward)
        master.bind('<Up>',self.go_forward)
        master.bind('<Button-2>',self.go_backward)
        master.bind('<Next>',self.go_backward)
        master.bind('<ButtonRelease-1>', self.ButtonReleaseProcess)
        master.bind('<ButtonRelease-2>', self.ButtonReleaseProcess)
        master.bind('<KeyRelease-Prior>', self.ButtonReleaseProcess)
        master.bind('<KeyRelease-Next>', self.ButtonReleaseProcess)

        sock.connect((HOST, PORT))


 
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

root=tk.Tk()
app=FullScreenApp(root)
root.mainloop()
