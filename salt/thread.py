import thread
import time

def runOnContainer(conn,conlist,cmd):
    
    rc,stdout,sderr=0,'',''
    for container in conlist:

        print "Dealing with %s" %(container)
        coexecute=conn.containers.get(container)
        rc,stdout,sderr=coexecute.execute(['sh','-c',cmd])
        t.sleep(5)

        
        
    return rc,stdout,sderr

