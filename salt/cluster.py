
from bbmodules import createContainer as cc
from bbmodules import executeCmd as ec
from bbmodules import runOnContainer as roc
import re
import sys
from pylxd import Client

import time as t

def gatherInput():
	clustnum=1

	try:
		
		clustnum=input("Enter the Number Of Nodes In Salt-Cluster : -- ")
		clustnum=int(clustnum)

		rc,msg=Validation(clustnum)

		if rc==0:
			print msg
		else:
			print msg
			sys.exit()
		
	except NameError as e:
		print "Please Enter a valid interger as %s " %(e)

	except ValueError as e:
		print e

	clustname=raw_input("Enter the ClusterName: -- ")

	if not re.match("^[a-z]*$",clustname):
		 print "Please Enter  a Valid ClusterName [ Only letters a-z allowed! ]"
		 sys.exit()
	
	elif len(clustname)>10:
		print "ClusterName should not be bigger than 8 chars"
		sys.exit()

	
	return clustnum , clustname



def Validation(clustnum):

	'''

		flag=0 means true and 1 means false

	'''
	flag=0
	flagmsg=''
	
	if clustnum<=0 or clustnum > 15 :
		flag=1
		flagmsg="Input Should Be Other than 0 Nonegative numbers lesser than 15"
	else:
		flag=0
		flagmsg="Successfully Validated"

	return flag , flagmsg		



def getMasterMinion():
	
	minion=[]
	num,name=gatherInput()
	
	'''
		 creating containers

	'''
	print num,name
	conlist=cc(num,name)
	print "container--list %s " % conlist
	master=''
	minion=[]
	if len(conlist) == 1:
		print "Single Node Cluster"
		master=conlist[0]
		minion=master
	
	else:
		master=conlist[0]
		minion=conlist[1:]

	
	return master,minion





def settingupminion(minionlist,conn):
	'''
		Clone the Git Repository

	'''
	print minionlist
	update="apt-get update"
	install_python="apt install python-minimal -y"
	clone="git clone https://github.com/sylesh687/Automation.git"
	install_pylxd="pip install pylxd"
	install_master="python  Automation/salt/salt.py 16 minion"

	rc,output,err= roc(conn,minionlist,update)
	if rc==0:
		print output
	else: 
		print err

	

	rc,output,err= roc(conn,minionlist,install_python)
	
	if rc==0:
		print output
	else: 
		print err


	rc,output,err= roc(conn,minionlist,clone)
	if rc==0:
		print output

	else: 
		print err

	rc,output,err= roc(conn,minionlist,"apt install python-pip -y")
	if rc==0:
		print output
	else :
		print err

	rc,output,err= roc(conn,minionlist,"pip install pylxd")
	if rc==0:
		print output
	else :
		print err

	

	rc,output,err= roc(conn,minionlist,install_master)

	if rc==0:
		print output
	else :
		print err






def main():
	conn=Client()
	master,minion= getMasterMinion()
	print master
	print (settingupminion(minion,conn))



if __name__=="__main__":
	main()