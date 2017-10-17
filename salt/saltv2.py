

class instantSalt:


	def __init__(self,role):
		self.role=role

	def setup(self):
		from bbmodules import runCmd as cmd 

   		curl="curl -L https://bootstrap.saltstack.com -o install_salt.sh"

   		output, err , rc=cmd(curl)
   		print output
   		print err
   		print rc 

   		install_salt="sh install_salt.sh -%s" %(role)
   		output, err , rc=cmd(install_salt)
   		print output
   		print err
   		print rc 


i=instantSalt("P")
i.setup()
