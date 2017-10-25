#!/usr/bin/python3
import lxc

class conCreate:

	def __init__(self,name):
		self.name=name


	def create(self):
		conn=lxc.Container(self.name)
		created=conn.create("ubuntu",{"release":"xenial", "architecture":"amd64"})

		return created


	def start(self):

		self.created().start()
		print(container.get_ips(timeout=10))


if __name__=="__main__":
	tuna=conCreate("fazer")
