import os 
import numpy as np
from sklearn.decomposition import PCA


def firstfit(inup,cl_idx_v):
    # inup is the whole dataset, cl_idx is the cluster index position for points
    #make the dataset for the cluster into an np array 
    cl_pts = []
    for s in cl_idx_v: 
	t = [inup[s][0],inup[s][1],inup[s][2]]
	cl_pts.append(t)
    cl_pts = np.asarray(cl_pts)
    uu, dd, vv = np.linalg.svd(cl_pts - cl_pts.mean(axis=0))
    # This is the first PC is vv[0] 
    return vv[0]

def showerfit(inup,cl_idx_v):
    # inup is the whole dataset, cl_idx is the cluster index position for points
    #make the dataset for the cluster into an np array 
    # Data is in the form [[x,y,z].[],...[xn,yn,zn]]
    cl_pts = []
    for s in cl_idx_v: 
	t = [inup[s][0],inup[s][1],inup[s][2]]
	cl_pts.append(t)
    cl_pts = np.asarray(cl_pts)
    uu, dd, vv = np.linalg.svd(cl_pts - cl_pts.mean(axis=0))
    # This is the first PC and returned as a direction vector
    point = cl_pts.mean(axis=0)
    return point , vv[0] 

def weightshowerfit(inup,cl_idx_v):
    # inup is the whole dataset, cl_idx is the cluster index position for points
    #make the dataset for the cluster into an np array 
    # Data is in the form [[x,y,z].[],...[xn,yn,zn]]
    cl_pts = []
    # Find max charge for a pt 
    maxcharge = 0.0
    char_wt = []
    for m in cl_idx_v: 
        cw = [inup[m][3],inup[m][3],inup[m][3]]
	char_wt.append(cw)
    char_wt = np.asarray(char_wt)
    #print ' this is max charge ' , str(char_wt.max())
    #Put all the cluster points into a list
    for s in cl_idx_v: 
	t = [inup[s][0],inup[s][1],inup[s][2]]
	cl_pts.append(t)
    cl_pts = np.asarray(cl_pts)
    A = cl_pts - cl_pts.mean(axis=0)
    #here we want to weight the fit by charge
    # we will weight by charge* meancharge
    wt = char_wt*char_wt.mean()
    # multiply (point-mean )* wt
    newA = A*wt
    uu, dd, vv = np.linalg.svd(newA)
    #print vvv[0]
    # This is the first PC and returned as a direction vector
    point = cl_pts.mean(axis=0)
    return point , vv[0] 


def showerfitPCA(inup,cl_idx_v):
    # inup is the whole dataset, cl_idx is the cluster index position for points
    #make the dataset for the cluster into an np array 
    # Data is in the form [[x,y,z].[],...[xn,yn,zn]]
    cl_pts = []
    for s in cl_idx_v: 
	t = [inup[s][0],inup[s][1],inup[s][2]]
	cl_pts.append(t)
    pca = PCA(n_components=1)
    pca.fit(dd)
    strong = pca.components_
    return strong

def PCAParams(inup,cl_idx_v,n_degree):
    # inup is the whole dataset, cl_idx is the cluster index position for points
    #make the dataset for the cluster into an np array 
    # Data is in the form [[x,y,z].[],...[xn,yn,zn]]
    cl_pts = []
    for s in cl_idx_v: 
	t = [inup[s][0],inup[s][1],inup[s][2]]
	cl_pts.append(t)
    pca = PCA(n_components=n_degree)
    pca.fit(dd)
    par = pca.explained_variance_ratio_
    return par
