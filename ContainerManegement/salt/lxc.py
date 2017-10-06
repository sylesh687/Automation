from subprocess import Popen,PIPE
import shlex
import sys

from bbmodules import runCmd as cmd

def usage():
	data= '''
			***********************LXC Management Scrit**********************
			Usage: python lxc.py <prefix> <no of containers>
			Eg:    python lxc.py "BB" 10

			*****************************************************************
	'''

	print data


def inputVal():
	
	if (len(sys.argv) !=3):
		usage()

	prefix=sys.argv[1]
	num=sys.argv[2]

	if (prefix==''):
		prefix="BBSALTM"

	try:
		int(prefix)
		
		print "Please Enter a Valid Prefix"

	except ValueError as E:

		print "Please enter a number"
		if (num==0 or num <0 or num> 20):
			print "Please Enter a no negative number other than 0 and lesser than 20"

	return prefix, num




def createContainer(number,containerPrefix="bb"):

	for con in range(number):
		conname="%s%s" % (containerPrefix,con)
		command="lxc launch ubuntu: %s "% (conname)
		
		output,err,rc=cmd(command)

		if rc==0:
			print output
		else: 
			print err


def main():
	prefix,num=inputVal()
	createContainer(num,prefix)

if __name__=="__main__":
	main()
