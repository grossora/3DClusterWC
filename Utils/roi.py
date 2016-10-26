import os
import numpy as np
import collections as col

# Carry around the over dummy geometry
xDetL = 260.
yDetL = 120.*2
zDetL = 1050. # This is not correct 

def roi_vox_buffer( ds, cls_pts , buff):
    # We have to already have the -1 removed from labels since we don't need to pass labels along
    # Find the max for xyz
    # ds here for vox comes with sub index
    xpos = []
    ypos = []
    zpos = []
    for i in cls_pts:
	#if labels[i] == -1: # Don't count the minus -1. They are not clustered
         #   continue
        xpos.append(ds[i][0])
        ypos.append(ds[i][1])
        zpos.append(ds[i][2])

    if len(cls_pts) >0:
	xlo = min(xpos)-buff
	xhi = max(xpos)+buff
	ylo = min(ypos)-buff
	yhi = max(ypos)+buff
	zlo = min(zpos)-buff
	zhi = max(zpos)+buff
    if len(cls_pts) ==0:
	xlo = 0
	xhi = xDetL
	ylo = -1.*yDetL/2 
	yhi = yDetL/2
	zlo = 0
	zhi = zDetL

    # Check all the mins and max for edge of TPC
    if xlo < 0:
	xlo = 0.0
    if ylo < -1*yDetL/2:
	ylo = -1*yDetL/2
    if zlo < 0:
	zlo = 0.0
    if xhi > xDetL:
	xhi = xDetL
    if yhi > yDetL/2:
	yhi = yDetL/2
    if zhi > zDetL:
	zhi = zDetL
    # Now we have all the hilo maxed out at the TPC edges if needed

    retv = [xlo,xhi,ylo,yhi,zlo,zhi]
    return retv

    
    

    
	
