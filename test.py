from tcpserver import Server
import time

s = Server()
s.ip = 'localhost'
s.port = 8080
s.start()
counter = 0
while counter < 5:
    counter+=1
    print('from pipe ' + s.npipe.recv())
    print(str(counter))


print('doing this doing that')
time.sleep(3)
while True:
    print('from pipe again ' + s.npipe.recv())
