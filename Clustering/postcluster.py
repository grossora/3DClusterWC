import numpy as np
#from operator import itemgetter
#from scipy.spatial import distance
#from scipy.spatial import ConvexHull
#import SParams.axisfit as axfi
import math as math
import Merging.merger as mr





def cluster_volumes(dataset,tracks_epts,min_doca):
    #tracks_epts [ [label,top_pt,bottom_pt]...] 
    min_doca_sq = min_doca*min_doca

    labels = [-1 for x in range(len(dataset))]

    # Loop over dataset entirly Don't worry about what was previously clustered
    for i in range(len(dataset)):
	# Check for minimum distance between pt and volumes
	lowest_sqdist = 100000 # Hardcoded max
	v_label = -999
	for line in range(len(tracks_epts)):
	    sq_dist = mr.sqdist_ptline_to_point(tracks_epts[line][1],tracks_epts[line][2],[dataset[i][0],dataset[i][1],dataset[i][2]])
	    if sq_dist<lowest_sqdist and sq_dist<min_doca_sq:
	    #if sq_dist<lowest_sqdist:
	        lowest_sqdist=sq_dist
		v_label = line 
	    
	if v_label!=-999:
	    labels[i] = v_label
    return labels

def cluster_volumes_keep(dataset,labels,tracks_epts,min_doca):
    #tracks_epts [ [label,top_pt,bottom_pt]...] 
    min_doca_sq = min_doca*min_doca

    # Loop over dataset entirly Don't worry about what was previously clustered
    for i in range(len(dataset)):
	# Check for minimum distance between pt and volumes
	lowest_sqdist = 100000 # Hardcoded max
	v_label = -999
	for line in range(len(tracks_epts)):
	    sq_dist = mr.sqdist_ptline_to_point(tracks_epts[line][1],tracks_epts[line][2],[dataset[i][0],dataset[i][1],dataset[i][2]])
	    if sq_dist<lowest_sqdist and sq_dist<min_doca_sq:
	    #if sq_dist<lowest_sqdist:
	        lowest_sqdist=sq_dist
		v_label = tracks_epts[line][0]
	    
	if v_label!=-999:
	    labels[i] = v_label
    return labels




def cluster_near_clusters(dataset, cluster_holder, near_dist):
    min_distsqrd = pow(near_dist,2)
    merge_pairs = []

    for i in range(len(cluster_holder)):
        for j in xrange(i+1,len(cluster_holder)):
            matched_bool = False
            for ii in cluster_holder[i]:
                for jj in cluster_holder[j]:
                    # calculate dist
                    distsqrd = pow(dataset[ii][0] - dataset[jj][0],2)+pow(dataset[ii][1] - dataset[jj][1],2)+pow(dataset[ii][2] - dataset[jj][2],2)
                    if distsqrd<min_distsqrd:
                        merge_pairs.append([i,j])
                        matched_bool = True
			# Once one is close enough break out... no point in testing more
                        break
                if matched_bool:
                    break
    # Now we have the pair list
    # This takes pairs and fully connects neighbors 
    clust_merge_plex = sorted([sorted(x) for x in merge_pairs])
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
 

    mergedidx_holder= []
    merged_pass = [item for sublist in resultlist for item in sublist]
    solo_pass = [ a for a in range(len(cluster_holder)) if a not in merged_pass]

    for i in solo_pass:
        temp_holder = []
        for idx in cluster_holder[i]:
            temp_holder.append(idx)
        mergedidx_holder.append(temp_holder)

    for a in resultlist:
        temp_holder = []
        for i in a:
            for idx in cluster_holder[i]:
                temp_holder.append(idx)
        mergedidx_holder.append(temp_holder)

    # Make new labels for the new clusters
    labels = [-1 for x in range(len(dataset))]

    for l in range(len(mergedidx_holder)):
        for idx in mergedidx_holder[l]:
            labels[idx] = l


    #### Now we have labels and a new holder to work with for the clusters 
 
    return dataset , mergedidx_holder , labels






 


 




