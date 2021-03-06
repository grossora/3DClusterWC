import numpy as np
#from sklearn.decomposition import PCA
import Geo_Utils.axisfit as axfi
from scipy.spatial import ConvexHull

def clusterspread_first(dataset,datasetidx_holder, vari, clustersize):
    track_holder = []
    shower_holder = []

    for a in datasetidx_holder:
        points = []
        for p in a:
            pt = [ dataset[p][0],dataset[p][1],dataset[p][2] , dataset[p][3]]
            points.append(pt)

        if len(points)<clustersize:
            # Push this to the showers holder
            shower_holder.append(a)
            continue

	par = -999
        try:
	    par = axfi.WPCAParams(points,[x for x in range(len(points))],3)
	except:
	    print ' could not make a PCA'
            shower_holder.append(a)
	    continue

        if par[0] > vari:
            track_holder.append(a)
            continue
        else:
            shower_holder.append(a)

    return shower_holder, track_holder

def clusterspreadR_first(dataset,datasetidx_holder, vari, clustersize):
    track_holder = []
    shower_holder = []

    for a in datasetidx_holder:
        points = []
        for p in a:
            pt = [ dataset[p][0],dataset[p][1],dataset[p][2] , dataset[p][3]]
            points.append(pt)

        if len(points)<clustersize:
            # Push this to the showers holder
            shower_holder.append(a)
            continue

	par = -999
        try:
	    par = axfi.WPCAParamsR(points,[x for x in range(len(points))],3)
	except:
	    print ' could not make a PCA'
            shower_holder.append(a)
	    continue

        if par[0] > vari:
            track_holder.append(a)
            continue
        else:
            shower_holder.append(a)

    return shower_holder, track_holder

#============================================================================
def clusterspreadR(dataset,datasetidx_holder, vari_lo=0, vari_hi=1, moment = 0 ):
    in_holder = []
    out_holder = []

    for a in datasetidx_holder:
        points = []
        for p in a:
            pt = [ dataset[p][0],dataset[p][1],dataset[p][2] , dataset[p][3]]
            points.append(pt)

	par = -999
        try:
	    par = axfi.WPCAParamsR(points,[x for x in range(len(points))],3)
	except:
	    print ' could not make a PCA'
            out_holder.append(a)
	    continue

        if par[moment] > vari_lo and par[moment]<vari_hi:
            in_holder.append(a)
            continue
        else:
            out_holder.append(a)

    return out_holder, in_holder

#============================================================================
def cluster_lhull_cut(dataset,datasetidx_holder):

    track_holder = []
    shower_holder = []

    # Function we will  use for the cut is something like pow(SA,3/2)
    for a in datasetidx_holder:
        points_v = []
	for i in a:
	    pt = [ dataset[i][0],dataset[i][1],dataset[i][2]]
	    points_v.append(pt)
        try:
            hull = ConvexHull(points_v)
        except:
            print ' AHHHHHHHHHH couldnt make hull'
	    # Put the cluster in the shower
	    shower_holder.append(a)
            continue

        # Check if it is past the min_length
        min_bd = hull.min_bound
        max_bd = hull.max_bound
        # distance using NP 
	x_min = min_bd[0]
	y_min = min_bd[1]
	z_min = min_bd[2]
	x_max = max_bd[0]
	y_max = max_bd[1]
	z_max = max_bd[2]
	
	clust_length = pow((x_max-x_min)*(x_max-x_min) + (y_max-y_min)*(y_max-y_min) + (z_max-z_min)*(z_max-z_min),0.5)

	# This is the function we will cut on .... it's derived from single pi0 and SA
	Test_cut_param = pow(clust_length,1.5)-15

	if hull.area>= Test_cut_param:
	    shower_holder.append(a)
	else :
	    print ' ###############################'
	    print ' Look we made a track object from length'
	    print ' ###############################'
	    track_holder.append(a)
	
    return shower_holder, track_holder

#============================================================================
def cluster_lhull_length_cut(dataset,datasetidx_holder, min_length):

    track_holder = []
    shower_holder = []

    # Function we will  use for the cut is something like pow(SA,3/2)
    for a in datasetidx_holder:
        points_v = []
	for i in a:
	    pt = [ dataset[i][0],dataset[i][1],dataset[i][2]]
	    points_v.append(pt)
        try:
            hull = ConvexHull(points_v)
        except:
            print ' AHHHHHHHHHH couldnt make hull'
	    # Put the cluster in the shower
	    shower_holder.append(a)
            continue

        # Check if it is past the min_length
        min_bd = hull.min_bound
        max_bd = hull.max_bound
        # distance using NP 
	x_min = min_bd[0]
	y_min = min_bd[1]
	z_min = min_bd[2]
	x_max = max_bd[0]
	y_max = max_bd[1]
	z_max = max_bd[2]
	
	clust_length = pow((x_max-x_min)*(x_max-x_min) + (y_max-y_min)*(y_max-y_min) + (z_max-z_min)*(z_max-z_min),0.5)

	if clust_length>= min_length:
	    track_holder.append(a)
	# This is the function we will cut on .... it's derived from single pi0 and SA
	Test_cut_param = pow(clust_length,1.5)-15

	if hull.area>= Test_cut_param:
	    shower_holder.append(a)
	else :
	    print ' ###############################'
	    print ' Look we made a track object from length'
	    print ' ###############################'
	    track_holder.append(a)
	
    return shower_holder, track_holder



#============================================================================

def clusterlength_sep(dataset,datasetidx_holder, min_length):

    track_holder = []
    shower_holder = []
    min_length_sq = min_length*min_length

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
	    # Put the cluster in the shower
	    shower_holder.append(a)
            continue

        # Check if it is past the min_length
        min_bd = hull.min_bound
        max_bd = hull.max_bound
        # distance using NP 
	x_min = min_bd[0]
	y_min = min_bd[1]
	z_min = min_bd[2]
	x_max = max_bd[0]
	y_max = max_bd[1]
	z_max = max_bd[2]
	
	clust_length_sq = (x_max-x_min)*(x_max-x_min) + (y_max-y_min)*(y_max-y_min) + (z_max-z_min)*(z_max-z_min)
	if clust_length_sq<= min_length_sq:
	    shower_holder.append(a)
	else :
	    print ' ###############################'
	    print ' Look we made a track object from length'
	    print ' ###############################'
	    track_holder.append(a)
	
    return shower_holder, track_holder


######################################################################

### Needs to be updated
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
