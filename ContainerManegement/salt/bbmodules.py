import sys
import os
import logging

from subprocess import Popen, PIPE
import shlex

'''
	Runs a linux command and returns file descriptors
'''
def runCmd(cmd):
	

	cmdargs=shlex.split(cmd)
	Execute_Cmd=Popen(cmdargs, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = Execute_Cmd.communicate()
	rc=Execute_Cmd.returncode


	return output,err,rc

