import sys, os
import math as math
import numpy as np
import Utils.datahandle as dh
import Utils.mchandle as mh
import Utils.anahandle as ah
import Utils.eventhandle as eh
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
import Clustering.postcluster as postc
import Clustering.ts_separation as tss
import Utils.prefilter as pf
import Utils.roi as roi
from matplotlib import style
from mpl_toolkits.mplot3d import Axes3D
import collections as col
from scipy.spatial import ConvexHull
from scipy.spatial import distance
from sklearn.decomposition import PCA

style.use("ggplot")
colors = 1000*['r','g','b','c','k','y','m']





#######################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#######################################
#Global Call
debug = True
#draw_image = True
draw_image = False 
Charge_thresh = 300 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
method_name = 'test_7'
fig_dir = method_name

##TEMP BEGIN GLOBAL######
vox_event_size = []
remain_shower_spts = [] 
remain_track_spts = [] 

##TEMP END   GLOBAL######

#######################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#######################################

#######################################
#######################################
#######################################
#######################################

for f in sys.argv[1:]:
    ########################
    # Check if the File is good
    ########################
    file_info = dh.F_Info_Cosmic(f)
    #file_info = dh.F_Info(f)

    ########################
    # File info
    ########################
    if debug:
        print 'Current Event -->  Event Run SubRun : ',file_info[1]

    ########################
    # Check the log, If we have it continue
    # This needs to be implemmented when we are doing processing but not needed for when we are testing This will skip over things in the log
    ########################
    #proced = eh.event_processed(method_name,file_info[1])
    #if proced:
        #continue

    ########################
    # if the file is bad then continue and fill 
    ########################
    if not file_info[0]:
        lookup.writelines(file_info[1])
        continue


     ########################
    # IF we want to draw some plots we set up some directory stuff
    # For now we will just overwrite things so be careful !!!!!
    ########################
    curdir = os.getcwd() + '/figs/'+fig_dir+ '/'+file_info[1]   # This still is global and can be used later
    ########################
    # First check if it exists
    ########################
    if draw_image:
        if not os.path.isdir(curdir):
            print 'NO DIR.... making one for you'
            os.makedirs(curdir)


    ########################
    #Bring in  Dataset 
    ########################
    dataset = dh.ConvertWC_InTPC_thresh('{}'.format(f),3000.0)
    #dataset = dh.ConvertWC_InTPC_thresh('{}'.format(f),1000.0)
    #dataset = dh.ConvertWC_InTPC_thresh('{}'.format(f),0.0)
    print 'Size of dataset', str(len(dataset))


    ########################
    #Voxilize the event
    ########################
    ########################
    pfl = pf.Voxalizedata(dataset,64,58,250)   # Magic
    #pfl = pf.Voxalizedata(dataset,128,116,500)   # Magic
    dt = pf.Vdataset(pfl,1000)   # Magic
    ### Can't I carry along full data set spts
    vdata = [ [dt[i][0],dt[i][1],dt[i][2], dt[i][3][0], dt[i][3][1] ] for i in range(len(dt))]

    #### TEMP BEGIN #####
    vox_event_size.append(len(vdata))
    print 'Size of dataset', str(len(vdata))
    #### TEMP END   #####

    ########################
    # cluster the event into something 
    ########################
    labels = pc.crawler(vdata,5.,25) # Runs clustering and returns labels list 
    datasetidx_holder = mr.label_to_idxholder(labels,25) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  


    #######################
    #Now save the graphic and save it to a figs directory 
    #######################
    if draw_image:
        dh.Make_nipi_Fig(vdata, datasetidx_holder,labels,curdir,'All_Vox_Points',f)
        #dh.Make_Fig(vdata, datasetidx_holder,labels,curdir,'All_Vox_Points')

    #######################
    #  Stitch track like clusters
    #######################
    datasetidx_holder , labels = pc.Track_VOX_Stitcher_v2(vdata,datasetidx_holder,labels)

    #######################
    #  Identify Track-like long clusters
    #  Very straight tracks
    #######################
    showeridx_holder , trackidx_holder = tss.clusterspread(vdata,datasetidx_holder,0.989,10)
    #showeridx_holder , trackidx_holder = tss.clusterspread(vdata,datasetidx_holder,0.989,50)


    #######################
    #Now save the graphic for the showers 
    #######################
    if draw_image:
        dh.Make_nipi_Fig(vdata, showeridx_holder,labels,curdir,'All_Vox_Shower',f)
        #dh.Make_Fig(vdata, showeridx_holder,labels,curdir,'All_Vox_Shower')
    #######################
    #Now save the graphic and save it to a figs directory 
    #######################
    if draw_image:
        dh.Make_nipi_Fig(vdata, trackidx_holder,labels,curdir,'All_Vox_Track',f)
        #dh.Make_Fig(vdata, trackidx_holder,labels,curdir,'All_Vox_Track')




    ###$#$@#$@#$@#$@##@#$@#$#
    # Play ground #####
    ###$#$@#$@#$@#$@##@#$@#$#
    # Print out the indext holder
    remain_shower_spts.append(len(showeridx_holder))
    remain_track_spts.append(len(trackidx_holder))









#################################################################
#################################################################
#################################################################
#################################################################
#################################################################


###TEMP BEGIN #########

n, bins, patches  = plt.hist(remain_shower_spts,100)
plt.show()
n, bins, patches  = plt.hist(remain_track_spts,100)
plt.show()


n, bins, patches  = plt.hist(vox_event_size,100)
plt.show()
###TEMP End #########







