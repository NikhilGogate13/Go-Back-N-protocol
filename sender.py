import socket 
from threading import Thread
import time 
import os
threads=[]
base=1
base=int(base)
hiack=-1
hiack=int(hiack)
nextsegnum=1
nextsegnum=int(base)
lastackedtime=-1
lastackedtime=float(lastackedtime)
stime=0
stime=int(stime)
numofpacket=raw_input("Number of packets: ")
#numofpacket=100
numofpacket=int(numofpacket)
windowsize=raw_input("Size of window: ")
#windowsize=10
windowsize=int(windowsize)
timeouttime=raw_input("Time for timeout: ")
#timeouttime=4
timeouttime=float(timeouttime)
class ACKRecievingThread(Thread):
	def __init__(self,ip,port,sock):
		Thread.__init__(self)
		self.ip=ip
		self.port=port
		self.sock = sock
	def run(self):
		global base
		global nextsegnum
		global numofpacket
		global stime
                while nextsegnum<=numofpacket+1:
		    conn, addr = self.sock.accept()
		    ackpk=conn.recv(1024)
		    conn.close()
		    ackpk=ackpk.split(':')
		    acknum=int(ackpk[1])
                    print "ACK Num recieved:"+' '+ackpk[1]
		    if base<=acknum+1:
		    	base= acknum+1
		    if base==nextsegnum:
		    	stime=0
			
class SenderThread(Thread):
	def __init__(self,ip,port):
		Thread.__init__(self)
		self.ip=ip
		self.port=port
	def make_pkt(self,num):
		pkt="SeqNum:"+num
		return pkt
	def run(self):
		print "Sender is up and running"
		global nextsegnum
                global base
                global windowsize
                global lastackedtime
                global stime
		while base<=numofpacket+1:
                	#print nextsegnum
			#print base+windowsize
			if nextsegnum<base+windowsize and nextsegnum<=numofpacket:
				s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				s.connect((self.ip,self.port))
				temp=str(nextsegnum)
				data=self.make_pkt(temp)
                		print nextsegnum
                		print "Sending"+' '+str(nextsegnum)
				s.sendall(data)
				if base==nextsegnum:
					lastackedtime=time.time()
					stime=1
				nextsegnum=nextsegnum+1
				s.close()
		quit()
class TimerThread(Thread):
	def __init__(self):
		Thread.__init__(self)
	def run(self):
		global stime
		global base
		global nextsegnum
		while 1:
			#print str(time.time())+' '+str(lastackedtime)+' '+str(stime)
			#print time.time()-lastackedtime
			if time.time()-lastackedtime>timeouttime and stime==1:
				print "TimeOut"
                                nextsegnum=base
				stime=0
ACKSIP='localhost'
ACKPORT=9001
SenderIP='localhost'
SenderPORT=10001
#Binding Port for ACKReciever
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind((ACKSIP,ACKPORT))
sock.listen(5)
ackr=ACKRecievingThread(ACKSIP,ACKPORT,sock)
ackr.start()
threads.append(ackr)
time.sleep(5)
#Starting SenderThread
timer=TimerThread()
timer.start()
threads.append(timer)
sender=SenderThread(SenderIP,SenderPORT)
sender.start()
threads.append(sender)
for t in threads:
	t.join()
sock.close()
