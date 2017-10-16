
from bbmodules import createContainer as cc
from bbmodules import executeCmd as ec
from bbmodules import runOnContainer as roc
import re
import sys
from pylxd import Client

import time as t
import thread as th
import threading 

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

	if not re.match("^[a-zA-Z]*$",clustname):
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


class ConRun(threading.Thread):
	
	def __init__(self,conn,conlist,cmd):

		threading.Thread.__init__(self)
		self.conn=conn
		self.conlist=conlist
		self.cmd=cmd
	
	def run(self):
		
		roc(self.conn,self.conlist,self.cmd)
		t.sleep(5)


def preReq(minionlist,conn):

	precmd=["apt upgrade","apt install python-minimal -y","apt update ; apt install python-pip -y","pip install pylxd","git clone https://github.com/sylesh687/Automation.git"]
	lh=rh=0

	if len(minionlist)%2==0:
		lh=len(minionlist)/2
		rh=lh

	else:

		lh=len(minionlist)//2
		rh=len(minionlist)-lh

	print lh
	print rh
	thread1=ConRun(conn,minionlist[:lh],precmd)
	thread2=ConRun(conn,minionlist[-rh:],precmd)
	
	print minionlist[:lh]
	print minionlist[-rh:]
	thread1.start()
	thread2.start()






def main():

	conn=Client()
	master,minion= getMasterMinion()
	print master
	print minion
	preReq(minion,conn)





if __name__=="__main__":
	main()