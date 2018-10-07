from tcpserver import Client
import time


c = Client()

c.ip = 'localhost'
c.port = 8080
c.start()
counter = 0
while counter < 10:
    counter+=1
    c.npipe.send('test')
    time.sleep(1)
print('doing this doing that')
c.npipe.send('sending more stuff')

