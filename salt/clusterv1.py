
class cluster:

	def __init__(self,num,name,config):
		self.num=num
		self.name=name
		self.config=config


	def validate(self):
		import sys
		import re
		

		try:
			self.num=int(self.num)
			if not re.match("^[a-zA-Z]*$",self.name):
				print "Enter A Valid ClusterName"
				sys.exit()

		except ValueError as e:
			print e
			sys.exit()

		return self.num,self.name


	def create(self):
		from pylxd import client
		client=Client()
		config = {
        
        "source": {
               "type": "image"
               "mode": "pull",
               "server": "https://cloud-images.ubuntu.com/releases",
               "protocol": "simplestreams"
               "fingerprint": "16.04"
        }
    }

    	container = client.containers.create(config, wait=False)

    	print container

  c=cluster()


