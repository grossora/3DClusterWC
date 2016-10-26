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
import Utils.roi as roi
from matplotlib import style
from mpl_toolkits.mplot3d import Axes3D
import collections as col
style.use("ggplot")
colors = 1000*['r','g','b','c','k','y','m']


#### THese cuts don't matter here
lookup = open('Out_text/test_data_ROI.txt','a+')

for f in sys.argv[1:]:
    ##########
    #### Build in a check to see if we did this already
    ##########
    event = f.rsplit('/',1)[1].split('.')[0].split('_')[1]
    run = f.rsplit('/',1)[1].split('.')[0].split('_')[2]
    subrun = f.rsplit('/',1)[1].split('.')[0].split('_')[3]
    ers = str(event)+'_'+str(run)+'_'+str(subrun)
    # The file
    fi = ROOT.TFile("{}".format(f))
    #### Check if file is zomobie
    if fi.IsZombie():
	print 'We have a Zombie!'
	fline =[ -1 for x in range(18)] ### Fix to what ever the number is
	rfline = event+' '+run+' '+subrun+' '+ str(fline).split('[')[1].rsplit(']')[0].replace(',','')+ '\n'
	continue
	
    rt= fi.Get("T_rec_charge")
    if rt.GetEntries()==0:
        print 'AHHHH Got nothing...'
	fline =[ -2 for x in range(18)] ### Fix to what ever the number is
	rfline = event+' '+run+' '+subrun+' '+ str(fline).split('[')[1].rsplit(']')[0].replace(',','')+ '\n'
	continue

    # Print out the current evet
    print 'Current Event -->  Event: ', str(event) +'  Run ' + str(run)+'  subRun ' + str(subrun)

    ########################
    #Bring in  Dataset 
    ########################
    predataset = dh.ConvertWC_InTPC_thresh('{}'.format(f),100)
    dataset = dh.Unique(predataset) # This might not be needed
    print 'Size of dataset', str(len(dataset))

    ########################
    #Turn Dataset into a vox
    ########################
    pfl = pf.Voxalizedata(dataset,128,116,500)   # Magic
    dt = pf.Vdataset(pfl,1000)   # Magic
    ### Can't I carry along full data set spts
    vdata = [ [dt[i][0],dt[i][1],dt[i][2], dt[i][3][0], dt[i][3][1] ] for i in range(len(dt))]
    #print 'size of Vox Data ' , len(dataset)

    ########################
    # Run the walking code for ROI
    ########################
    labels = pc.crawlernn(vdata,11.,50)



    ########################
    #Now save the graphic and save it to a figs directory 
    ########################
    cwd = os.getcwd()
    fig_dir = 'thresh_11cm_dist_0.35_merge'
    curdir = cwd + '/figs/'+fig_dir+ '/'+ers
    # First check if it exists
    if not os.path.isdir(curdir):
	print 'NO DIR.... making one for you'
        os.makedirs(curdir)


    ########################
    # Plot all the vox data 
    ########################
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(vdata)): #This loop over just the return/passed clusters
       if labels[i] == -1:
            continue
       ax.scatter(vdata[i][2], vdata[i][0], vdata[i][1], c=colors[labels[i]], marker='o')
    ax.set_xlabel(' Z ')
    ax.set_ylabel(' X ')
    ax.set_zlabel(' Y ')
    path = cwd + '/figs/'+fig_dir+ '/'+ers + '/'+'All_Vox.png'
    plt.savefig(path)


    ########################
    # Run Track removal
    ########################
    cval_clean = pf.tracklike(vdata,labels)  #  Fix this into a beter function RG
    datasetidx_vclean = []
    for s in cval_clean:
        [datasetidx_vclean.append(i) for i, j in enumerate(labels) if j == s]  # This makes the datasetidx that point back to vdata
    vdata_track = [ x for x in range(len(vdata)) if x in datasetidx_vclean] 
    vdata_notrack = [ x for x in range(len(vdata)) if x not in vdata_track]


    ########################
    # Plot the tracks
    ########################
    #Now save the graphic and save it to a figs directory 
    fig0 = plt.figure()
    ax0 = fig0.add_subplot(111, projection='3d')
    for i in vdata_track: #This loop over just the return/passed clusters
        if labels[i] == -1: # HEre this might not be necessary
            continue
        ax0.scatter(vdata[i][2], vdata[i][0], vdata[i][1], c=colors[labels[i]], marker='o')
    ax0.set_xlabel(' Z ')
    ax0.set_ylabel(' X ')
    ax0.set_zlabel(' Y ')
    ax0.set_title('tracks ')
    path = cwd + '/figs/'+fig_dir+ '/'+ers + '/'+'All_Tracks.png'
    plt.savefig(path)

    ########################
    # Plot the leftovers
    ########################
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, projection='3d')
    for i in vdata_notrack: #This loop over just the return/passed clusters
        if labels[i] == -1:
            continue
        ax1.scatter(vdata[i][2], vdata[i][0], vdata[i][1], c=colors[labels[i]], marker='o')
    ax1.set_xlabel('  Z ')
    ax1.set_ylabel(' X ')
    ax1.set_zlabel(' Y ')
    ax1.set_title('track removed ')
    path = cwd + '/figs/'+fig_dir+ '/'+ers + '/'+'All_NoTrack.png'
    plt.savefig(path)

## RG Pick up clean up here
# Note to self
    ########################
    # get the primary spts 
    ########################
    tid = [ vdata[x][4] for x in vdata_track]
    ntid = [ vdata[x][4] for x in vdata_notrack]
    # This is all the index for all the tracks from voxals 
    track_fine_idx = [item for sublist in tid for item in sublist]
    notrack_fine_idx =[item for sublist in ntid for item in sublist]


    ########################
    # Work out the ROI 
    ########################
    # The ROI comes from the no track case
    # If there is cluster... the idea is assume that it is an interaction 
    # Here we will build something around that region
    #protoROI_labels = [ labels[x] for x in vdata_notrack if labels[x]!=-1] # We are not using this at the moment so let's remove
    protoROI = [ x for x in vdata_notrack if labels[x]!=-1]

    #if len(col.Counter(protoROI))==1:
	#print 'we have a solo ROI'

    # Function to take in vdata and the protoROI
    # Return the xyz_hilo
    roi_hilo = roi.roi_vox_buffer(vdata,protoROI,20.)

    print 'roi hi lo'
    for s in range(len(roi_hilo)):
	print roi_hilo[s]
    print 'roi hi lo end'




    ##################################################################################
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    ##################################################################################
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    ##################################################################################


    ########################
    # Fine Grain 
    ########################
    # Take idx from dataset so it's unique

    fine_data_ROI = [ i for i in range(len(dataset)) if dataset[i][0]>roi_hilo[0] if dataset[i][0]<roi_hilo[1] if dataset[i][1]>roi_hilo[2] if dataset[i][1]<roi_hilo[3] if dataset[i][2]>roi_hilo[4] if dataset[i][2]<roi_hilo[5] if dataset[i][3]>100 if i not in track_fine_idx]
    #fine_data_ROI = [ i for i in range(len(dataset)) if dataset[i][0]>roi_hilo[0] if dataset[i][0]<roi_hilo[1] if dataset[i][1]>roi_hilo[2] if dataset[i][1]<roi_hilo[3] if dataset[i][2]>roi_hilo[4] if dataset[i][2]<roi_hilo[5] if i not in track_fine_idx]

    print ' length of fine ' , str(len(fine_data_ROI))
    #fine_data_ROI = dh.ConvertWC_InRange_thresh('{}'.format(f),100.,roi_hilo[0],roi_hilo[1],roi_hilo[2],roi_hilo[3],roi_hilo[4],roi_hilo[5])
    ########################
    # Run the walking code for ROI
    ########################
    # This is dumb and slow
    fdata = [ [dataset[i][0],dataset[i][1],dataset[i][2], dataset[i][3]] for i in fine_data_ROI]
    flabels = pc.crawler(fdata,9,50)
    #flabels = pc.crawler(fdata,4,50)
    datasetidx_holder = mr.label_to_idxholder(flabels,150)
    # Do some merging
    nlabels = mr.PCA_merge(fdata,flabels,datasetidx_holder,0.35)
    flabels = nlabels
    datasetidx_holder = mr.label_to_idxholder(flabels,150)

    # Ok... let's see what we get.
    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111, projection='3d')
    #for i in range(len(fdata)): #This loop over just the return/passed clusters
    cl_idx_v = [item for sublist in datasetidx_holder for item in sublist]
    
    
    #ffdata = [ [fdata[i][0] ,fdata[i][1],fdata[i][2] ,fdata[i][3]] for i in cl_idx_v if flabels[i] !=-1]
    #fflabels = [ flabels[i] for i in cl_idx_v if flabels[i] !=-1]
    ## make ffdata
    ffdata = []
    fflabels = []
    for i in cl_idx_v: #This loop over just the return/passed clusters
        if flabels[i] == -1:
            continue
	ffdata.append([fdata[i][0] ,fdata[i][1],fdata[i][2] ,fdata[i][3]])
	fflabels.append(flabels[i])
        ax3.scatter(fdata[i][2], fdata[i][0], fdata[i][1], c=colors[flabels[i]], marker='o')
    ax3.set_xlabel(' Z ')
    ax3.set_ylabel(' X ')
    ax3.set_zlabel(' Y ')
    path = cwd + '/figs/'+fig_dir+ '/'+ers + '/'+'All_Fine_ROI.png'
    print path
    plt.savefig(path)    







    ########################
    ########################
    ########################
    # Run Track removal
    ########################
    #cval_clean = pf.tracklike(fdata,flabels)  #  Fix this into a beter function RG
    cval_ftracks = pf.tracklike_set(fdata,flabels,0.01)
    datasetidx_fclean = []
    for s in cval_clean:
        [datasetidx_fclean.append(i) for i, j in enumerate(flabels) if j == s]  # This makes the datasetidx that point back to vdata
    fdata_track = [ x for x in range(len(fdata)) if x in datasetidx_fclean]
    fdata_track_labels = [ flabels[x] for x in fdata_track]
    fdata_notrack = [ x for x in range(len(fdata)) if x not in fdata_track]
    fdata_notrack_labels = [ flabels[x] for x in fdata_notrack]


    # Labels above thresh 
    ftcol = col.Counter(fdata_track_labels)
    fntcol = col.Counter(fdata_notrack_labels)
    ### Setter for the  threshold for spts to be shown
    vsps_show = 150
    fdata_track_goodlabs = [ x[0] for x in ftcol.items() if  x[1]> vsps_show]
    fdata_ntrack_goodlabs = [ x[0] for x in fntcol.items() if  x[1]> vsps_show]


    #fdata_notrack_clean = [item for sublist in fnotrack_holder for item in sublist]
    ########################
    ########################
    ########################
    fig4 = plt.figure()
    ax4 = fig4.add_subplot(111, projection='3d')
    print 'the Data track collection for labels'
    print col.Counter([flabels[x] for x in fdata_track])
    #for i in fdata_track_clean: #This loop over just the return/passed clusters
    for i in fdata_track: #This loop over just the return/passed clusters
        if flabels[i] == -1:
            continue
        if flabels[i] in fdata_track_goodlabs:
            ax4.scatter(fdata[i][2], fdata[i][0], fdata[i][1], c=colors[flabels[i]], marker='o')
    ax4.set_xlabel(' Z ')
    ax4.set_ylabel(' X ')
    ax4.set_zlabel(' Y ')
    ax4.set_title(' Fine tracks ')
    path = cwd + '/figs/'+fig_dir+ '/'+ers + '/'+'All_fine_Tracks.png'
    print path
    plt.savefig(path)

    fig5 = plt.figure()
    ax5 = fig5.add_subplot(111, projection='3d')
    print 'the no data track collection for labels'
    print col.Counter([flabels[x] for x in fdata_notrack])
    print 'the good labs'
    print fdata_ntrack_goodlabs
    #for i in fdata_notrack_clean: #This loop over just the return/passed clusters
    for i in fdata_notrack: #This loop over just the return/passed clusters
        if flabels[i] == -1:
            continue
        if flabels[i] in fdata_ntrack_goodlabs:
            ax5.scatter(fdata[i][2], fdata[i][0], fdata[i][1], c=colors[flabels[i]], marker='o')
    ax5.set_xlabel(' Z ')
    ax5.set_ylabel(' X ')
    ax5.set_zlabel(' Y ')
    ax5.set_title('fine track removed ')
    path = cwd + '/figs/'+fig_dir+ '/'+ers + '/'+'All_fine_NoTrack.png'
    print path
    #plt.show()
    plt.savefig(path)

