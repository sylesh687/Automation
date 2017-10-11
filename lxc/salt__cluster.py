from pylxd import Client
from bbmodules import runCmd as  cmd

def getContainers(con):
	conlist=[]
	
	for container in (con.containers.all()):
		if (((container.status).upper()) == "RUNNING"):
			
			conlist.append(container.name)
	
	return conlist

def pushfile(file,containerlist):
	
	if (len(containerlist)==0):
		print "List of running container is Empty"
	else:
		for container in containerlist:
			filepush="lxc file push %s %s/root/" %(file, container)
			output,err,rc = cmd(filepush)

			if rc==0:
				print output

			else:
				print err

def install_Python(cl):

	for i in cl:
		install="lxc exec %s -- %s " %(i,"apt install python-minimal -y")
		output,err,rc=cmd(install)

		if rc==0:
			print output
		else:
			print err





def main():
	con=Client()
	cl=getContainers(con)
	print cl
	install_Python(cl)
	#print (pushfile("salt.py",cl))


if __name__=="__main__":
	main()