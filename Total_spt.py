import sys, os
import math as math
import numpy as np
import Utils.datahandle as dh
import Utils.mchandle as mh
import ROOT
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
from scipy import stats
import Clustering.protocluster as pc
import collections as col
import SParams.axisfit as axfi 
import SParams.selpizero as selpz
import SParams.merger as mr
import Clustering.protocluster as pc
import Utils.prefilter as pf


n_spts = []
q_tot = []
vn_spts = []
vq_tot = []
counter = 0 
for f in sys.argv[1:]:
    ##########
    #### Build in a check to see if we did this already
    ##########
    fi = ROOT.TFile("{}".format(f))
    if fi.IsZombie():
        print 'AHHHH Zombie...'
        continue

    rt= fi.Get("T_rec_charge")
    if rt.GetEntries()==0:
        print 'AHHHH Got nothing...'
        continue

    predataset = dh.ConvertWC_InTPC_thresh('{}'.format(f),100.)
    dataset = dh.Unique(predataset)
    # Put this length into some vector to hang on to
    n_spts.append(len(dataset))
   
    tot_q = 0.0  
    for a in dataset:
	tot_q+=a[3]
    q_tot.append(tot_q)

    # continue for now just to go fast
    counter+=1
    print "aprox counter ", counter
    continue
    ### Now voxelize with zero threshold

    ########################
    #Turn Dataset into a vox
    ########################
    pfl = pf.Voxalizedata(dataset,128*2,116*2,500*2)  # Magic
    dt = pf.Vdataset(pfl,10000.0)   # Magic
    vdataset = [ [dt[i][0],dt[i][1],dt[i][2], dt[i][3][0]] for i in range(len(dt))]
    vn_spts.append(len(vdataset))


# Here we want to look at the distrubtion of n_spts


plt.hist(np.asarray(n_spts),20)
plt.show()

plt.scatter(np.asarray(n_spts),np.asarray(q_tot))
plt.show()

# For Vox data
plt.hist(np.asarray(vn_spts),30)
plt.show()


