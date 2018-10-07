import socket, time    #Ressource til at lave TCP forbindelse

def connect():      #Funktion til shell forbindelse

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #AF_INET
    s.bind(("localhost", 8080))
    s.listen(1)     #Angiver antallet af forbindelser der forventes.

    print '[+] Listening for incoming TCP connection on port 8080'

    conn, addr = s.accept()     #Ud af accept kan vi traekke informationer om forbindelser der er oprettet til det aktive netvaerkssocket.

    print '[+] Received connection from: ', addr

    counter = 0
    while True:
        try:
            a = conn.recv(1024)
        except Exception as e:
            print(e)
            a = ''
        if a:
            print(a)

def main ():
    connect()
main()
