from pylxd import Client

conn=Client()


conlis=["gg0","gg1"]



def runOnContainer(conn,conlist,cmd):
	rc,stdout,sderr=0,'',''
	for container in conlist:
		coexecute=conn.containers.get(container)
		rc,stdout,sderr=coexecute.execute(['sh','-c',cmd])

	return rc,stdout,sderr

rc,stdout,sderr= runOnContainer(conn,conlis,"apt-get install python-minimal -y")
print stdout
rc,stdout,sderr= runOnContainer(conn,conlis,"git clone https://github.com/sylesh687/Automation.git")
print stdout
print sderr