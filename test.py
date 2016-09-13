import sys, os
import numpy as np
import Utils.datahandle as dh
    
print sys.argv[1]

#bring in the data
predataset = dh.ConvertWC_InTPC('{}'.format(sys.argv[1]))
#predataset = dh.ConvertWC('{}'.format(sys.argv[1]))
#dataset = dh.ConvertWC_points('{}'.format(sys.argv[1]))
#dataset = dh.ConvertWC('{}'.format(sys.argv[1]))
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
#colors = 20*['r','g','b','c','k','y','m']
labels = pc.crawler(dataset,8.,10)
#labels = pc.dbscan(dataset,2.,100)
#print ' Total clusters ' 
print len(np.unique(labels))
print labels


'''
# Add some clustering algos
import protocluster as pc


# Visualize the events 

#Define Labels 
#labels = kmlabels
labels = mslabels

'''

#Shit hack for now
# this is realll bad
# Add this into the utilities 
import collections as col
shi = col.Counter(labels)
# Shi is a set, and dic lookup 
cval = [x[0] for x in shi.items() if x[1]>100]
print cval
datasetidx_v = []
for s in cval:
    [datasetidx_v.append(i) for i, j in enumerate(labels) if j == s]
# Make custers with index

#################
import SParams.axisfit as axfi

axfi.firstfit(dataset,datasetidx_v)



import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
style.use("ggplot")
colors = 10*['r','g','b','c','k','y','m']


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in datasetidx_v:
#for i in range(len(dataset)):
    #ax.scatter(dataset[i][0], dataset[i][1], dataset[i][2]])
    #ax.scatter(dataset[i][0], dataset[i][1], dataset[i][2], marker='o')
    #ax.scatter(pfl[i][0], pfl[i][1], pfl[i][2],  marker='o')
    ax.scatter(dataset[i][0], dataset[i][1], dataset[i][2], c=colors[labels[i]], marker='o')
ax.set_xlabel('X ')
ax.set_ylabel('Y ')
ax.set_zlabel('Z ')

plt.show()

