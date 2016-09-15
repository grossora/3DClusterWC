import numpy as np
import axisfit as af
import math as math

def findvtx(shrA,shrB):
    # Get the first Shower 
    shrA_dir = shrA[1]
    shrB_dir = shrB[1]

    a = np.dot(shrA[1],shrA[1])
    b = np.dot(shrA[1],shrB[1])
    c = np.dot(shrB[1],shrB[1])
    d = np.dot(shrA[1],(shrA[0]-shrB[0]))
    e = np.dot(shrB[1],(shrA[0]-shrB[0]))
    # Check if non paralle
    den = a*c-b*b
    if den<0.0000001:
	print 'lines are too close'
    sc = (b*e-c*d)/(den)
    tc = (a*e-b*d)/(den)
    midway = (shrA[0]+sc*shrA[1] - (shrB[0]+tc*shrB[1]))/2
    vtx = shrA[0]+sc*shrA[1] - midway
    return vtx


def openingangle(shrA, shrB, vtx):
    shrA_dir = shrA[1]
    shrB_dir = shrB[1]
    pv = shrA[0]-vtx
    qv = shrB[0]-vtx
    pvu = pv/(np.sqrt(pv[0]*pv[0]+pv[1]*pv[1]+pv[2]*pv[2]))
    qvu = qv/(np.sqrt(qv[0]*qv[0]+qv[1]*qv[1]+qv[2]*qv[2]))
    dirA = np.dot(pvu,shrA_dir)
    dirB = np.dot(pvu,shrB_dir)
    #print ' This is the dir dits '
    #print dirA
    #print dirB
    if dirA<0: 
	shrA_dir = -1.*shrA_dir
    if dirB<0: 
	shrB_dir = -1.*shrB_dir
    #print ' This is the post dir dits '
    #print np.dot(pvu,shrA_dir)
    #print np.dot(pvu,shrB_dir)
    # Get the angle between 
    sma = np.sqrt(shrA_dir[0]*shrA_dir[0] + shrA_dir[1]*shrA_dir[1]+shrA_dir[2]*shrA_dir[2])
    smb = np.sqrt(shrB_dir[0]*shrB_dir[0] + shrB_dir[1]*shrB_dir[1]+shrB_dir[2]*shrB_dir[2])
    cos = np.dot(shrA_dir,shrB_dir) /( sma*smb  )
    #print 'this is cos ', str(cos)
    angle = math.acos(cos)
    print 'this is angle ', str(angle)
    return angle
    
def totcharge(inup, indexset):
    totq =0.0
    for s in indexset:
	totq+= inup[s][3]
    # Shitty fit for energy 
    fenergy = 2.5847*pow(10,-8) *totq +0.017209
    #fenergy = 2.473*pow(10,-8) *totq +0.030966546
    return fenergy
    

def mass(ea,eb,angle):
    # make sure things are ok 
    if ea<=0 or eb <=0 :
        print ' energy is zero!!!'
    mass = np.sqrt(2.* ea*eb*(1-math.cos(angle)))
    return mass
    
    
    
    

    
