

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


i=instantSalt("P")
i.setup()
