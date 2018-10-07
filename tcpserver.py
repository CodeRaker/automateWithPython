import socket
from multiprocessing import Process, Pipe

class Server:
    def __init__(self):
        self.ip = ''
        self.port = 0
        self.npipe, self.spipe = Pipe()
        self.keepAlive = True

    def start(self):
        p = Process(target=self.server, args=())
        p.start()

    def server(self):
        keepAlive = True
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.ip, self.port))
        s.listen(1)
        print('listening')
        conn, addr = s.accept()
        print('received connection from ' + str(addr))
        while keepAlive == True:
            try:
                d = conn.recv(1024)
            except Exception as e:
                pass
            if d:
                self.spipe.send(d)
            if self.spipe.poll():
                if self.spipe.recv() == 'close':
                    keepAlive = False
        conn.close()
        #self.stop()
    def stop(self):
        #self.keepAlive = False
        p.terminate()


class Client:
    def __init__(self):
        self.ip = ''
        self.port = 0
        self.npipe, self.spipe = Pipe()

    def start(self):
        p = Process(target=self.client, args=(self.ip,self.port,self.spipe))
        p.start()

    def client(self,ip,port,spipe):
        keepAlive = True
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        while keepAlive:
            try:
                if spipe.poll():
                    s.send(spipe.recv())
            except Exception as e:
                pass
