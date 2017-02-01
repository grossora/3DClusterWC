import numpy as np 
import collections as col
import Geo_Utils.axisfit as axfi
from sklearn.decomposition import PCA


xDetL = 256.
yDetL = 116.*2
zDetL = 1060. # This is not correct 


###########################################################################################
###########################################################################################
#############     a few functions to use for the geometry ################################
###########################################################################################
###########################################################################################

def sqdist_ptline_to_point(pt_a,pt_b,pt_t):
    n = [pt_b[0]- pt_a[0],pt_b[1]- pt_a[1],pt_b[2]- pt_a[2]]
   # pt_t = [np.random.rand(),np.random.rand(),np.random.rand()]
    pa = [pt_a[0]- pt_t[0],pt_a[1]- pt_t[1],pt_a[2]- pt_t[2]]
    #c = n  * pa.n /n.n
    pan = (pa[0]*n[0] + pa[1]*n[1]+pa[2]*n[2])/ (n[0]*n[0] + n[1]*n[1]+n[2]*n[2])
    #pan = (pt_a[0]*n[0] + pt_a[1]*n[1]+pt_a[2]*n[2])/ (n[0]*n[0] + n[1]*n[1]+n[2]*n[2])
    c = [n[0] * pan, n[1]*pan,n[2]*pan]
    d = [pa[0]-c[0], pa[1]-c[1],pa[2]-c[2]]
    return d[0]*d[0]+d[1]*d[1]+d[2]*d[2]


###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################
###########################################################################################


def make_extend_lines_list(dataset , idxlist_for_tracks,labels):
#def make_extend_lines_list(dataset , idxlist_for_tracks):
    # loop over all the 'track' points 
    # take the pca for direction 
    # extend the direction past the top and bottom in y 
    # make a circle of radius that is user defined. 
    # return the vector of points for each..there is no hull done here...  just getting the points to make hulls for 
    lp_list = [] # Append will be slow.... but this is ok for now
    for t in idxlist_for_tracks:
        #Get PCA Direction # note... this will be easier when more organized ... we have done this loop already once
        points = []
	label_val = labels[t[0]]# This gets the label value to pass along
        for p in t:
            pt = [ dataset[p][0],dataset[p][1],dataset[p][2] ]
            points.append(pt)
        # This PCA Should always converge since we have done it already 
	# There should be a Try in here
        pca = PCA(n_components=3)
        pca.fit(points)
        tdir_forward = pca.components_[0]
        tdir_backward = -1.0*pca.components_[0]
        # Get start point 
        sp = np.mean(np.asarray(points),axis=0)
        # Instead of finding the box ... just extent past the farthest possible track ( corner to corner ) 
        #  xchi = sqrt( zz+xx+yy) sqrrt( zDet**2, xdet**2, (ydet)**2) = 
        mp_length = pow( pow(zDetL,2)+pow(xDetL,2) + pow(yDetL,2),0.5)
        top_pt = sp + mp_length*tdir_forward
        bottom_pt = sp + mp_length*tdir_backward
        # Calcuate brute forced cyl polygon 
        pointslist = [label_val,top_pt, bottom_pt]
        lp_list.append(pointslist)
    return lp_list


###########################################################################################
def TrackExtend_sweep(dataset, labels, extended_lines_list, doca):
    # 
    doca_sq = doca*doca
    for i in range(len(dataset)):
	if labels[i]!= -1:
	    continue
    # Points are list
        for t in extended_lines_list:
            pt_to_line_dist_sq = sqdist_ptline_to_point(t[1],t[2],[dataset[i][0],dataset[i][1],dataset[i][2]])
	    if pt_to_line_dist_sq<doca_sq:
		# Add this shit to the cluster
	        labels[i]=t[0]
		break 
    return labels
    
		
	 
	
	
    







'''
def PCA_merge(dataset,labels,datasetidx_holder,crit_merge_angle):
    pca_holder = []
    # This is hard code need to be writted better
    min_angle_merge = crit_merge_angle
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
            anes_listngle = selpz.openingangle(shrA,shrB,vertex)
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
           # print s[z]
            for dlab in datasetidx_holder[z]:
                labels[dlab] = matchlabel

    return labels

'''
