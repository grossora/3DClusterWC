from sklearn.cluster import KMeans , MeanShift
import numpy as np


############################################
#######Make the Numpy array ################
############################################
def MakeNPA(nar, lab):
    listofclusters = []
    for i in range(max(lab)+1):
        emptylist = []
        listofclusters.append(emptylist)
    for a in range(len(nar)):
        xyz = [nar[a][0],nar[a][1],nar[a][2]]
        listofclusters[lab[a]].append(xyz)
    return listofclusters

############################################
#### K Means Clustering ####################
############################################
def kmeansNCluster(inup, nclusters):
    est = KMeans(n_clusters=nclusters)
    est.fit(inup)
    labels = est.labels_
    return labels

def kmeans(inup):
    est = KMeans()
    est.fit(inup)
    labels = est.labels_
    return labels
 
############################################
############################################
############################################
def meanshift(inup):
    ms = MeanShift()
    ms.fit(inup)
    labels = ms.labels_
    return labels

############################################
######### DB Clustering ####################
############################################
from sklearn.cluster import DBSCAN
def dbscan(inup, dist, minsample ):
    #db = DBSCAN(dist).fit(inup)
    #db = DBSCAN(dist, minsample).fit(inup)
    db = DBSCAN(eps=dist, min_samples=minsample, algorithm='brute').fit(inup)
    #db = DBSCAN(eps=dist, min_samples=minsample).fit(inup)
    labels = db.labels_
    return labels

############################################
######### crawler Clustering ###############
############################################
def crawler(inup, dist, mincluster ):
    indexlist = [-1 for x in range(len(inup))] 
    unusedlist = [x for x in range(len(inup))] 
    clusterlabel = 0
    mindist = pow(dist,2) # This will save us from computing a square root on 
    for pt in range(len(inup)):
	#see if this point is already used
	if not pt in unusedlist:
	    continue
	# Make a temp list for potential merged points 
	tmpmerge = []
	tmpmerge.append(pt)
	#Push back on a temp list... next version#### RG
	mergedpts = False# This is here now.. we can remove this later

	# remove pt from unused list 
	ptindex = unusedlist.index(pt)
	unusedlist.pop(ptindex)

	# Now crawthough all the rest of the points
	boo = True    ### Is this needed? 
	while boo: # This is going to take long... but it's like a clean up
	    tmp_copy = len(tmpmerge)	
	    for testpt in unusedlist:
	        # Check distances  
	        # here we are going to check all the list of points in the tmp until we either end of find a close point
	        for other in tmpmerge: 
	            distsqrd = pow(inup[other][0]-inup[testpt][0],2) + pow(inup[other][1]-inup[testpt][1],2) + pow(inup[other][2]-inup[testpt][2],2) 
	            if distsqrd<mindist:
	 	        #Merge them into the current cluster 
		        #The index in index list becomes whatever the cluster counter is
		        tmpmerge.append(testpt)
		        #now get out and move to next point to consider
		        break
	    if len(tmpmerge)>mincluster:# this is not the best way to do this but for now its ok 
	    # if we make it to pass the if that means we are going to make cluster
	    # so it does not matter if we clean up the unusedlist here 
	        for s in tmpmerge: 
		    if s ==0:# this is the pt and it is not in unused
			continue
		    # Check if it is in the list
		    if s in unusedlist:
			# clear it out of the unused list since it is not used
		        iv = unusedlist.index(s)
		        unusedlist.pop(iv)
		
	    # if we are at a steady state then get out of this
	    if tmp_copy==len(tmpmerge):
		boo = False # is this needed? Wont break just take us out? 
		break
	

	if len(tmpmerge)>=mincluster:
	    #label the points 
	    for s in tmpmerge:
		indexlist[s] = clusterlabel	
	    clusterlabel+=1
	    #remove from unused list 

	    # We already did this
	# we need a catch to put back the tmpperge points into unused if we do not pass the min cluster
##########
	if len(tmpmerge)<mincluster:
	    for b in tmpmerge:
		unusedlist.append(b)
##########   
	
    return indexlist
		
	












 






