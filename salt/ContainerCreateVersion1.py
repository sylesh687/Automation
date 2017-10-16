
'''
	
	Generate a certificate one can use open ssl command 

	openssl req -newkey rsa:2048 -nodes -keyout lxd.key -out lxd.csr
	openssl x509 -signkey lxd.key -in lxd.csr -req -days 365 -out lxd.crt


'''

from pylxd import Client


'''
	
	This Class is Blueprint for Container LifeCycle Action(Create/ Update/Delete)

'''


