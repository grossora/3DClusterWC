import numpy as np
import SParams.axisfit as axfi
from scipy.spatial import distance
from scipy.spatial import ConvexHull


def Track_Stitcher_epts(dataset,datasetidx_holder,labels,gap_dist,k_radius,pdelta):
    # Clean Stitch 
    #gap_dist = minimal closest distance betweel hulls
    #k_radius = radius for points around the hulls minimal dist point 
    #pdelta = minimal distance allowed from the projection 
    CHQ_vec = []
    # ^^^^^^ Will be of the form [    [datasetidx_holder INDEX, the vertices of the hull, total_charge] ]
    for a in range(len(datasetidx_holder)):
        points_v = []
        tot_q = 0.0
        for i in datasetidx_holder[a]:
            if labels[i]==-1:
                break
            pt = [ dataset[i][0],dataset[i][1],dataset[i][2]]
            points_v.append(pt)
            tot_q+= dataset[i][3]
        #Try to make a hull 
        try:
            hull = ConvexHull(points_v)
        except:
            continue
        # Now we have the hull
        ds_hull_idx = [datasetidx_holder[a][i] for i in list(hull.vertices)] # Remeber use the true idx
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
            #Find the two vertex points that are closest to each other from the different clusters
            for i in range(len(first_CHQ[1])):
                for j in range(len(second_CHQ[1])):
                    ## RG This is slow... USE Dist SQ to speed up...  do it yourself
                    test_dist = distance.euclidean([dataset[first_CHQ[1][i]][0],dataset[first_CHQ[1][i]][1],dataset[first_CHQ[1][i]][2]],[dataset[second_CHQ[1][j]][0],dataset[second_CHQ[1][j]][1],dataset[second_CHQ[1][j]][2]])
                    if  test_dist<gap_dist and test_dist<cur_smallest_dist:
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

            # Now do the comparison
            #Find First PCA 
            local_pts_idx_a = []
            for i in datasetidx_holder[clst_label_a]:
            #for i in clst_indexs_a:
                k_dist = distance.euclidean([dataset[i][0],dataset[i][1],dataset[i][2]],[dataset[vp_idx_a][0],dataset[vp_idx_a][1],dataset[vp_idx_a][2]])
                if k_dist<k_radius:
                    local_pts_idx_a.append(i)
            # Find the PCA
            local_PCA_a = [-999]
            local_PCA_dir_a = [-999]
            try:
                local_PCA_a = axfi.PCAParams(dataset,local_pts_idx_a,3)
                local_PCA_dir_a = axfi.PCAParams_dir(dataset,local_pts_idx_a,3)
            except:
                local_PCA_a = [-999]
                continue

            #Find second PCA 
            local_pts_idx_b = []
            #for i in clst_indexs_b:
            for i in datasetidx_holder[clst_label_b]:
                k_dist = distance.euclidean([dataset[i][0],dataset[i][1],dataset[i][2]],[dataset[vp_idx_b][0],dataset[vp_idx_b][1],dataset[vp_idx_b][2]])
                if k_dist<k_radius:
                    local_pts_idx_b.append(i)
            # Find the PCA
            #local_PCA_a = [-999]  ##### This is a typo
            local_PCA_b = [-999]
            local_PCA_dir_b = [-999]
            try:
                local_PCA_b = axfi.PCAParams(dataset,local_pts_idx_b,3)
                local_PCA_dir_b = axfi.PCAParams_dir(dataset,local_pts_idx_b,3)
            except:
                local_PCA_b = [-999]
                continue
            # Get the points 
            vtx_A =  np.asarray([dataset[vp_idx_a][0],dataset[vp_idx_a][1],dataset[vp_idx_a][2]])
            vtx_B =  np.asarray([dataset[vp_idx_b][0],dataset[vp_idx_b][1],dataset[vp_idx_b][2]])
            Length_between_vtx = distance.euclidean(vtx_A,vtx_B)
            projA_plus = vtx_A + np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_dir_a[0])
            projA_minus = vtx_A - np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_dir_a[0])
            projB_plus = vtx_B + np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_dir_b[0])
            projB_minus = vtx_B - np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_dir_b[0])
            # Deltas
            deltaAB_plus = distance.euclidean(projA_plus,vtx_B)
            deltaAB_minus = distance.euclidean(projA_minus,vtx_B)
            deltaBA_plus = distance.euclidean(projB_plus,vtx_A)
            deltaBA_minus = distance.euclidean(projB_minus,vtx_A)

	    # Do the comparison
            AB = False
            BA = False
            if deltaAB_plus < pdelta or deltaAB_minus <pdelta:
                AB = True

            if deltaBA_plus < pdelta or deltaBA_minus <pdelta:
                BA = True

            if not AB :
                continue

            if not BA :
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

        # loop over all of the PA;
        for p in pa:
            # p is the clusterlabel
            cidx = datasetidx_holder[p]
            for i in cidx:
                labels[i] = labels_label
    # Return here? 
    # Currently this is only working of the labels end of things... .the new dataset is not addresed yet
    # I just  need the labels at the moment .... and this is a fucking mess.... 
    return datasetidx_holder,labels

#############################################################
### DEPRICATED STUFF
#############################################################

#def Track_Stitcher_epts(dataset,datasetidx_holder,labels,gap_dist,k_radius,pdelta):
'''
    # Clean Stitch 
    #gap_dist = minimal closest distance betweel hulls
    #k_radius = radius for points around the hulls minimal dist point 
    #pdelta = minimal distance allowed from the projection 
    CHQ_vec = []
    # ^^^^^^ Will be of the form [    [datasetidx_holder INDEX, the vertices of the hull, total_charge] ]
    print 'This is the length of the holder'
    print len(datasetidx_holder)
    for a in range(len(datasetidx_holder)):
        points_v = []
        tot_q = 0.0

        for i in datasetidx_holder[a]:
            if labels[i]==-1:
                print 'LOOOOOOOOOOOOOOOOOOOK -1  '
                break
            pt = [ dataset[i][0],dataset[i][1],dataset[i][2]]
            points_v.append(pt)
            tot_q+= dataset[i][3]

        #Try to make a hull 
        try:
            hull = ConvexHull(points_v)
        except:
            continue

        # Now we have the hull
        ds_hull_idx = [datasetidx_holder[a][i] for i in list(hull.vertices)] # Remeber use the true idx
        chq = [a,ds_hull_idx,tot_q]
        CHQ_vec.append(chq)

#       print ' the four ;;;;;;;;;;;; '
#       print min(datasetidx_holder[a])
#       print max(datasetidx_holder[a])
#       print min(ds_hull_idx)
#       print max(ds_hull_idx)

    clust_merge_plex = [] # Pairs of local clusters that need to be merged There are from the id from the datasetidx_holder labels
    for a in range(len(CHQ_vec)):
        # Get the first 
        first_CHQ = CHQ_vec[a]
        for b in xrange(a+1,len(CHQ_vec)):
            second_CHQ = CHQ_vec[b]
            # Find the closest points between the two hulls
            cur_smallest_dist = 1000000. # This stays hardcoded as a maximum
            cur_pair = []
            #Find the two vertex points that are closest to each other from the different clusters
            for i in range(len(first_CHQ[1])):
                for j in range(len(second_CHQ[1])):
                    ## RG This is slow... USE Dist SQ to speed up...  do it yourself
                    test_dist = distance.euclidean([dataset[first_CHQ[1][i]][0],dataset[first_CHQ[1][i]][1],dataset[first_CHQ[1][i]][2]],[dataset[second_CHQ[1][j]][0],dataset[second_CHQ[1][j]][1],dataset[second_CHQ[1][j]][2]])
                    if  test_dist<gap_dist and test_dist<cur_smallest_dist:
                        #print 'test distance in min!!!!!!!!!!!', str(test_dist)
                        cur_smallest_dist = test_dist
                        cur_pair = [i,j] # This is the idx value that should corespond to dataset for this pair of hull vertices
            if len(cur_pair)==0:
                #we didn't get anything to match
                continue
            print cur_pair
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


            print 'A few things  with current stuff A', str(clst_label_a)
            print 'length of clusters' , str(len(clst_indexs_a))
            print 'length of full clusters' , str(len(datasetidx_holder[clst_label_a]))
            print vp_idx_a
            print 'A few things  with current stuff B', str(clst_label_b)
            print 'length of clusters' , str(len(clst_indexs_b))
            print 'length of full clusters' , str(len(datasetidx_holder[clst_label_b]))
            print vp_idx_b
            print ' what is the distance between the two points... see if its small '
            print distance.euclidean([dataset[vp_idx_a][0],dataset[vp_idx_a][1],dataset[vp_idx_a][2]],[dataset[vp_idx_b][0],dataset[vp_idx_b][1],dataset[vp_idx_b][2]])

            # Now do the comparison

            #Find First PCA 
            local_pts_idx_a = []
            for i in datasetidx_holder[clst_label_a]:
            #for i in clst_indexs_a:
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
            #for i in clst_indexs_b:
            for i in datasetidx_holder[clst_label_b]:
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
            # Get the points 
            vtx_A =  np.asarray([dataset[vp_idx_a][0],dataset[vp_idx_a][1],dataset[vp_idx_a][2]])
            vtx_B =  np.asarray([dataset[vp_idx_b][0],dataset[vp_idx_b][1],dataset[vp_idx_b][2]])
            Length_between_vtx = distance.euclidean(vtx_A,vtx_B)
            print ' ========OUT PUT ======='
            print vtx_A
            print vtx_B
            print Length_between_vtx
            projA_plus = vtx_A + np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_dir_a[0])
            projA_minus = vtx_A - np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_dir_a[0])
            projB_plus = vtx_B + np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_dir_b[0])
            projB_minus = vtx_B - np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_dir_b[0])
            #projA_plus = vtx_A + np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_a)
            #projA_minus = vtx_A - np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_a)
            #projB_plus = vtx_B + np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_b)
            #projB_minus = vtx_B - np.asarray([1,1,1])*Length_between_vtx * np.asarray(local_PCA_b)
            print ' here are the prohA'
            print projA_plus
            print ' here are the prohA'
            print projA_minus
            print ' here are the prohB'
            print projB_plus
            print ' here are the prohB'
            print projB_minus

            # Deltas
            deltaAB_plus = distance.euclidean(projA_plus,vtx_B)
            deltaAB_minus = distance.euclidean(projA_minus,vtx_B)
            deltaBA_plus = distance.euclidean(projB_plus,vtx_A)
            deltaBA_minus = distance.euclidean(projB_minus,vtx_A)
            print ' here are the delats AB'
            print deltaAB_plus
            print ' here are the delats AB - '
            print deltaAB_minus
            print ' here are the delats BA'
            print deltaBA_plus
            print ' here are the delats BA - '
            print deltaBA_minus

            print ' ======== E N D ======='

            AB = False
            BA = False
            if deltaAB_plus < pdelta or deltaAB_minus <pdelta:
                AB = True

            if deltaBA_plus < pdelta or deltaBA_minus <pdelta:
                BA = True

            if not AB :
                print 'did not pass prjection AB'
                continue

            if not BA :
                print 'did not pass prjection BA'
                continue

            # Now we have found that these two need to get merged together. 
            clust_merge_plex.append([clst_label_a,clst_label_b])
            print ' we made it!!!!!'

    print ' presort '
    print clust_merge_plex
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
    print ' resultlist '
    print resultlist

    ####### Reassign all labels for the results list
    print 'working in the reassign part of the code in the result list loop'
    for pa in resultlist:
        print ' this is pa '
        print pa
        # First one keeps the label
        clusterlabel = pa[0]
        print ' this is cluster label '
        print clusterlabel
        # These already should all have the same labels
        cluster_idx_positions =  datasetidx_holder[clusterlabel]
        print ' this is cluster idx position'
        print cluster_idx_positions
        # This gets the label value for the cluster
        labels_label = labels[cluster_idx_positions[0]]
        print 'this is labels_label.... it should be a unique label for all of the preclustered points'
        print labels_label

        # Test check 
        print ' length of the labels list is this '
        print len(labels)

        print' we need to midify the labels list '
        # loop over all of the PA;
        for p in pa:
            # p is the clusterlabel
            cidx = datasetidx_holder[p]
            print ' this is the first labels and convert '
            for i in cidx:
                print labels[i]
                labels[i] = labels_label
                print labels[i]

        #test_labels = [labels[cluster_idx_positions[x]] for x in range(len(cluster_idx_positions))]
        print ' '
    # Return here? 
    # Currently this is only working of the labels end of things... .the new dataset is not addresed yet
    # I just  need the labels at the moment .... and this is a fucking mess.... 
    return datasetidx_holder,labels

'''
