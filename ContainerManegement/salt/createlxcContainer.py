from subprocess import Popen,PIPE
import shlex

def createContainer(number,containerPrefix="bb"):

	for con in range(10):
		conname="%s%s" % (containerPrefix,con)
		command="lxc launch ubuntu: %s "% (conname)
		
		output,err,rc=cmd(command)

		if rc==0:
			print output
		else: 
			print err


def main():
	createContainer(10,"m")

if __name__=="__main__":
	main()
