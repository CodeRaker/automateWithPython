import socket, time       #Ressource til at lave TCP forbindelse

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #AF_INET fortaeller at der skal bruges host,port og SOCK_STREAM er den normale overfoerselsmetode.
    s.connect(('localhost', 8080))
    counter = 0
    while True:
        counter+=1
        try:
            s.send('START!') #unique
            s.send('i wonder how long a string can be before it is above the 1024') #message will split of too long
            s.send('COMPLETE!') #unique
        except Exception as e:
            print(e)
        time.sleep(3)

def main():
    connect()
main()
