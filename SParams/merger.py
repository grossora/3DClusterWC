import numpy as np 
import collections as col
import axisfit as axfi
import selpizero as selpz
from sklearn.decomposition import PCA



def PCA_merge(dataset,labels,datasetidx_holder):
    pca_holder = []
    # This is hard code need to be writted better
    min_angle_merge = 0.3
    for d in datasetidx_holder:
        dd = []
        for s in d:
            t = [dataset[s][0],dataset[s][1],dataset[s][2]]
            dd.append(t)
        pca = PCA(n_components=1)
        pca.fit(dd)
        pca_holder.append(pca.components_)
    # now do the grouping

    mergedpairs = []
    for a in xrange(0,len(pca_holder)):
        shrA = axfi.showerfit(dataset,datasetidx_holder[a])
        for b in xrange(a+1,len(pca_holder)):
            shrB = axfi.showerfit(dataset,datasetidx_holder[b])
            vertex = selpz.findvtx(shrA,shrB)
            angle = selpz.openingangle(shrA,shrB,vertex)
            if angle <min_angle_merge:
                pair = [a,b]
                mergedpairs.append(pair)
    # Merge together some showers
    # that share nodes
    lists = mergedpairs
    resultlist = []
    if len(lists) >= 1: # If your list is empty then you dont need to do anything.
        resultlist = [lists[0]] #Add the first item to your resultset
        if len(lists) > 1: #If there is only one list in your list then you dont need to do anything.
            for l in lists[1:]: #Loop through lists starting at list 1
                listset = set(l) #Turn you list into a set
                merged = False #Trigger
                for index in range(len(resultlist)): #Use indexes of the list for speed.
                    rset = set(resultlist[index]) #Get list from you resultset as a set
                    if len(listset & rset) != 0: #If listset and rset have a common value then the len will be greater than 1
                        resultlist[index] = list(listset | rset) #Update the resultlist with the updated union of listset and rset
                        merged = True #Turn trigger to True
                        break #Because you found a match there is no need to continue the for loop.
                if not merged: #If there was no match then add the list to the resultset, so it doesnt get left out.
                    resultlist.append(l)

    # Connect all of these into a holder
    for s in resultlist:
        #print 'These below will all be merged '
        matchlabel = labels[datasetidx_holder[s[0]][0]] # grabbing the cluster index from datasetholder using s[0] and looking at the first point in that cluster to get the label
        for z in xrange(1,len(s)):
            print s[z]
            for dlab in datasetidx_holder[z]:
                labels[dlab] = matchlabel

    return labels

def label_to_idxholder(labels,thresh):
    shi = col.Counter(labels)
    # Shi is a set, and dic lookup 
    cval = [x[0] for x in shi.items() if x[1]>thresh]
    datasetidx_holder = []
    datasetidx_v = []
    for s in cval:
        datasetidx_v=[]
        [datasetidx_v.append(i) for i,j in enumerate(labels) if j==s]
        datasetidx_holder.append(datasetidx_v)
    return datasetidx_holder

