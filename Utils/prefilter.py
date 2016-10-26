import os 
import numpy as np 
import collections as col
from sklearn.decomposition import PCA


##RG This needs to be defined in a geometry type file
## for now these are  hard coded
xDetL = 260.
yDetL = 120.*2
zDetL = 1050. # This is not correct 

################################################################################
def Voxalizedata(inup, n_xdiv,n_ydiv, n_zdiv):
    # For now hardcode dectector geom 
    # Format goes like [charge,[index list ]]
    xyz = [[[ [0.0,[]] for x in range(n_zdiv)] for y in range(n_ydiv)] for z in range(n_xdiv)]
    #loop over the numpy input array of spacepoints log the index in the xyz 
    for s in xrange(0,len(inup)):
	xidx = int(inup[s][0]/(xDetL/n_xdiv))
	yidx = int((inup[s][1]+yDetL/2)/(yDetL/n_ydiv)) # Is this handled properly 
	zidx = int(inup[s][2]/(zDetL/n_zdiv))
	xyz[xidx][yidx][zidx][0]+=inup[s][3] # Make sure you are in the bucket
	xyz[xidx][yidx][zidx][1].append(s) # Make sure you are in the bucket
    return xyz
################################################################################
def Vdataset(vinup,thresh):
    xdiv = len(vinup)   
    ydiv = len(vinup[0])    
    zdiv = len(vinup[0][0])  
    cpt_list = []
    # Note the call goes like vinup[x][y][z]
    for x in xrange(0,len(vinup)):
	for y in xrange(0,len(vinup[x])):
	    for z in xrange(0,len(vinup[x][y])):
		# Calulate position of center of box
		xp = xDetL/xdiv *(x+0.5)
		#yp = yDetL/ydiv *(y+0.5)
		yp = yDetL/ydiv *(y+0.5) -yDetL/2 # RG Y_FIX
		zp = zDetL/zdiv *(z+0.5)
                posq =  [xp,yp,zp,vinup[x][y][z] ]# This has vinup [charge , [idx list for inup] ]
		if vinup[x][y][z][0]>thresh:
	            cpt_list.append(posq)
    return cpt_list
################################################################################
def Vdataset_InRange(vinup,thresh,xlo,xhi,ylo,yhi,zlo,zhi):
    xdiv = len(vinup)   
    ydiv = len(vinup[0])    
    zdiv = len(vinup[0][0])  
    cpt_list = []
    # Note the call goes like vinup[x][y][z]
    for x in xrange(0,len(vinup)):
        if x < xlo or x >xhi:
	    continue
	for y in xrange(0,len(vinup[x])):
            if y- yDetL/2 < ylo or y- yDetL/2 >yhi:
	        continue
	    for z in xrange(0,len(vinup[x][y])):
                if z < zlo or z >zhi:
		    continue
		# Calulate position of center of box
		xp = xDetL/xdiv *(x+0.5)
		#yp = yDetL/ydiv *(y+0.5)
		yp = yDetL/ydiv *(y+0.5) -yDetL/2 # RG Y_FIX
		zp = zDetL/zdiv *(z+0.5)
                posq =  [xp,yp,zp,vinup[x][y][z]] # This has vinup [charge , [idx list for inup] ]
		if vinup[x][y][z][0]>thresh:
	            cpt_list.append(posq)
    return cpt_list
################################################################################
def tracklike(vdata,labels):
    shi = col.Counter(labels)
    # Shi is a set, and dic lookup 
    cval = [x[0] for x in shi.items() if x[1]>50]  # Hard Coded Magic
    #clean up any -1
    if -1 in cval:
        pos = cval.index(-1)
        cval.pop(pos)

    datasetidx_v = []
    for s in cval:
        [datasetidx_v.append(i) for i, j in enumerate(labels) if j == s]

    cval_clean = []
    for a in cval:
        dd = []
        for pt in datasetidx_v:
            if labels[pt] == a:
                td = [vdata[pt][0],vdata[pt][1],vdata[pt][2]]
                dd.append(td)
        if len(dd)<3:
	    print 'OH SHIT!!! FIX THIS'
	    # Need to log some catch
            continue
        pca = PCA(n_components=3)
        pca.fit(dd)
        ppp = pca.explained_variance_ratio_
        print(pca.explained_variance_ratio_)
        print'sum of 2 and 3 ', ppp[1]+ppp[2]
        if ppp[1]+ppp[2]< 0.05:
            cval_clean.append(a)

    return cval_clean
################################################################################
def tracklike_set(vdata,labels,pcasum):
    shi = col.Counter(labels)
    # Shi is a set, and dic lookup 
    cval = [x[0] for x in shi.items() if x[1]>150]  # Hard Coded Magic
    #cval = [x[0] for x in shi.items() if x[1]>25]  # Hard Coded Magic
    #clean up any -1
    if -1 in cval:
        pos = cval.index(-1)
        cval.pop(pos)

    datasetidx_v = []
    for s in cval:
        [datasetidx_v.append(i) for i, j in enumerate(labels) if j == s]

    cval_clean = []
    for a in cval:
        dd = []
        for pt in datasetidx_v:
            if labels[pt] == a:
                td = [vdata[pt][0],vdata[pt][1],vdata[pt][2]]
                dd.append(td)
        if len(dd)<3:
	    print 'OH SHIT!!! FIX THIS'
	    # Need to log some catch
            continue
        pca = PCA(n_components=3)
        pca.fit(dd)
        ppp = pca.explained_variance_ratio_
        print(pca.explained_variance_ratio_)
        print'sum of 2 and 3 ', ppp[1]+ppp[2]
        #if ppp[1]+ppp[2]< pcasum or ppp[1]+ppp[2]> 0.25 :
        if ppp[1]+ppp[2]< pcasum:
            cval_clean.append(a)

    return cval_clean





