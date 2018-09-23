#ICMP subnet scanner
import sys, time
from scapy.all import *

#Get subnet to scan
#try:
#    subnet = input('enter subnet to icmp scan: ')
#except Exception as e:
#    sys.exit(str(e))

subnet = '10.0.1.0/24'

def scan_net(subnet):
    subnet_split = subnet.split('/')[0].split('.')
    counter = 0
    while counter < 254:
        counter+=1
        time.sleep(0.1)
        print('Scanning: ' + subnet_split[0] + '.' + subnet_split[1] + '.' + subnet_split[2] + '.' + str(counter))
        ip_to_scan = subnet_split[0] + '.' + subnet_split[1] + '.' + subnet_split[2] + '.' + str(counter)
        threading.Thread(target=scan_single, args=(ip_to_scan,)).start()

def scan_single(ip_to_scan):
    p=sr1(IP(dst=ip_to_scan)/ICMP(),timeout=0.1,verbose=0)
    time.sleep(0.1)
    if p:
        p.show()

scan_net(subnet)
