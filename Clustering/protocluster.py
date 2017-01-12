from sklearn.cluster import KMeans , MeanShift
import numpy as np
from operator import itemgetter
from scipy.spatial import distance
from scipy.spatial import ConvexHull
import SParams.axisfit as axfi
import math as math






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

def hull_check(points):
    # Here we ant it to return the dimension number
    # Take in the set of points
    # loop over all points and make sure that there are 3 dim
    x_p = -10000
    y_p = -10000
    z_p = -10000
    x_good = False
    y_good = False
    z_good = False
    for pt in points:
        if x_p == -10000:
            x_p = pt[0]
            y_p = pt[1]
            z_p = pt[2]
            continue
        # This is not the correct algo.... it needs more
        if x_p !=pt[0] and not x_good:
            x_good = True
        if y_p !=pt[1] and not y_good:
            y_good = True
        if z_p !=pt[2] and not z_good:
            z_good = True
        if x_good and y_good and z_good:
            return 3
        x_p = pt[0]
        y_p = pt[1]
        z_p = pt[2]
    boolv= [x_good,y_good,z_good]
    if len([ i for i in boolv if i==True])==2:
        return 2
    if len([ i for i in boolv if i==True])==1:
        return 1
    if len([ i for i in boolv if i==True])==0:
        return 0
    # This really needs to be n+1 for checking dimensionality.... but we might get lucky ror now.


def Track_Stitcher(dataset,datasetidx_holder,labels):
    # What is tunable
    # min_dist ==> min dist for the vertex points of two different hulls to be considered
    min_dist = 10  # RG Magic
    # k_radius ==> radius of the sphere around the vertex point looking at clustered charge for that hull
    k_radius = 5  # RG Hard Coded
    #k_radius = 10  # RG Hard Coded
    CHQ_vec = []
    # ^^^^^^ Will be of the form [    [datasetidx_holder INDEX, the vertices of the hull, total_charge] ]
    for a in range(len(datasetidx_holder)):
        points_v = []
        tot_q = 0.0
        for i in datasetidx_holder[a]:
            pt = [ dataset[i][0],dataset[i][1],dataset[i][2]]
            points_v.append(pt)
            tot_q+= dataset[i][3]

        if hull_check(points_v)!=3:
            # Bail out and give up on hull
	    return datasetidx_holder, labels

        hull = ConvexHull(points_v)
        # Fill up the CHQ_V     
        ds_hull_idx = [datasetidx_holder[a][i] for i in list(hull.vertices)]
        chq = [a,ds_hull_idx,tot_q]
        CHQ_vec.append(chq)

    clust_merge_plex = [] # Pairs of local clusters that need to be merged There are from the id from the datasetidx_holder labels
    for a in range(len(CHQ_vec)):
        # Get the first 
        first_CHQ = CHQ_vec[a]
        for b in xrange(a+1,len(CHQ_vec)):
            second_CHQ = CHQ_vec[b]
            # Find the closest points between the two hulls
            cur_smallest_dist = 1000000. # This stays hardcoded as a maximum
            cur_pair = []
            for i in range(len(first_CHQ[1])):
                for j in range(len(second_CHQ[1])):
                    test_dist = distance.euclidean([dataset[first_CHQ[1][i]][0],dataset[first_CHQ[1][i]][1],dataset[first_CHQ[1][i]][2]],[dataset[second_CHQ[1][j]][0],dataset[second_CHQ[1][j]][1],dataset[second_CHQ[1][j]][2]])
                    if  test_dist<min_dist and test_dist<cur_smallest_dist:
                        print 'test distance in min!!!!!!!!!!!', str(test_dist)
                        cur_smallest_dist = test_dist
                        cur_pair = [i,j] # This is the idx value that should corespond to dataset for this pair of hull vertices
            if len(cur_pair)==0:
                #we didn't get anything to match
                continue
            # If we have a pair... look at the NN points in each hull seperatly
            #.... then get local PCA... and compare

            # First vertex  position in the CHQ_vec
            clst_label_a = first_CHQ[0] # This is the label coresponding to which posiition in the holder    
            clst_indexs_a = first_CHQ[1] # This is a list of index for this cluster... index of datasets
            vp_idx_a = first_CHQ[1][cur_pair[0]] # This is the ds index for the vertex in question
             # second vertex  position in the CHQ_vec
            clst_label_b = second_CHQ[0]        # This is the label coresponding to which posiition in the holder    
            clst_indexs_b =  second_CHQ[1] # This is a list of index for this cluster... index of datasets
            vp_idx_b = second_CHQ[1][cur_pair[1]] # This is the ds index for the vertex in question

            #Find PCA for local points

            #Find First PCA 
            local_pts_idx_a = []
            for i in clst_indexs_a:
                k_dist = distance.euclidean([dataset[i][0],dataset[i][1],dataset[i][2]],[dataset[vp_idx_a][0],dataset[vp_idx_a][1],dataset[vp_idx_a][2]])
                if k_dist<k_radius:
                    local_pts_idx_a.append(i)
            # Find the PCA
	    print 'size of local pca A' , str(len(local_pts_idx_a))
            local_PCA_a = [-999]
            local_PCA_dir_a = [-999]
            try:
                local_PCA_a = axfi.PCAParams(dataset,local_pts_idx_a,3)
                local_PCA_dir_a = axfi.PCAParams_dir(dataset,local_pts_idx_a,3)
            except:
                print 'Opps we dont have a pca'
                local_PCA_a = [-999]
                continue

            #Find second PCA 
            local_pts_idx_b = []
            for i in clst_indexs_b:
                k_dist = distance.euclidean([dataset[i][0],dataset[i][1],dataset[i][2]],[dataset[vp_idx_b][0],dataset[vp_idx_b][1],dataset[vp_idx_b][2]])
                if k_dist<k_radius:
                    local_pts_idx_b.append(i)
            # Find the PCA
	    print 'size of local pca B' , str(len(local_pts_idx_b))
            #local_PCA_a = [-999]  ##### This is a typo
            local_PCA_b = [-999]
            local_PCA_dir_b = [-999]
            try:
                local_PCA_b = axfi.PCAParams(dataset,local_pts_idx_b,3)
                local_PCA_dir_b = axfi.PCAParams_dir(dataset,local_pts_idx_b,3)
            except:
                print 'Opps we dont have a pca'
                local_PCA_b = [-999]
                continue

            if len(local_PCA_a)<3 and len(local_PCA_b)<3:
                print ' unable merge since pca is too small degress of freedom '
		continue

            # Check if the PCA's are similiar... 
            # we want to check that the first compoent is similiar in straighness? ?
            # compentes_ are the direction 
            # explained_variance_ratio_ is the straightness

	    '''
            # RG
            #check that the delta x,y,z's are small 
            print '========'
            print '== A ==='
            print local_PCA_dir_a
            print '-------'
            print local_PCA_dir_a[0]
            print '========'
            print '== B ==='
            print local_PCA_dir_b
            print '-------'
            print local_PCA_dir_b[0]
            print '========'
	    '''
            # Take the dot between the two angles
            dotp = 0.0
            for i in range(3):
                 dotp += local_PCA_dir_a[0][i]*local_PCA_dir_b[0][i]

            # Take the Abs, and then figure out a cut. 
            dotp = math.fabs(dotp)

            print 'this is the dotp'
            print dotp
            #min_dotp = 0.9  # RG Magic number
            min_dotp = 0.96  # RG Magic number
            #min_dotp = 0.95  # RG Magic number
            if dotp < min_dotp:
                print 'Local pca do not ad up'
                continue
            # Now we have found that these two need to get merged together. 
            clust_merge_plex.append([clst_label_a,clst_label_b])

    # Put together the clusters that should be merged
    clust_merge_plex = sorted([sorted(x) for x in clust_merge_plex])
    resultlist = []
    if len(clust_merge_plex) >= 1: # If your list is empty then you dont need to do anything.
        resultlist = [clust_merge_plex[0]] #Add the first item to your resultset
        if len(clust_merge_plex) > 1: #If there is only one list in your list then you dont need to do anything.
            for l in clust_merge_plex[1:]: #Loop through lists starting at list 1
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

    ####### Reassign all labels for the results list
    for pa in resultlist:
        # First one keeps the label
        clusterlabel = pa[0]
        # These already should all have the same labels
        cluster_idx_positions =  datasetidx_holder[clusterlabel]
        # This gets the label value for the cluster
        labels_label = labels[cluster_idx_positions[0]]
	
	# Test check 
	test_labels = [labels[cluster_idx_positions[x]] for x in range(len(cluster_idx_positions))]
        print ' ' 
        print ' ' 
        print 'Test labels' 
	print test_labels


	# pa is an index in a holder

        nclusterlabels = [ pa[x] for x in xrange(1,len(pa))]
	idxlabels_to_change = []
	for i in nclusterlabels:
	    for l in datasetidx_holder[i]:
	        idxlabels_to_change.append(l)
		
		
        for lab in range(len(labels)):
            clab = labels[lab]
            # Loop over the ncluster labels to check
            for tc in idxlabels_to_change:
            #for tc in nclusterlabels:
                if labels[tc]==clab:
                #if tc==clab:
                    # Make this position label value labels_label
                    labels[lab]=labels_label

    new_holder = []
    for pa in resultlist:
	temp_new_holder = []
	for cpos in pa:
	    idx_positions = datasetidx_holder[cpos]
	    [temp_new_holder.append(i) for i in idx_positions]
        new_holder.append(temp_new_holder) 		

    # Remove the older clusters from the index holde
    remove_holder = [item for sublist in resultlist for item in sublist]
    new_datasetidx_holder = [ datasetidx_holder[a] for a in xrange(len(datasetidx_holder)) if a not in remove_holder]
    # Next add on the new holder
    for i in new_holder:
	new_datasetidx_holder.append(i)

    return new_datasetidx_holder,labels


#====================================================================================================================================
#====================================================================================================================================
#====================================================================================================================================


def Track_Stitcher_v2(dataset,datasetidx_holder,labels):
    # What is tunable
    # min_dist ==> min dist for the vertex points of two different hulls to be considered
    min_dist = 10  # RG Magic
    # k_radius ==> radius of the sphere around the vertex point looking at clustered charge for that hull
    k_radius = 5  # RG Hard Coded
    #k_radius = 10  # RG Hard Coded
    # delta_length ==> maximum allowed distance to pass for the sticking displacement... this can be small  
    max_delta = 1
    CHQ_vec = []
    # ^^^^^^ Will be of the form [    [datasetidx_holder INDEX, the vertices of the hull, total_charge] ]
    for a in range(len(datasetidx_holder)):
        points_v = []
        tot_q = 0.0
        for i in datasetidx_holder[a]:
            pt = [ dataset[i][0],dataset[i][1],dataset[i][2]]
            points_v.append(pt)
            tot_q+= dataset[i][3]

        if hull_check(points_v)!=3:
            # Bail out and give up on hull
	    return datasetidx_holder, labels

        hull = ConvexHull(points_v)
        # Fill up the CHQ_V     
        ds_hull_idx = [datasetidx_holder[a][i] for i in list(hull.vertices)]
        chq = [a,ds_hull_idx,tot_q]
        CHQ_vec.append(chq)

    clust_merge_plex = [] # Pairs of local clusters that need to be merged There are from the id from the datasetidx_holder labels
    for a in range(len(CHQ_vec)):
        # Get the first 
        first_CHQ = CHQ_vec[a]
        for b in xrange(a+1,len(CHQ_vec)):
            second_CHQ = CHQ_vec[b]
            # Find the closest points between the two hulls
            cur_smallest_dist = 1000000. # This stays hardcoded as a maximum
            cur_pair = []
            for i in range(len(first_CHQ[1])):
                for j in range(len(second_CHQ[1])):
                    test_dist = distance.euclidean([dataset[first_CHQ[1][i]][0],dataset[first_CHQ[1][i]][1],dataset[first_CHQ[1][i]][2]],[dataset[second_CHQ[1][j]][0],dataset[second_CHQ[1][j]][1],dataset[second_CHQ[1][j]][2]])
                    if  test_dist<min_dist and test_dist<cur_smallest_dist:
                        print 'test distance in min!!!!!!!!!!!', str(test_dist)
                        cur_smallest_dist = test_dist
                        cur_pair = [i,j] # This is the idx value that should corespond to dataset for this pair of hull vertices
            if len(cur_pair)==0:
                #we didn't get anything to match
                continue
            # If we have a pair... look at the NN points in each hull seperatly
            #.... then get local PCA... and compare

            # First vertex  position in the CHQ_vec
            clst_label_a = first_CHQ[0] # This is the label coresponding to which posiition in the holder    
            clst_indexs_a = first_CHQ[1] # This is a list of index for this cluster... index of datasets
            vp_idx_a = first_CHQ[1][cur_pair[0]] # This is the ds index for the vertex in question
             # second vertex  position in the CHQ_vec
            clst_label_b = second_CHQ[0]        # This is the label coresponding to which posiition in the holder    
            clst_indexs_b =  second_CHQ[1] # This is a list of index for this cluster... index of datasets
            vp_idx_b = second_CHQ[1][cur_pair[1]] # This is the ds index for the vertex in question

            #Find PCA for local points

            #Find First PCA 
            local_pts_idx_a = []
            for i in clst_indexs_a:
                k_dist = distance.euclidean([dataset[i][0],dataset[i][1],dataset[i][2]],[dataset[vp_idx_a][0],dataset[vp_idx_a][1],dataset[vp_idx_a][2]])
                if k_dist<k_radius:
                    local_pts_idx_a.append(i)
            # Find the PCA
	    print 'size of local pca A' , str(len(local_pts_idx_a))
            local_PCA_a = [-999]
            local_PCA_dir_a = [-999]
            try:
                local_PCA_a = axfi.PCAParams(dataset,local_pts_idx_a,3)
                local_PCA_dir_a = axfi.PCAParams_dir(dataset,local_pts_idx_a,3)
            except:
                print 'Opps we dont have a pca'
                local_PCA_a = [-999]
                continue

            #Find second PCA 
            local_pts_idx_b = []
            for i in clst_indexs_b:
                k_dist = distance.euclidean([dataset[i][0],dataset[i][1],dataset[i][2]],[dataset[vp_idx_b][0],dataset[vp_idx_b][1],dataset[vp_idx_b][2]])
                if k_dist<k_radius:
                    local_pts_idx_b.append(i)
            # Find the PCA
	    print 'size of local pca B' , str(len(local_pts_idx_b))
            #local_PCA_a = [-999]  ##### This is a typo
            local_PCA_b = [-999]
            local_PCA_dir_b = [-999]
            try:
                local_PCA_b = axfi.PCAParams(dataset,local_pts_idx_b,3)
                local_PCA_dir_b = axfi.PCAParams_dir(dataset,local_pts_idx_b,3)
            except:
                print 'Opps we dont have a pca'
                local_PCA_b = [-999]
                continue

            if len(local_PCA_a)<3 and len(local_PCA_b)<3:
                print ' unable merge since pca is too small degress of freedom '
		continue

            # Check if the PCA's are similiar... 
            # we want to check that the first compoent is similiar in straighness? ?
            # compentes_ are the direction 
            # explained_variance_ratio_ is the straightness

	    '''
            # RG
            #check that the delta x,y,z's are small 
            print '========'
            print '== A ==='
            print local_PCA_dir_a
            print '-------'
            print local_PCA_dir_a[0]
            print '========'
            print '== B ==='
            print local_PCA_dir_b
            print '-------'
            print local_PCA_dir_b[0]
            print '========'
	    '''

	    ##### Take cluster A
	    
	    # Calculate position of ProjectA hullvtx +/- pca*abs(vtxA-vtxB)
	    # Calculate Delta between (ProjA_plus/minus - vtxB) 
	    # Calculate position of ProjectB hullvtx +/- pca*abs(vtxA-vtxB)
	    # Calculate Delta between (ProjB_plus/minus - vtxA) 
	    vtx_A =  np.asarray([dataset[vp_idx_a][0],dataset[vp_idx_a][1],dataset[vp_idx_a][2]])
	    vtx_B =  np.asarray([dataset[vp_idx_b][0],dataset[vp_idx_b][1],dataset[vp_idx_b][2]])
	    Length_between_vtx = distance.euclidean(vtx_A,vtx_B)
            projA_plus = vtx_A + np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_a)
            projA_minus = vtx_A - np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_a)
            projB_plus = vtx_B + np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_b)
            projB_minus = vtx_B - np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_b)

	    # Deltas
	    deltaAB_plus = distance.euclidean(projA_plus,vtx_B)
	    deltaAB_minus = distance.euclidean(projA_minus,vtx_B)
	    deltaBA_plus = distance.euclidean(projB_plus,vtx_A)
	    deltaBA_minus = distance.euclidean(projB_minus,vtx_A)

	    AB = False
	    BA = False
	    if deltaAB_plus < max_delta or deltaAB_minus <max_delta:
		AB = True

	    if deltaBA_plus < max_delta or deltaBA_minus <max_delta:
		BA = True

	    if not AB :
                print 'did not pass prjection AB'
                continue

	    if not BA :
                print 'did not pass prjection BA'
                continue



            # Take the dot between the two angles
            dotp = 0.0
            for i in range(3):
                 dotp += local_PCA_dir_a[0][i]*local_PCA_dir_b[0][i]

            # Take the Abs, and then figure out a cut. 
            dotp = math.fabs(dotp)

            print 'this is the dotp'
            print dotp
            #min_dotp = 0.9  # RG Magic number
            min_dotp = 0.96  # RG Magic number
            #min_dotp = 0.95  # RG Magic number
            if dotp < min_dotp:
                print 'Local pca do not ad up'
                continue
            # Now we have found that these two need to get merged together. 
            clust_merge_plex.append([clst_label_a,clst_label_b])

    # Put together the clusters that should be merged
    clust_merge_plex = sorted([sorted(x) for x in clust_merge_plex])
    resultlist = []
    if len(clust_merge_plex) >= 1: # If your list is empty then you dont need to do anything.
        resultlist = [clust_merge_plex[0]] #Add the first item to your resultset
        if len(clust_merge_plex) > 1: #If there is only one list in your list then you dont need to do anything.
            for l in clust_merge_plex[1:]: #Loop through lists starting at list 1
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

    ####### Reassign all labels for the results list
    for pa in resultlist:
        # First one keeps the label
        clusterlabel = pa[0]
        # These already should all have the same labels
        cluster_idx_positions =  datasetidx_holder[clusterlabel]
        # This gets the label value for the cluster
        labels_label = labels[cluster_idx_positions[0]]
	
	# Test check 
	test_labels = [labels[cluster_idx_positions[x]] for x in range(len(cluster_idx_positions))]
        print ' ' 
        print ' ' 
        print 'Test labels' 
	print test_labels


	# pa is an index in a holder

        nclusterlabels = [ pa[x] for x in xrange(1,len(pa))]
	idxlabels_to_change = []
	for i in nclusterlabels:
	    for l in datasetidx_holder[i]:
	        idxlabels_to_change.append(l)
		
		
        for lab in range(len(labels)):
            clab = labels[lab]
            # Loop over the ncluster labels to check
            for tc in idxlabels_to_change:
            #for tc in nclusterlabels:
                if labels[tc]==clab:
                #if tc==clab:
                    # Make this position label value labels_label
                    labels[lab]=labels_label
	

    new_holder = []
    for pa in resultlist:
	temp_new_holder = []
	for cpos in pa:
	    idx_positions = datasetidx_holder[cpos]
	    [temp_new_holder.append(i) for i in idx_positions]
        new_holder.append(temp_new_holder) 		

    # Remove the older clusters from the index holde
    remove_holder = [item for sublist in resultlist for item in sublist]
    new_datasetidx_holder = [ datasetidx_holder[a] for a in xrange(len(datasetidx_holder)) if a not in remove_holder]
    # Next add on the new holder
    for i in new_holder:
	new_datasetidx_holder.append(i)

    return new_datasetidx_holder,labels



def Track_VOX_Stitcher_v2(dataset,datasetidx_holder,labels):
    # What is tunable
    # min_dist ==> min dist for the vertex points of two different hulls to be considered
    min_dist = 10  # RG Magic
    # k_radius ==> radius of the sphere around the vertex point looking at clustered charge for that hull
    k_radius = 20  # RG Hard Coded
    #k_radius = 10  # RG Hard Coded
    # delta_length ==> maximum allowed distance to pass for the sticking displacement... this can be small  
    max_delta = 1
    CHQ_vec = []
    # ^^^^^^ Will be of the form [    [datasetidx_holder INDEX, the vertices of the hull, total_charge] ]
    for a in range(len(datasetidx_holder)):
        points_v = []
        tot_q = 0.0
        for i in datasetidx_holder[a]:
            pt = [ dataset[i][0],dataset[i][1],dataset[i][2]]
            points_v.append(pt)
            tot_q+= dataset[i][3]

        if hull_check(points_v)!=3:
            # Bail out and give up on hull
	    return datasetidx_holder, labels

        hull = ConvexHull(points_v)
        # Fill up the CHQ_V     
        ds_hull_idx = [datasetidx_holder[a][i] for i in list(hull.vertices)]
        chq = [a,ds_hull_idx,tot_q]
        CHQ_vec.append(chq)

    clust_merge_plex = [] # Pairs of local clusters that need to be merged There are from the id from the datasetidx_holder labels
    for a in range(len(CHQ_vec)):
        # Get the first 
        first_CHQ = CHQ_vec[a]
        for b in xrange(a+1,len(CHQ_vec)):
            second_CHQ = CHQ_vec[b]
            # Find the closest points between the two hulls
            cur_smallest_dist = 1000000. # This stays hardcoded as a maximum
            cur_pair = []
            for i in range(len(first_CHQ[1])):
                for j in range(len(second_CHQ[1])):
                    test_dist = distance.euclidean([dataset[first_CHQ[1][i]][0],dataset[first_CHQ[1][i]][1],dataset[first_CHQ[1][i]][2]],[dataset[second_CHQ[1][j]][0],dataset[second_CHQ[1][j]][1],dataset[second_CHQ[1][j]][2]])
                    if  test_dist<min_dist and test_dist<cur_smallest_dist:
                        print 'test distance in min!!!!!!!!!!!', str(test_dist)
                        cur_smallest_dist = test_dist
                        cur_pair = [i,j] # This is the idx value that should corespond to dataset for this pair of hull vertices
            if len(cur_pair)==0:
                #we didn't get anything to match
                continue
            # If we have a pair... look at the NN points in each hull seperatly
            #.... then get local PCA... and compare

            # First vertex  position in the CHQ_vec
            clst_label_a = first_CHQ[0] # This is the label coresponding to which posiition in the holder    
            clst_indexs_a = first_CHQ[1] # This is a list of index for this cluster... index of datasets
            vp_idx_a = first_CHQ[1][cur_pair[0]] # This is the ds index for the vertex in question
             # second vertex  position in the CHQ_vec
            clst_label_b = second_CHQ[0]        # This is the label coresponding to which posiition in the holder    
            clst_indexs_b =  second_CHQ[1] # This is a list of index for this cluster... index of datasets
            vp_idx_b = second_CHQ[1][cur_pair[1]] # This is the ds index for the vertex in question

            #Find PCA for local points

            #Find First PCA 
            local_pts_idx_a = []
            for i in clst_indexs_a:
                k_dist = distance.euclidean([dataset[i][0],dataset[i][1],dataset[i][2]],[dataset[vp_idx_a][0],dataset[vp_idx_a][1],dataset[vp_idx_a][2]])
                if k_dist<k_radius:
                    local_pts_idx_a.append(i)
            # Find the PCA
	    print 'size of local pca A' , str(len(local_pts_idx_a))
            local_PCA_a = [-999]
            local_PCA_dir_a = [-999]
            try:
                local_PCA_a = axfi.PCAParams(dataset,local_pts_idx_a,3)
                local_PCA_dir_a = axfi.PCAParams_dir(dataset,local_pts_idx_a,3)
            except:
                print 'Opps we dont have a pca'
                local_PCA_a = [-999]
                continue

            #Find second PCA 
            local_pts_idx_b = []
            for i in clst_indexs_b:
                k_dist = distance.euclidean([dataset[i][0],dataset[i][1],dataset[i][2]],[dataset[vp_idx_b][0],dataset[vp_idx_b][1],dataset[vp_idx_b][2]])
                if k_dist<k_radius:
                    local_pts_idx_b.append(i)
            # Find the PCA
	    print 'size of local pca B' , str(len(local_pts_idx_b))
            #local_PCA_a = [-999]  ##### This is a typo
            local_PCA_b = [-999]
            local_PCA_dir_b = [-999]
            try:
                local_PCA_b = axfi.PCAParams(dataset,local_pts_idx_b,3)
                local_PCA_dir_b = axfi.PCAParams_dir(dataset,local_pts_idx_b,3)
            except:
                print 'Opps we dont have a pca'
                local_PCA_b = [-999]
                continue

            if len(local_PCA_a)<3 or len(local_PCA_b)<3:
            #if len(local_PCA_a)<3 and len(local_PCA_b)<3:
                print ' unable merge since pca is too small degress of freedom '
		continue

            # Check if the PCA's are similiar... 
            # we want to check that the first compoent is similiar in straighness? ?
            # compentes_ are the direction 
            # explained_variance_ratio_ is the straightness

	    '''
            # RG
            #check that the delta x,y,z's are small 
            print '========'
            print '== A ==='
            print local_PCA_dir_a
            print '-------'
            print local_PCA_dir_a[0]
            print '========'
            print '== B ==='
            print local_PCA_dir_b
            print '-------'
            print local_PCA_dir_b[0]
            print '========'
	    '''

	    ##### Take cluster A
	    
	    # Calculate position of ProjectA hullvtx +/- pca*abs(vtxA-vtxB)
	    # Calculate Delta between (ProjA_plus/minus - vtxB) 
	    # Calculate position of ProjectB hullvtx +/- pca*abs(vtxA-vtxB)
	    # Calculate Delta between (ProjB_plus/minus - vtxA) 
	    vtx_A =  np.asarray([dataset[vp_idx_a][0],dataset[vp_idx_a][1],dataset[vp_idx_a][2]])
	    vtx_B =  np.asarray([dataset[vp_idx_b][0],dataset[vp_idx_b][1],dataset[vp_idx_b][2]])
	    Length_between_vtx = distance.euclidean(vtx_A,vtx_B)
            projA_plus = vtx_A + np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_a)
            projA_minus = vtx_A - np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_a)
            projB_plus = vtx_B + np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_b)
            projB_minus = vtx_B - np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_b)

	    # Deltas
	    deltaAB_plus = distance.euclidean(projA_plus,vtx_B)
	    deltaAB_minus = distance.euclidean(projA_minus,vtx_B)
	    deltaBA_plus = distance.euclidean(projB_plus,vtx_A)
	    deltaBA_minus = distance.euclidean(projB_minus,vtx_A)

	    AB = False
	    BA = False
	    if deltaAB_plus < max_delta or deltaAB_minus <max_delta:
		AB = True

	    if deltaBA_plus < max_delta or deltaBA_minus <max_delta:
		BA = True

	    if not AB :
                print 'did not pass prjection AB'
                continue

	    if not BA :
                print 'did not pass prjection BA'
                continue



            # Take the dot between the two angles
            dotp = 0.0
            for i in range(3):
                 dotp += local_PCA_dir_a[0][i]*local_PCA_dir_b[0][i]

            # Take the Abs, and then figure out a cut. 
            dotp = math.fabs(dotp)

            print 'this is the dotp'
            print dotp
            #min_dotp = 0.9  # RG Magic number
            min_dotp = 0.96  # RG Magic number
            #min_dotp = 0.95  # RG Magic number
            if dotp < min_dotp:
                print 'Local pca do not ad up'
                continue
            # Now we have found that these two need to get merged together. 
            clust_merge_plex.append([clst_label_a,clst_label_b])

    # Put together the clusters that should be merged
    clust_merge_plex = sorted([sorted(x) for x in clust_merge_plex])
    resultlist = []
    if len(clust_merge_plex) >= 1: # If your list is empty then you dont need to do anything.
        resultlist = [clust_merge_plex[0]] #Add the first item to your resultset
        if len(clust_merge_plex) > 1: #If there is only one list in your list then you dont need to do anything.
            for l in clust_merge_plex[1:]: #Loop through lists starting at list 1
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

    ####### Reassign all labels for the results list
    for pa in resultlist:
        # First one keeps the label
        clusterlabel = pa[0]
        # These already should all have the same labels
        cluster_idx_positions =  datasetidx_holder[clusterlabel]
        # This gets the label value for the cluster
        labels_label = labels[cluster_idx_positions[0]]
	
	# Test check 
	test_labels = [labels[cluster_idx_positions[x]] for x in range(len(cluster_idx_positions))]
        print ' ' 
        print ' ' 
        print 'Test labels' 
	print test_labels


	# pa is an index in a holder

        nclusterlabels = [ pa[x] for x in xrange(1,len(pa))]
	idxlabels_to_change = []
	for i in nclusterlabels:
	    for l in datasetidx_holder[i]:
	        idxlabels_to_change.append(l)
		
		
        for lab in range(len(labels)):
            clab = labels[lab]
            # Loop over the ncluster labels to check
            for tc in idxlabels_to_change:
            #for tc in nclusterlabels:
                if labels[tc]==clab:
                #if tc==clab:
                    # Make this position label value labels_label
                    labels[lab]=labels_label
	

    new_holder = []
    for pa in resultlist:
	temp_new_holder = []
	for cpos in pa:
	    idx_positions = datasetidx_holder[cpos]
	    [temp_new_holder.append(i) for i in idx_positions]
        new_holder.append(temp_new_holder) 		

    # Remove the older clusters from the index holde
    remove_holder = [item for sublist in resultlist for item in sublist]
    new_datasetidx_holder = [ datasetidx_holder[a] for a in xrange(len(datasetidx_holder)) if a not in remove_holder]
    # Next add on the new holder
    for i in new_holder:
	new_datasetidx_holder.append(i)

    return new_datasetidx_holder,labels


