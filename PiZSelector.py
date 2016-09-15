import sys, os
import numpy as np
import Utils.datahandle as dh
import ROOT 
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
from scipy import stats


# List for the reco mass 
rmass_v = []
maxdatasetsize = 10000
proc = 0 

for f in sys.argv[1:]:
    fi = ROOT.TFile("{}".format(f))

#Bring in data 
    predataset = dh.ConvertWC_InTPC('{}'.format(f))
    print 'predataset size ', len(predataset)
    dataset = dh.Unique(predataset)
    print 'dataset size ', len(dataset)

    if len(dataset)>maxdatasetsize:
        continue
    proc +=1



# Add some clustering algos
    import Clustering.protocluster as pc
    labels = pc.crawler(dataset,8.,10)

#Shit hack for now
# Add this into the utilities 
    import collections as col
    shi = col.Counter(labels)
# Shi is a set, and dic lookup 
    print shi.items()
    cval = [x[0] for x in shi.items() if x[1]>200]
    print cval
# cval are cadidate shower/cluster id ... find out what there index is in dataset
#  find out what there index is in dataset below 
    datasetidx_holder = []
    for s in cval:
        datasetidx_v = []
        [datasetidx_v.append(i) for i, j in enumerate(labels) if j == s]
        datasetidx_holder.append(datasetidx_v)

#datasetidx_holder contains lists of index values for cluster in the dataset
# Run over them as pairs 
#################
    import SParams.axisfit as axfi
    import SParams.selpizero as selpz

    if len(datasetidx_holder)<2: 
        print'seg fault'

    FIA = 0  
    FIB = 0    
    shrpair_v = []
 
    for a in xrange(len(datasetidx_holder)):
        shrA = axfi.showerfit(dataset,datasetidx_holder[a])
        EA =  selpz.totcharge(dataset,datasetidx_holder[a]) 
        for b in xrange(a+1,len(datasetidx_holder)):
            shrB = axfi.showerfit(dataset,datasetidx_holder[b])
            EB =  selpz.totcharge(dataset,datasetidx_holder[b]) 
        #print 'position :' , str(a),str(b)
	#### Will do work in here 
	    vertex = selpz.findvtx(shrA,shrB)
            angle = selpz.openingangle(shrA,shrB,vertex)

	# Get prodocuts to return index 
	
	# If dataset holder ==2 just make the mass
	    recomass = selpz.mass(EA,EB,angle)
	    
	#############################
	###cut on opening anlge####
	#############################
	    if angle < 0.1:
	        continue
            #if EA+EB<.070:
	#	continue
            print' this is a given reco mass' , str(recomass*1000)
	    pair = (a,b,recomass)
	    shrpair_v.append(pair)
	
#############################
#############################
# Fill out the mass histogram
#############################
#############################

    if len(shrpair_v)>=1:
        rmass_v.append(shrpair_v[0][2]*1000.)



print 'Summary: ' , proc, ' out of ', len(sys.argv[1:]),' total files were processed '    
    
fig3 = plt.figure()
n, bins, patches = plt.hist(rmass_v, 35, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(rmass_v)
y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'r--', linewidth=1)
nent = len(rmass_v)
plt.title(r'$\mathrm{(True-Reco) / True:}\ \mu=%.3f,\ \sigma=%.3f,\ \mathrm{entries:}\ %.3f,\ \mathrm{ out of:}\ %.3f $' %(mu, sigma,nent,proc))
plt.show()




