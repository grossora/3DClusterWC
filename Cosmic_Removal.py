import sys, os
import Utils.datahandle as dh
import Clustering.protocluster as pc
import Clustering.postcluster as postc
import Utils.labelhanle as lh
import Merging.stitcher as st
import Merging.merger as mr 
import Utils.mchandle as mh
import TS_Qual.ts_separation as tss
import TS_Qual.crossingtracks as cts
import Utils.mchandle as mh


from datetime import datetime

#######################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#######################################

#Global Calls
debug = True
#make_jsons = False 
make_jsons = True 
Charge_thresh = 3000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
method_name = 'Outputs'
drun_dir = method_name

First_pass_time = []
First_pass_time = []

jcount = 0 
#######################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#######################################


for f in sys.argv[1:]:

    # This is for checking process time for things
    start = datetime.now()

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
    # Is this a Signal Event  AKA One neutron induced pi0
    ########################
    SigEVT =  mh.mc_neutron_induced_contained(f)
    print ' Is this a signal'
    print SigEVT
    if not SigEVT:
	continue

    ########################
    # mc_datalabel info
    # Call this once and get the mc info for the jsons for later
    ########################
    mc_dl =  mh.mc_Obj_points(mh.mc_neutron_induced_OBJ(f))

    ########################
    # if the file is bad then continue and fill 
    ########################
    if not file_info[0]:
        continue

    ########################
    # make the data dir for json 
    ########################
    jdir = os.getcwd() + '/Bjson/'+drun_dir+ '/'+str(jcount)   # This still is global and can be used later
    if make_jsons:
        if not os.path.isdir(jdir):
            print 'NO DIR.... making one for you'
            os.makedirs(jdir)

    ########################
    # Print out all the MC Spacepts 
    # Print out all the WC-Reco Spacepts 
    ########################
    if make_jsons:
        dh.MakeJsonMC(f,jdir,jcount,'AlgMC',mc_dl)

    if make_jsons:
        dh.MakeJsonReco(f,jdir,jcount,'AlgSPT',mc_dl)

    ########################
    #Bring in  Dataset 
    ########################
    dataset = dh.ConvertWC_InTPC_thresh('{}'.format(f),Charge_thresh)
    print 'Size of dataset', str(len(dataset))

    ########################
    # cluster the event into something 
    ########################
    labels = pc.walker(dataset,4,25) # Runs clustering and returns labels list 
    datasetidx_holder = lh.label_to_idxholder(labels,25) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  

    ########################
    # Make Jsons
    ########################
    if make_jsons:
	dh.MakeJson(dataset,labels,jdir,jcount,'Alg1_first_pass',mc_dl)

    #######################
    #  Stitch track like clusters
    #######################
    d, labels = st.Track_Stitcher_epts(dataset,datasetidx_holder,labels,100,20,2.0,0.16,10 )
    # STICH :  dataset,datasetidx_holder,labels,gap_dist,k_radius,min_pdelta, angle_error,min_clust_length
    datasetidx_holder = lh.label_to_idxholder(labels,25) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  

    ########################
    # Make Jsons
    ########################
    if make_jsons:
	dh.MakeJson_Objects(dataset,datasetidx_holder,labels,jdir,jcount,'Alg2_stitch_obj',mc_dl)

    ########################
    # Sweep algo 
    ########################
    ell = mr.make_extend_lines_list(dataset,datasetidx_holder,labels, 20)
    labels = mr.TrackExtend_sweep(dataset,labels,ell,25)
    datasetidx_holder = lh.label_to_idxholder(labels,25) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  
 
    ########################
    # Make Jsons
    ########################
    if make_jsons:
	dh.MakeJson_Objects(dataset,datasetidx_holder,labels,jdir,jcount,'Alg3_sweep_obj', mc_dl)

    ###########################
    # track Shower Seperation 
    ###########################
    showeridx_holder, trackidx_holder  =tss.clusterspread(dataset,datasetidx_holder,500,50)

    ########################
    # Make Jsons
    ########################
    if make_jsons:
	dh.MakeJson_Objects(dataset,showeridx_holder,labels,jdir,jcount,'Shower_obj',mc_dl)
	dh.MakeJson_Objects(dataset,trackidx_holder,labels,jdir,jcount,'Track_obj',mc_dl)

    ###########################
    # Identify Crossing Track 
    ###########################
    llshoweridx_holder, lltrackidx_holder  =cts.locallin(dataset,showeridx_holder,50,6,.88,0.93)

    ########################
    # Make Jsons
    ########################
    if make_jsons:
	dh.MakeJson_Objects(dataset,llshoweridx_holder,labels,jdir,jcount,'llShower_obj',mc_dl)
	dh.MakeJson_Objects(dataset,trackidx_holder+lltrackidx_holder,labels,jdir,jcount,'llTrack_obj',mc_dl)

    #######################################################################################################
    #######################################################################################################
    #######################################################################################################
    #######################################################################################################


    ########################
    # Look at post clustering for things
    ########################
    labels = postc.cluster_volumes_keep(dataset,labels,ell,5)
    #labels = postc.cluster_volumes(dataset,ell,3)
    datasetidx_holder = lh.label_to_idxholder(labels,10) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  

    print ' looking at things that just goit clustered after the post step '
    print ' size of dataset ', str(len(dataset))
    print ' size of unclustered ' , str(labels.count(-1))

    if make_jsons:
	dh.MakeJson(dataset,labels,jdir,jcount,'RePass_Alg1',mc_dl)

    #d, labels = st.Track_Stitcher_epts(dataset,datasetidx_holder,labels,50,20,10,20 )
    d, labels = st.Track_Stitcher_epts(dataset,datasetidx_holder,labels,100,20,2.0,0.16,10 )
    datasetidx_holder = lh.label_to_idxholder(labels,10) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  

    if make_jsons:
	dh.MakeJson_Objects(dataset,datasetidx_holder,labels,jdir,jcount,'repass_alg2_stitch',mc_dl)

    ######################### Try SOMETHING WITH MORE POINTS###############


    ###########################
    # track Shower Seperation 
    ###########################
    showeridx_holder, trackidx_holder  =tss.clusterspread(dataset,datasetidx_holder,500,50)
    llshoweridx_holder, lltrackidx_holder  =cts.locallin(dataset,showeridx_holder,50,6,.88,0.93)

    if make_jsons:
	dh.MakeJson_Objects(dataset,llshoweridx_holder,labels,jdir,jcount,'Repass_Shower_obj',mc_dl)
	dh.MakeJson_Objects(dataset,trackidx_holder+lltrackidx_holder,labels,jdir,jcount,'Repass_Track_obj',mc_dl)


    '''

    full_dataset = dh.ConvertWC_InTPC_thresh('{}'.format(f),0.0)
    print 'Size of full_dataset', str(len(full_dataset))
    labels = postc.cluster_volumes(full_dataset,ell,10)
    #labels = postc.cluster_volumes(full_dataset,ell,3)
    datasetidx_holder = lh.label_to_idxholder(labels,10) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  
    print ' size of unclustered ' , str(labels.count(-1))

    if make_jsons:
	dh.MakeJson(full_dataset,labels,jdir,jcount,'Full_RePass_Alg1',mc_dl)

    d, labels = st.Track_Stitcher_epts(full_dataset,datasetidx_holder,labels,50,20,10,20 )
    datasetidx_holder = lh.label_to_idxholder(labels,10) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  
 
    if make_jsons:
	dh.MakeJson_Objects(full_dataset,datasetidx_holder,labels,jdir,jcount,'Full_Repass_alg2_stitch',mc_dl)

    '''


    jcount +=1
    end = datetime.now()
    delta = end-start
    print 'time for an event :'
    print delta.seconds
