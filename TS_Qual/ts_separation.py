import numpy as np
from sklearn.decomposition import PCA
from scipy.spatial import ConvexHull


def clusterspread(dataset,datasetidx_holder, vari, clustersize):
    #print 'start of clusterspread'
    track_holder = []
    shower_holder = []
    for a in datasetidx_holder:
        points = []
        for p in a:
            pt = [ dataset[p][0],dataset[p][1],dataset[p][2] ]
            points.append(pt)

        if len(points)<clustersize:
            # Push this to the showers holder
            shower_holder.append(a)
            continue

	par = -999
        try:
            pca = PCA(n_components=3)
            pca.fit(points)
            par = pca.explained_variance_
            #par = pca.explained_variance_ratio_
	    #print' this is the vairance '
            #print pca.explained_variance_
	    #print' this is the ratio'
            #print pca.explained_variance_ratio_
	except:
	    print ' could not make a PCA'
            shower_holder.append(a)
	    continue

        if par[0] > vari:
        #if par[0] > first:
            #print len(points)
            #print par[0]
            track_holder.append(a)
            continue
        else:
            shower_holder.append(a)

    return shower_holder, track_holder


def clusterlength_sep(dataset,datasetidx_holder, min_length):

    track_holder = []
    shower_holder = []

    #for a in range(len(datasetidx_holder)):
    for a in datasetidx_holder:
        points_v = []
	for i in a:
	    pt = [ dataset[i][0],dataset[i][1],dataset[i][2]]
	    points_v.append(pt)

        try:
            hull = ConvexHull(points_v)
        except:
            print ' AHHHHHHHHHH couldnt make hull'
            print ' length of the points cluster' , str(len(points_v))
	    # Put the cluster in the shower
	    shower_holder.append(a)
            continue


        # Check if it is past the min_length
        min_bd = hull.min_bound
        max_bd = hull.max_bound
        # distance using NP 
        clust_length = np.linalg.norm(min_bd-max_bd)
	if clust_length<= min_length:
	    shower_holder.append(a)
	else :
	    print ' ###############################'
	    print ' Look we made a track object from length'
	    print clust_length
	    print ' ###############################'
	    track_holder.append(a)
	
    return shower_holder, track_holder


######################################################################

def stray_charge_removal(dataset,datasetidx_holder,labels, max_csize, m_dist):
    CHQ_vec = []
    stray_holder = []
    remain_holder = []
    # ^^^^^^ Will be of the form [    [datasetidx_holder INDEX, the vertices of the hull, total_charge] ]
    notStrays = []  # This is the idx holderr for the datasetidx_holder....
    min_dist_not_be_a_LONER_sq = m_dist*m_dist
 
    for a in range(len(datasetidx_holder)):
        points_v = []
        for i in datasetidx_holder[a]:
            if labels[i]==-1:
                break
            pt = [ dataset[i][0],dataset[i][1],dataset[i][2]]
            points_v.append(pt)
        #Try to make a hull 
        try:
            hull = ConvexHull(points_v)
        except:
	    # Use all the points in the cluster as the vertex points
            chq = [a,datasetidx_holder[a]]
	    # RG 
	    print ' in the exception '  
	    print chq
            #chq = [a,datasetidx_holder[a],tot_q]
            CHQ_vec.append(chq)
            continue
        # Now we have the hull
        ds_hull_idx = [datasetidx_holder[a][i] for i in list(hull.vertices)] # Remeber use the true idx
        chq = [a,ds_hull_idx]
	# RG 
	print ' out the exception '  
	print chq
        #chq = [a,ds_hull_idx,tot_q]
        CHQ_vec.append(chq)
    Strays = []  # This is the idx holderr for the datasetidx_holder....
    for a in range(len(CHQ_vec)):
        first_CHQ = CHQ_vec[a]
	if len(datasetidx_holder[first_CHQ[0]])>max_csize:
            notStrays.append(first_CHQ[0]) # This is the idx holderr for the datasetidx_holder.... 
	    continue
	passed_close_bool = False
        for b in range(len(CHQ_vec)):
        #for b in range(a+1,len(CHQ_vec)):
	    if passed_close_bool:
		break
	    if b==a:
		continue

            second_CHQ = CHQ_vec[b]
            min_dist_not_be_a_LONER_sq = m_dist*m_dist

	    # all I care about is if it passes to a so use a break... this will be a double count
            cur_pair = []
            for i in range(len(first_CHQ[1])):
		if passed_close_bool:
		    break
                for j in range(len(second_CHQ[1])):
                    test_dist_sq = ((dataset[first_CHQ[1][i]][0] - dataset[second_CHQ[1][j]][0]) *(dataset[first_CHQ[1][i]][0] - dataset[second_CHQ[1][j]][0])) +((dataset[first_CHQ[1][i]][1] - dataset[second_CHQ[1][j]][1]) *(dataset[first_CHQ[1][i]][1] - dataset[second_CHQ[1][j]][1])) + ( (dataset[first_CHQ[1][i]][2] - dataset[second_CHQ[1][j]][2]) *(dataset[first_CHQ[1][i]][2] - dataset[second_CHQ[1][j]][2]))
                    if test_dist_sq<min_dist_not_be_a_LONER_sq:
			passed_close_bool = True
			print 'we have a close cluster'
			break
			
            if passed_close_bool:
                #we didn't get anything to match
		notStrays.append(first_CHQ[0]) # This is the idx holderr for the datasetidx_holder.... 
                continue
    print ' look at the straysStrays'
    print notStrays

    # Take the idxs from the starys and label these are -1 objects
    for a in range(len(datasetidx_holder)):
	if a in notStrays:
	    remain_holder.append(datasetidx_holder[a])
	else:
	    stray_holder.append(datasetidx_holder[a])
	    for lab in datasetidx_holder[a]:
		labels[lab] = -1

    return stray_holder, remain_holder, labels
    




######################################################################



