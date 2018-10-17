import sys
import os
import logging
#@@
from subprocess import Popen, PIPE
import shlex

from bbmodules  import runCmd as cmd

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

            key_download = 'wget -O - %s ' % (url1)
            key="sudo apt-key add -"
            #write_to_file='echo %s > /etc/apt/sources.list.d/saltstack.list ' % (url2)
            url2="deb %s" % url2
            
            try:
              with open('/etc/apt/sources.list.d/saltstack.list','w') as f:
                f.write(url2)
                print "%s is success fully written to /etc/apt/sources.list.d/saltstack.list" % url2
            except IOError as e:
              print "unable to write to file %s" % e

            install_salt_role='apt-get install salt-%s -y' %(role)
            print install_salt_role
            Cmd1=shlex.split(key_download)
            Cmd2=shlex.split(key)

            st_out_1=Popen(Cmd1, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            st_out_2=Popen(Cmd2,stdin=st_out_1.stdout,stdout=PIPE,stderr=PIPE)
            output, err = st_out_2.communicate()
            rc=st_out_2.returncode
  
            if rc==0:
                print "Successfully Added to repository"
                print output
            else:
                print err 


            o1,e1,rc1=cmd('sudo apt-get update')
            if rc1==0:
                print "SuccessFully Updated The repository"
                print o1

            o1, e1, rc1 = cmd(install_salt_role)
            if rc1==0:
                print "SuccessFully installed %s " % role
                print o1



        else :
            usage()


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

