import os 
import numpy as np

#def firstfit(inup):
def firstfit(inup,cl_idx_v):
    # inup is the whole dataset, cl_idx is the cluster index position for points
    #make the dataset for the cluster into an np array 
    # Data is in the form [[x,y,z].[],...[xn,yn,zn]]
    cl_pts = []
    for s in cl_idx_v: 
	t = [inup[s][0],inup[s][1],inup[s][2]]
	cl_pts.append(t)
    print 'size of cluster', len(cl_pts)
    cl_pts = np.asarray(cl_pts)
    uu, dd, vv = np.linalg.svd(cl_pts - cl_pts.mean(axis=0))
    # This is the first PC
    print vv[0]
     
    return vv[0]
