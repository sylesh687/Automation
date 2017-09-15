import sys
import os
import logging

from subprocess import Popen, PIPE
import shlex


#--------------------------------------------------------------------------------
# Getting Command Line Arguments And Validation
#--------------------------------------------------------------------------------
def inputs():

    ver=0
    role=''
    if (len(sys.argv) != 3 ):

        usage()

    else:
        ver=sys.argv[1]
        role=sys.argv[2]

        valid_ver,valid_role=Validations(ver,role)

        if (valid_role == True and valid_ver==True):
            print "Validation Done Successfully"

            url1,url2= Config(ver,role)

            add_to_repo = 'wget -O - %s | sudo apt-key add -' % (url1)
            write_to_file='echo %s > /etc/apt/sources.list.d/saltstack.list ' % url2
            install_salt_role='apt-get install salt-%s -y' %(role)

            o0,e0,rc0=runCmd(add_to_repo)

            if rc0==0:
                print "Successfully Added to repository"
                print o0
            else:
                print e0


            o1,e1,rc1=runCmd(write_to_file)
            if rc1==0:
                print "SuccessFully Written to a File"
                print o1 


            o1,e1,rc1=runCmd('sudo apt-get update')
            if rc1==0:
                print "SuccessFully Updated The repository"
                print o1

            o1, e1, rc1 = runCmd(install_salt_role)
            if rc1==0:
                print "SuccessFully Updated The repository"
                print o1



        else :
            usage()


def runCmd(cmd):

    cmdargs=shlex.split(cmd)

    Execute_Cmd=Popen(cmdargs, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    output, err = Execute_Cmd.communicate()
    rc=Execute_Cmd.returncode

    return output,err,rc

def Validations(ver,role):
    version_available="""
            Versions: 12 , 14 , 16
    """

    roles_available="""
        Roles: master , minion
    """

    valid_ver=False
    valid_role=False

    #---- Version Validation--------------------------------------
    try:
        ver=int(ver)
        if (ver==12 or ver==14 or ver==16):
            valid_ver=True

        else:

            print "---> Please Enter the Valid Version from %s " % version_available


    except ValueError as e:
        print e

        print "---> Please Enter the Valid Version from %s " % version_available

    #------master/minion  Validation------------------------------------------------

    if (role.upper()=='MASTER' or role.upper()=="MINION"):

        valid_role=True

    else:

        print "---> Please Enter  A Valid Role %s " % roles_available

    return valid_ver, valid_role

def usage():

    print "***** Salt Master/Minion Setup Config Management Script ******"
    data="""
            Usage: python Salt.py <version> <role>
            Eg: python Salt.py 16 master
    """
    print data
    print  "***************************************************************"


def Config(ver,role):
    codename=''
    version=''
    if ( int(ver) == 12):
        version='12.04'
        codename='precise'

    elif (int (ver) == 14 ):
        version = '14.04'
        codename='trusty'

    else:
        version='16.04'
        codename='xenial'


    url='http://repo.saltstack.com/apt/ubuntu/%s/amd64/latest/SALTSTACK-GPG-KEY.pub' %(version)
    url2='http://repo.saltstack.com/apt/ubuntu/%s/amd64/latest/ %s main' %(version,codename)

    return url ,url2

def main():
    inputs()

if __name__=="__main__":
    main()

