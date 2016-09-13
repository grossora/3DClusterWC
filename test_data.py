import sys, os
import numpy as np
import Utils.datahandle as dh
    
print sys.argv[1]


## Find Event number
evtpath = str(sys.argv[1])
evt = evtpath.split('result_')[1].split('.')[0]

# Open up the text file for looking up the ROI 
# Find the line that had the evt and then read off the rest of the params 
lookup = open('ROI_Visual.txt','r')

fid_v =[]
for line in lookup:
    #print line
    # split up the line
    line_v = line.split()
    if line_v[0] == evt:
        fid_v = line_v[1:]
if len(fid_v) ==0:
    print 'We did not find an ROI for this event'
    print ' If you like you may put them in manually... don\'t mess it up '
    xlo = raw_input('Value for xlo:')
    xhi = raw_input('Value for xhi:')
    ylo = raw_input('Value for ylo:')
    yhi = raw_input('Value for yhi:')
    zlo = raw_input('Value for zlo:')
    zhi = raw_input('Value for zhi:')
    fid_v = [xlo,xhi,ylo,yhi,zlo,zhi]
print 'These are the params you are using ', fid_v
#bring in the data
#predataset = dh.ConvertWC_InRange('{}'.format(sys.argv[1]),0,256,-116,-20,300,600)### First attempt
predataset = dh.ConvertWC_InRange('{}'.format(sys.argv[1]),float(fid_v[0]),float(fid_v[1]),float(fid_v[2]),float(fid_v[3]),float(fid_v[4]),float(fid_v[5]))
#predataset = dh.ConvertWC_InRange('{}'.format(sys.argv[1]),float(fid_v[0]),fid_v[1],fid_v[2],fid_v[3],fid_v[4],fid_v[5])
#dataset = dh.ConvertWC('shower3D_signal_6.root')
#^^ Coverts Wirecell data tree into a numpyarray
print 'predataset size ', len(predataset)
dataset = dh.Unique(predataset)
print 'dataset size ', len(dataset)

# Prefilter 

import prefilter as pf 

#pfl = pf.VoxalizeData(dataset,10,10,10)

# Add some clustering algos
import Clustering.protocluster as pc
labels = pc.crawler(dataset,8.,10)
#print ' Total clusters ' 
print len(np.unique(labels))
print labels


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
style.use("ggplot")
colors = 10*['r','g','b','c','k','y','m']



#Shit hack for now
# this is realll bad
import collections as col

shi = col.Counter(labels)
# Shi is a set, and dic lookup 
cval = [x[0] for x in shi.items() if x[1]>100]
print cval
datasetidx_v = []
for s in cval: 
    [datasetidx_v.append(i) for i, j in enumerate(labels) if j == s]
	#jiif i == s:
	   # datasetidx_v.append(i)
#print' datat set idx '
#print datasetidx_v


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in datasetidx_v:
#for i in range(len(dataset)):
    #ax.scatter(dataset[i][0], dataset[i][1], dataset[i][2]])
    #ax.scatter(dataset[i][0], dataset[i][1], dataset[i][2], marker='o')
    ax.scatter(dataset[i][0], dataset[i][1], dataset[i][2], c=colors[labels[i]], marker='o')
ax.set_xlabel('X ')
ax.set_ylabel('Y ')
ax.set_zlabel('Z ')

plt.show()

