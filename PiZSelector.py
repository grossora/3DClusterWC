import sys, os
import math as math
import numpy as np
import Utils.datahandle as dh
import Utils.mchandle as mh
import ROOT
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
from scipy import stats
import Clustering.protocluster as pc
import collections as col
import SParams.axisfit as axfi 
import SParams.selpizero as selpz
import SParams.merger as mr


rmass_v = []
maxdatasetsize = 20000
proc = 0

#### THese cuts don't matter here
#minanlge = 0.3
#Emin = .001
#maxIP = 10
lookup = open('Out_text/test.txt','a+')
#lookup = open('Out_text/PiZero_Selection_Params.txt','a+')

totproc = 0 

for f in sys.argv[1:]:
    ##########
    #### Build in a check to see if we did this already
    ##########

    dirnum = f.rsplit('/',1)[0].rsplit('/',1)[1]
    fnum = f.rsplit('/',1)[1].rsplit('.')[0].rsplit('_',1)[1]
    alreadydone = False
    for line in  lookup:
	sline = line.split(' ',2)
	print ' alrady have these '  
	print sline[0]
	print sline[1]
	if sline[0]==dirnum and sline[1]==fnum:
	    alreadydone = True
	    break
    if alreadydone:
	continue

    fi = ROOT.TFile("{}".format(f))
    rt= fi.Get("T_rec")
    if rt.GetEntries()==0:
        print 'AHHHH Got nothing...'
        ##################################    FILLLLLLLLLLLLL
	fline =[ -2 for x in range(43)]
	rfline = dirnum+' '+fnum+' '+ str(fline).split('[')[1].rsplit(']')[0].replace(',','')+ '\n'
	lookup.writelines(rfline)

	 
        continue
    TruthString = mh.piz_mc_info('{}'.format(f))
    ### TEMP
    print dirnum
    print fnum
    print TruthString
    predataset = dh.ConvertWC_InTPC('{}'.format(f))
    print 'predataset_size ' , len(predataset)
    dataset = dh.Unique(predataset)
    print 'dataset_ Unique', len(dataset)
    if len(dataset)>maxdatasetsize: 
        ##################################    FILLLLLLLLLLLLL
	fline =[ -3 for x in range(43)]
	rfline = dirnum+' '+fnum+' '+ str(fline).split('[')[1].rsplit(']')[0].replace(',','')+ '\n'
	lookup.writelines(rfline)
	continue
    totproc +=1
    print 'Current Event -->  Dir: ', str(dirnum) +'  File number ' + str(fnum)
   # proc +=1
    labels = pc.crawler(dataset,9,10)
    #labels = pc.crawler(dataset,8.,10)
    datasetidx_holder = mr.label_to_idxholder(labels,150)
    nlabels = mr.PCA_merge(dataset,labels,datasetidx_holder,0.35)
    labels = nlabels
    datasetidx_holder = mr.label_to_idxholder(labels,150)


    
	
    if len(datasetidx_holder)==1:
	print 'segfault' 
        ##################################    FILLLLLLLLLLLLL
	fline =[ -4 for x in range(43)]
	rfline = dirnum+' '+fnum+' '+ str(fline).split('[')[1].rsplit(']')[0].replace(',','') + '\n'
	lookup.writelines(rfline)
	continue
    if len(datasetidx_holder)==0:
	print 'segfault' 
        ##################################    FILLLLLLLLLLLLL
	fline =[ -5 for x in range(43)]
	rfline = dirnum+' '+fnum+' '+ str(fline).split('[')[1].rsplit(']')[0].replace(',','') + '\n'
	lookup.writelines(rfline)
	continue
    shrpair_v = []

    #Implement a shower merging

    for a in xrange(len(datasetidx_holder)):
	shrA = axfi.weightshowerfit(dataset,datasetidx_holder[a])
	EA = selpz.corrected_energy(dataset,datasetidx_holder[a])
	ChargeA = selpz.totcharge(dataset,datasetidx_holder[a])
	for b in xrange(a+1,len(datasetidx_holder)):
	    shrB = axfi.weightshowerfit(dataset,datasetidx_holder[b])
	    EB = selpz.corrected_energy(dataset,datasetidx_holder[b])
	    ChargeB = selpz.totcharge(dataset,datasetidx_holder[b])
	    vertex = selpz.findvtx(shrA,shrB)
	    IP = selpz.findIP(shrA,shrB)
	    #print 'VERTEX ', str(vertex)
	    SP_a = selpz.findRoughShowerStart(dataset,datasetidx_holder[a],vertex)
	    #print 'SP A : ', str(SP_a)
	    radL_a = selpz.findconversionlength(vertex,SP_a)
	    SP_b = selpz.findRoughShowerStart(dataset,datasetidx_holder[b],vertex)
	    #print 'SP B : ', str(SP_b)
	    radL_b = selpz.findconversionlength(vertex,SP_b)
	    #print 'radL B', str(radL_b)
	    
	    angle = selpz.openingangle(shrA,shrB,vertex)	
	    recomass = selpz.mass(EA,EB,angle)
	    # Place all cuts
	    #if angle< 0.1:
	    #	continue
		
	    #print 'IP', IP 
	    #print 'recomass', recomass*1000.#Putting things in MEV
	    
	    pair = (a,b,recomass)
	    shrpair_v.append(pair)
	    
	    #Format : 
	    #old # Proc , mass , ShrA , ShrB, Elarge, Esmall, Angle, IP,radL_A , radL_B, vtx_x , vtx_y, vtx_z
	    RecoString =' ' +str(recomass*1000)+' '+ str(vertex[0])+ ' '+ str(vertex[1])+ ' '+ str(vertex[2])+' '+ str(EA)+' '+ str(ChargeA)+ ' '+ str(SP_a[0])+ ' '+ str(SP_a[1])+ ' '+ str(SP_a[2])+ ' '+ str(EB)+' '+ str(ChargeB)+ ' '+ str(SP_b[0])+ ' '+ str(SP_b[1])+ ' '+ str(SP_b[2])+ ' '+str(angle)+' '+str(1-math.cos(angle))+ ' '+ str(IP)+ ' '+ str(radL_a)+ ' '+ str(radL_b)

	    line = str(dirnum)+ ' ' + str(fnum)+' '+TruthString+RecoString+'\n'
	    #line linegth is 43
	    lookup.writelines(line)

lookup.close()
#print 'Summary: ' , proc, ' out of ', len(sys.argv[1:]), ' total files proccessed'


print' Total Processed ', str(totproc)
