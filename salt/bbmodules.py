import sys
import os
import logging

from subprocess import Popen, PIPE
import shlex

from pylxd import Client
import re

import time as t

import thread

'''
	Runs a linux command and returns file descriptors
'''


def runCmd(cmd):
	

	cmdargs=shlex.split(cmd)
	Execute_Cmd=Popen(cmdargs, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = Execute_Cmd.communicate()
	rc=Execute_Cmd.returncode


	return output,err,rc
'''
	Creates n numbers of Containers provided with Prefix 

'''

def createContainer(number,containerPrefix="BB"):
	
	conlist=[]

	for con in range(int(number)):

		print "Creating Cluster'"
		
		conname="%s%s" % (containerPrefix,con)
		print conname
		command="lxc launch ubuntu: %s "% (conname)
		
		output,err,rc=runCmd(command)
		

		if rc==0:
			conlist.append(conname)
			print output
		else: 
			print err
	
	return conlist


'''
  	This Function gets the Number of running Containers on your system

'''
def getContainers(con):
	
	conlist=[]
	
	for container in (con.containers.all()):
		if (((container.status).upper()) == "RUNNING"):
			
			conlist.append(container.name)
	
	return conlist



'''
	This function is used to Delete the Container list with Some prefix

'''

def delContainers(prefex,conn):
	
	exp=re.compile("%s.*"%prefex)
	stopcommand="lxc stop %s "
	
	runningContainers=getContainers(conn)

	targetContainer=filter(exp.match,runningContainers)

	if len(targetContainer) == 0:

		print "We Dont Have Any Containers with supplied Prefex %s  , Please Try With Something Else" %(prefex)

	else:
		for tc in targetContainer:
			try:
				stopcommand="lxc stop %s " % (tc)
				print "Stopping %s, By Executing %s" %(tc,stopcommand)
				output,err,rc=runCmd(stopcommand)

				if rc==0:
					print "SuccessFully Stopped %s " %(tc)

					print output
				else:
					print err

				delcommand="lxc delete %s " % (tc)

				print "Deleting %s, By Executing %s" %(tc,delcommand)

				output , err , rc= runCmd(delcommand)

				if rc==0 :
					print "SuccessFully Deleted %s " %(tc)
					print output 
				else:
					print err

			
			except Exception as e:
				print e



'''
	This function runs linux commannd on n running containers

'''

def executeCmd(containerList,command):


	flag=0
	msg=''
	
	if len(containerList)==0:
		
		flag=1
		msg= "Please input atleast single list of container"


	else:

		for container in containerList:


			runCommand="lxc exec %s -- %s" %(container,command)
			print "Running %s on %s "% (runCommand,container)

			try:

				output,err,rc=runCmd(runCommand)

				if rc==0:
					print output
					print "Successfully executed %s  on %s " %(runCommand,container)

				else: 
					print err

			except Exception as e:
				print e
		
		flag=0
		msg="Successfully run %s in %s" %(command,containerList)

	return flag, msg


'''
	This Module is used to run command directly inside a conntainer

'''

def runOnContainer(conn,conlist,precmd):
	
	rc,stdout,sderr=0,'',''	
	for container in conlist:
		for cmds in precmd:
			print "[ %s ]  on  [ %s ]" %(cmds,container)
			coexecute=conn.containers.get(container)
			t.sleep(4)
			rc,stdout,sderr=coexecute.execute(['sh','-c',cmds])
			print stdout


	




