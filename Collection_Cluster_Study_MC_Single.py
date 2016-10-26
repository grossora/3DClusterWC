import sys, os
import ROOT
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
from scipy import stats
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import Utils.datahandle as dh
import Utils.mchandle as mh
import Clustering.protocluster as pc
import collections as col 
import SParams.axisfit as axfi
import SParams.merger as mr 
import math as math
import time
import Utils.prefilter as pf


#Cheating on a few graphical things
from pylab import MaxNLocator


###############
####Define some lists and things 
###############

dist_cl_min =  9
dist_cl_max = 10 
dist_cl_step =  1
#####
clss_min =  150
clss_max =  151
clss_step =  1
#####
merge_angle_min =  .3
merge_angle_max =  .31
merge_angle_step =  .1
#####

###############
###############
###############
nclist = []


maxdatasetsize = 15000


###############
###############

#lookup = open('CL_Param_Opt_Photon.txt','a+')
lookup = open('Out_text/CL_Param_Opt_Photon_Single_vox_nomerge.txt','a+')
#lookup = open('CL_Param_Opt_Photon_Single.txt','a+')

#Loop through all the files

bypass = True 

for f in sys.argv[1:]:

    #Check if file is good
    if not dh.FileIsGood(f):
	continue
    dirnum = f.rsplit('/',1)[0].rsplit('/',1)[1]
    fnum = f.rsplit('/',1)[1].rsplit('.')[0].rsplit('_',1)[1]
    dist_cl = -1
    #Shit fast hack
    if bypass:
        if int(dirnum) < 7:
	    continue
        if int(fnum) < 30:
	    continue
    bypass = False

    '''
    ########## 
    # This is going to be slow if done every time
    ########## 
    lookup = open('CL_Param_Opt_Photon.txt','a+')
    print 'break A'
    if bypass:
        print 'break B'
        dirfiledone = True
        for dl in xrange(dist_cl_min,dist_cl_max,dist_cl_step):
            alreadydone = False
            for line in  lookup:
                sline = line.split(' ',3)
	        print ' dir num comp' , sline[0],'' , dirnum 
	        print sline[0] 
	        print dirnum 
                #if int(sline[0])==int(dirnum)and int(sline[1])==int(fnum) and int(sline[2])==int(dl):
                if int(sline[0])==int(dirnum):
                #if int(sline[0])==dirnum and int(sline[1])==fnum and sline[2]==dl:
                    print 'break C'
                    print 'break D'
                    print ' alrady have these '
                    alreadydone = True
                    break
            if alreadydone:
                continue
	    dist_cl_min = dl
	    dirfiledone= False
	    break 
    # if we are done.... then go to next file 
    if dirfiledone:
	continue
    ########## 
    ########## 
    print ' we are here .... ' 
    bypass = False 

    print dist_cl_min

    '''
    # Now that  we have the datafile... lets run mcinfo

    TruthString = mh.gamma_mc_info('{}'.format(f)) # Needs to be wrote
    TruthStringDep = mh.gamma_mc_dep('{}'.format(f)) # Needs to be wrote
    predataset = dh.ConvertWC_InTPC('{}'.format(f))
    dataset = dh.Unique(predataset)

    #################3
    #Turn Dataset into a vox
    pfl = pf.Voxalizedata(dataset,128,116,500)
    dt = pf.Vdataset(pfl,20000)
    dataset = [ [dt[i][0],dt[i][1],dt[i][2], dt[i][3][0]] for i in range(len(dt))]
    print 'size of Vox Data ' , len(dataset)
    print dataset
    #################3


    if len(dataset)>maxdatasetsize:
	continue


    ############# 
    ### Fill out things for MC and WC reco 
    ############# 
    fi = ROOT.TFile("{}".format(f))
    reco = fi.Get("T_rec_charge")
    tot_r_charge = 0.
    for ch in reco:
	tot_r_charge+=ch.q


    

    ##### _o the clustering tests
    for dist_cl in xrange(dist_cl_min,dist_cl_max,dist_cl_step):
	for clss in xrange(clss_min,clss_max,clss_step):
	    for ma in np.arange(merge_angle_min,merge_angle_max,merge_angle_step):
#---------------------------------------------------------------------------------------------
		print 'dir: ' + str(dirnum) + ' fNum ' + str(fnum) + ' dist: ' + str(dist_cl)
		labels = pc.crawler(dataset,1.* dist_cl,10) # a list of index values
		###### Here we may want to run a loop to vary the min cluster thres 
		datasetidx_holder = mr.label_to_idxholder(labels,clss)

		# Here we do some merging... 
		# Make merger a fucntion of angle then loop over differnt ones
		#labels = mr.PCA_merge(dataset,labels,datasetidx_holder,ma)
		#labels = mr.PCA_merge(dataset,labels,datasetidx_holder)
		#datasetidx_holder = mr.label_to_idxholder(labels,clss)

	#------ -work around this
		##### Grab the largest cluster and inspect
		countedlist = col.Counter(labels)
		#Here is the largest cluster label.... not index
		largest_cluster_label =  countedlist.most_common(1)[0][0]
#------ -work around this

		# This makes it the first in the list
		datasetidx_holder = mr.largestlabel_to_idxholder(labels)
		#datasetidx_holder = mr.label_to_idxholder([largest_cluster_label],200)
		# Run the shower axis fit..... ?
		print 'DS size' 
		print len(datasetidx_holder[0])
		wef = axfi.weightshowerfit(dataset,datasetidx_holder[0])
		# We can also quasi-get the start point
	
#---------------------------------------------------------------------------------------------

	#############################
	#######FILL OUT INFO#########
	#############################

		selectedcharge = 0.0
		for pt in datasetidx_holder[0]:
		#for pt in dh.DuplicateIDX(labels,largest_cluster_label):
		    FitData  =dataset[pt][3]
		    selectedcharge +=FitData
		#Fraction of selcharge to tot charge
		FracSel = selectedcharge/tot_r_charge
		FracRemain = 1-(selectedcharge/tot_r_charge)

		###
		#Calcualte angle diff from true dot with reco 
		mcdir = [TruthString.split(' ')[3],TruthString.split(' ')[4],TruthString.split(' ')[5]]
		mrdot = (float(mcdir[0])*wef[1][0]+ float(mcdir[1])*wef[1][1]+float(mcdir[2])*wef[1][2])
		
		Angle_Dif = math.acos(mrdot)
		
		if Angle_Dif > np.pi/2:
		    Angle_Dif = np.pi -Angle_Dif
		

		#Number of clusters
		nclusters = [ x for x in countedlist.items() if x[1]>clss]
		### RECO Line 
		RecoString = str(selectedcharge)+' '+ str(FracSel) + ' ' + str(FracRemain) +' '+ str(Angle_Dif)+' '+str(len(nclusters)) +'\n'

                lookup = open('Out_text/CL_Param_Opt_Photon_Single_vox_nomerge.txt','a+')
		#Fill out the string and add it to the file
		line = str(dirnum)+' '+ str(fnum)+' '+ str(dist_cl)+' '+str(clss) +' '+str(ma)+ ' '+ TruthString +' '+TruthStringDep+ ' ' + RecoString
		#line = str(dirnum)+' '+ str(fnum)+' '+ str(dist_cl) +' '+ TruthString + ' ' + RecoString
		lookup.writelines(line)
		lookup.close()

#---------------------------------------------------------------------------------------------








# Now that we have this file... 
# We wilil need to check





