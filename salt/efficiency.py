
import threading 
import time 

from pylxd import Client
import time as t

exitFlag=0

class ConRun (threading.Thread):
	
	def __init__(self,conn,conlist,cmd):

		threading.Thread.__init__(self)
		self.conn=conn
		self.conlist=conlist
		self.cmd=cmd
	
	def run(self):

		
		rc,out,err=runOnContainer(self.conn,self.conlist,self.cmd)
		#print out
		




def runOnContainer(conn,conlist,cmd):
	
	rc,stdout,sderr=0,'',''
	precmd=["apt install python-minimal -y","apt install python-pip -y","pip install pylxd"]
	
	for container in conlist:
		for cmds in precmd:
			print "[ %s ]  on  [ %s ]" %(cmds,container)
			coexecute=conn.containers.get(container)
			t.sleep(4)
			rc,stdout,sderr=coexecute.execute(['sh','-c',cmds])
			#print stdout



		
		
		
		#t.sleep(5)
		

	return rc,stdout,sderr


# Create New Threads
conn=Client()
minionlist=['guiapps','Salt-Master']
cmd="apt upgrade "

thread1=ConRun(conn,minionlist,cmd)
thread2=ConRun(conn,minionlist,cmd)
thread3=ConRun(conn,minionlist,cmd)



#starting threads

thread1.start()
#thread2.start()