#!/usr/bin/env python

import os, sys, re, time, string
from subprocess import Popen

timestr=time.strftime("%Y%m%d-%H%M%S")
fsubfile='submission.data'

seedfile = '/home/smritipradhan/seed'
seed = int(open(seedfile).read())
#fsub=open(fsubfile,'a+')

accounts=['hagan-lab']
partitions=['hagan-compute-long']
#nodes=['compute-9-[0-7]']
index0=0
index1=1
index2=4
runs=50


#account=accounts[index]
#partition=partitions[index]
#rep0 = { 'DMU' : map(float, "  -3.5 ".split())} #later do in between
rep1 = { 'GB' : map(float, " -6.0".split())}
#rep2 = { 'MU' : map(float, " -10.8 -11.1 -11.5 -12.2 ".split())}

rep0 = { 'DMU' : map(float, " -4.5 ".split())} #later do in between

#rep1 = { 'GB' : map(float, " -5.6 -5.8 -6.0 -6.2 ".split())}
rep2 = { 'kd' : map(float, "0.01".split())}
#rep2 = { 'gdrug' : map(float, " 1.4 1.5 ".split())} #drug binding affinity for CD-CD

#rep0 = { 'DMU' : map(float, "  -4.5 ".split())} #later do in between
#rep1 = { 'GB' : map(float, " -5.6 ".split())}
#rep2 = { 'MU' : map(float, " -10.8 -11.1 -11.5 -12.2 ".split())}



j=['dmu','gb','kd']
sh_tmp = string.Template(open('base.sh').read())
i=0
for x in range(1,runs+1):

    if x%4==0:
        index=index0
    #lif x%==1:
    #   index=index2
    else:
        index=index0

    account=accounts[index]
    partition=partitions[index]


    for k1,vals1 in rep1.iteritems(): #AVGB to GB
        for k2,vals2 in rep2.iteritems():
            for k0,vals0 in rep0.iteritems(): #DMUs
                for v2 in vals2:
                    for v1 in vals1:
                        for v0 in vals0:
                            #print("v1 ",v1 , " v0 ",v0)
                            
                            v1GB=str(int(100*(4*(float(v1)-3.42)+float(v0))/4.3)/100.0)
                            #rint("v1GB ",v1GB)
                            #rint("kCM %.2f"%(float(v1GB)/1.689))

                            dirf='SE-%s-%s_R%s-%s_%s-%s' % (k0, str(v0), k1, str(v1), k2, str(v2)) 
                            #rint(dirf)
                            if not (os.path.exists('%s' %dirf)):
                                Popen('mkdir %s' %dirf , shell = True).wait()
                            #Popen('cd %s' % dirf, shell = True).wait()
                            #print("now in ",os.getcwd())

                            dirx='seed-%s' % (str(x))
                            jobname='SM_Dec20_1-%s-%s_R%s-%s_%s-%s_%s' % (j[0] ,str(v0), j[1], str(v1), j[2], str(v2), str(x))
                            seed = seed + 1
                            if not (os.path.exists('%s/%s' %(dirf,dirx))):
                                #print(k0, str(v0) , k1, str(v1GB), k2, str(v2), str(x))
                                sh = sh_tmp.substitute({ 'ACCOUNT' : account , 'PARTITION' : partition , 'DIRF' :dirf, 'DIRX' :dirx ,'JNAME' : jobname , 'SEED' : str(seed), k2: str(v2), k1 : str(v1GB), k0: str(v0) })
                                Popen('mkdir %s/%s' %(dirf,dirx) , shell = True).wait()
                                #Popen('cd %s/%s' % (dirf,dirx), shell = True).wait()
                                print("now in ",os.getcwd())    
                                #sh = sh_tmp.substitute({ 'DIR' : dirx ,'JNAME' : jobname , 'SEED' : str(seed), k2: str(v2), k1 : str(v1), k0: str(v0) })
                                    
                                open('%s/%s/sd%s.sh'% (dirf,dirx, seed), 'w').write(sh)
                                    
                                Popen('chmod +x %s/%s/sd%s.sh' % (dirf,dirx, seed), shell = True).wait()

                                Popen('sbatch %s/%s/sd%d.sh'% (dirf, dirx, seed), shell = True).wait()
                                
                                #time.sleep(1)
                                #fsub.write('%s\t%s\t%s\n'% (dirx , jobname , nodes[i%len(nodes)]))
                                i+=1
                                #if i==len(nodes):
                                #sys.exit()								
                            else:
                                print('Already submitted  : ','%s' % dirx)

open(seedfile,'w').write(str(seed))
#fsub.close()
