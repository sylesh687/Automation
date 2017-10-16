

'''

	OOD- FOR SALT SETUP Only For ubuntu-Machines


'''

import time
import sys
import shlex
from subprocess import Popen, PIPE
from bbmodules import runCmd as cmd


class salt:

	'''
		Object Intialiazation 

	'''
	def __init__(self,version,role):
		self.version=version
		self.role=role


	
	def validate(self):

		versions= """  12 or 14  or  16"""

		roles=""" 	master /  minion  """

		'''
			vv=valid role 
			vr=valie version
			vm= error message for version
			rm= error messagge for role

		'''

		vv=False
		vm=''
		vr=False
		rm=''


		'''
				Versions Validation

		'''

		try:
			self.version=int(self.version)
			
			if (self.version==12 or self.version==14 or self.version==16):
				vv=True

			else:

				print "Please Enter The Correct Version -- [[%s]] " % versions
				sys.exit()

		except ValueError as e:
			print e

			vm= "Please Enter The Correct Versioo-- [[%s]]  " % versions
			sys.exit()


		'''
				Roles Validation
		'''

		try:

			if ((self.role).upper()=='MASTER' or (self.role).upper()=="MINION"):
				valid_role=True

			else:
				print "Please Enter  A Valid Role -- [[%s]] " % roles
				sys.exit()

		except AttributeError as e:
			print "Please Enter A Valid Role (It Should be String) -- [[ %s]]" % roles
			sys.exit()



		return self.role,self.version


		


	def createurl(self):
		
		codename={"12.04":"precise","14.04":"trusty","16.04":"xenial"}
		vs,vm=self.validate()
		

		url=''

		if vm==12 or vm == 14 or vm == 16:
			
			vm="%s.04" % vm
			url="http://repo.saltstack.com/apt/ubuntu/%s/amd64/latest/SALTSTACK-GPG-KEY.pub " % vm
			deburl="deb http://repo.saltstack.com/apt/ubuntu/%s/amd64/latest/ %s main" %( vm , codename[vm])


		
		return url,deburl
		
	def writetofile(self):
		
		filename="/etc/apt/sources.list.d/saltstack.list"

		gpgpubkey,repourl=self.createurl()

		'''
			Adding the Public Key

		'''
		key_download = 'wget -O - %s ' % gpgpubkey
		print key_download
		cmd1=shlex.split(key_download)
		cmd2=shlex.split("sudo apt-key add -")

		scmd1=Popen(cmd1, stdin=PIPE, stdout=PIPE, stderr=PIPE)
		scmd2=Popen(cmd2,stdin=scmd1.stdout,stdout=PIPE,stderr=PIPE)

		output, err= scmd2.communicate()
		rc=scmd2.returncode

		print output

		try:

			with open(filename,'w') as fin:
				fin.write(repourl)

			print "SuccessFully Written [[ %s  ]] to [[ %s ]] " %(repourl,filename)
		
		except IOError as e:

			print "Unable To Write To %s Due to [[ %s ]] " %(filename,e)
			sys.exit()

	
	def installSalt(self):
		
		role,version=self.validate()
		role=str(role)
		role=role.lower()
		role="salt-%s" % role
		saltcmd="apt install % s " % role
		cmdlist=["apt-get update",saltcmd]
		
		for cmdlet in cmdlist:
			output,err,rc=cmd(cmdlet)
			time.sleep(9)
			
			if rc==0:
				
				print output

			else: 
				
				print err






if __name__=="__main__":

	'''
		Objection instantiation and initialization

	'''

	salt1=salt("16","master")

	# Writing to file

	salt1.writetofile()

	salt1.installSalt()


