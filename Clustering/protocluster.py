from sklearn.cluster import KMeans , MeanShift
import numpy as np
from operator import itemgetter





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
        # we need a catch to put back the tmpperge points into unused if we do not pass the min cluster
#########   
    return indexlist




############################################
######### crawler nn     ###############
############################################
def crawlernn(inup, dist, min_cls ):

    #######
    #### some stuff at the start that won't change
    #######
    clusterlabel = 0
    indexlist = [-1 for x in range(len(inup))]
    distsq_max = pow(dist,2)
    def nn(pta,ptb):
	distsq = pow(pta[1]-ptb[1],2) + pow(pta[2]-ptb[2],2) + pow(pta[3]-ptb[3],2)
	if distsq < distsq_max:
	    return True
    #######
    #### some stuff at the start that won't change
    #######

    # Happens once
    unusedlist = [(x,inup[x][0],inup[x][1],inup[x][2]) for x in range(len(inup))]
    ## First sort the list based on z position since is it has the most spread
    unusedlist.sort(key=itemgetter(3))
    
### Work comes back to here
#### While unusedlist > min_cls

    while len(unusedlist)>min_cls:

	#Find the minium and max  batch for z
	minbatch_z = unusedlist[0][3]
	#This makes the batch list for unused to work with. 
	unused_batchlist = [x for x in unusedlist if x[3]<minbatch_z+dist]
	# Since it's sorted we can Use the last point as the farthest away point. 
	maxbatch_z = unused_batchlist[-1][3]

	### Now make the added points list
	unused = unused_batchlist
	#Start a cluster
	temp_cluster = [unused[0]]
	#Start wit this added  point
	added_points =  [temp_cluster[0]]
	# remove it from the unused list since we will be uing it in the cluster
	unused.pop(0)

	temp_maxbatch_z = maxbatch_z
        while len(added_points)!=0:
	    tmp_added = []
	    for a in added_points:
	        #### Get some stuff for NN
	        tmp_unused = []
	        for u in unused:
		    if nn(a,u):
		        tmp_added.append(u)
		        temp_cluster.append(u)
		    if not nn(a,u):
		        tmp_unused.append(u)
	        unused = tmp_unused
	        # Readjust the unused by adding extra points 
	        # Add points that are distance max z of temp cluster +dist
	        # this is going to be a time succk... but we need it for hookes with tracks on boundaries 

	    tunused = [x for x in unusedlist if  x[3] < max(temp_cluster,key=itemgetter(3))[3]+dist]
	    # Now remove the entries from front bactch that are already in the temp cluster
	    unused = [x for x in tunused if x not in temp_cluster]
	    added_points = tmp_added
	    

        # When getting out of the While we should have we have to clean up
        if len(temp_cluster) >= min_cls:
	    for idx in temp_cluster:
	        # Looping over the temp cluster and filling out the cluster label for the at the index in the index list
	        indexlist[idx[0]] = clusterlabel
	    # KEep it and remove these points from the unused list
	    clusterlabel+=1
	    unusedlist = [x for x in unusedlist if x not in temp_cluster]
	
        if len(temp_cluster) < min_cls:
	    unusedlist = [x for x in unusedlist if x not in temp_cluster]
	# Still remove points from the unused
	# because this means we tried them
    ### The unused list should still remain sorted... so we can just pick up with the next batch step	
    return indexlist


