import os 
import numpy as np 


##RG This needs to be defined in a geometry type file
## for now these are  hard coded
xDetL = 256.
yDetL = 116.*2
zDetL = 1036. # This is not correct 

################################################################################
def VoxalizeData(inup, n_xdiv,n_ydiv, n_zdiv):
    # For now hardcode dectector geom 
    s= (n_xdiv,n_ydiv,n_zdiv) 
    xyz = np.zeros(s)
    #loop over the numpy input array of spacepoints log the index in the xyz 
    for s in xrange(0,len(inup)):
	xidx = int(inup[s][0]/(xDetL/n_xdiv))
	yidx = int((inup[s][1]+yDetL/2)/(yDetL/n_ydiv))
	zidx = int(inup[s][2]/(zDetL/n_zdiv))
	xyz[xidx-1][yidx-1][zidx-1]+=inup[s][3]
    return xyz

################################################################################
def VDataSet(vinup,thresh):
    xdiv = vinup.shape[0]    
    ydiv = vinup.shape[1]    
    zdiv = vinup.shape[2]    
    cpt_list = []
    for x in xrange(0,len(vinup)):
	for y in xrange(0,len(vinup[x])):
	    for z in xrange(0,len(vinup[x][y])):
		# Calulate position of center of box
		xp = xDetL/xdiv *(x+0.5)
		yp = yDetL/ydiv *(y+0.5)
		zp = zDetL/zdiv *(z+0.5)
                posq =  [xp,yp,zp,vinup[x][y][z]] 
		if vinup[x][y][z]>thresh:
	            cpt_list.append(posq)
    return cpt_list



