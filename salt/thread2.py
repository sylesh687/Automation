import threading

from pylxd import Client
import time as th

def worker():
	print "worker"

	return 


def runOnContainer(conn,container,cmd):
	
	rc,stdout,sderr=0,'',''
	
	print "[ %s ]  on  [ %s ]" %(cmd,container)
	coexecute=conn.containers.get(container)
	rc,stdout,stderr=coexecute.execute(['sh','-c',cmd])
	th.sleep(5)
	if rc==0:
		print stdout
	else:
		print stderr


threads=[]
conn=Client()

	
for i in range(3):
	t=threading.Thread(target=runOnContainer,args=(conn,"gr2","hostname"))
	threads.append(t)

	t.start()