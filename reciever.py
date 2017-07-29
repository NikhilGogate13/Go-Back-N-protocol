import socket
from threading import Thread
import time
import os
import random
threads=[]
expectedseqnum=1
RecieverIP='localhost'
RecieverPORT=10001
ACKSIP='localhost'
ACKSPORT=9001

p=raw_input("Probablity for discarding packets: ")
#p=0.9
p=float(p)
if p>=1 or p<0:
	print "Probablity should be between 0 and 1."
	quit()
class RecieverThread(Thread):
	def __init__(self,ip,port,sock):
		Thread.__init__(self)
		self.ip=ip
		self.port=port
		self.sock = sock

	def extract(self , rcvpkt):
		temp = rcvpkt.split(':')
                print temp
		#converting the sequence number to integer
		temp1 = int(temp[1])
                print 'Packet seq num: '+temp[1]
		return temp1

	def run(self):
		print "Reciever is up and running"
                global expectedseqnum
		while 1:
                        prob = random.uniform(0,1)
                        print prob
			conn, addr = self.sock.accept()
			receivedpkt = conn.recv(1024)
			conn.close()
			print receivedpkt
			pktno = self.extract(receivedpkt)
			if prob<=p:
				if pktno==expectedseqnum:
					expectedseqnum = expectedseqnum +1
				asender=ACKSenderThread(ACKSIP,ACKSPORT, expectedseqnum-1)
				asender.start()
				threads.append(asender)
							

class ACKSenderThread(Thread):
	def __init__(self,ip,port,ackno):
		Thread.__init__(self)
		self.ip=ip
		self.port=port
		self.ackno =ackno
	def make_pkt(self,num):
		pkt="ACKNum:"+str(num)
		return pkt
	def run(self):
		print "Sending Ack "+str(self.ackno)
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((self.ip,self.port))
		s.sendall(self.make_pkt(self.ackno))
                s.close()
#Binding Port for ACKReciever
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind((RecieverIP,RecieverPORT))
sock.listen(100)
reciever=RecieverThread(RecieverIP,RecieverPORT,sock)
reciever.start()
threads.append(reciever)
time.sleep(5)
#Starting SenderThread

for t in threads:
	t.join()
sock.close()
