import numpy as np 
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
import Geo_Utils.axisfit as axfi
import SParams.selpizero as selpz







def Reco_Shower_HolderLabels( dataset, mc_dl , jdir, jcount , make_jsons=True):
    # This will take in a dataset and file information
    # Returns a rebased dataset, clustered index holder for showers, labels :  with candidate shower events 


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
    showeridx_holder, trackidx_holder  =tss.clusterspread(dataset,datasetidx_holder,5000,50)
    #showeridx_holder, trackidx_holder  =tss.clusterspread(dataset,datasetidx_holder,500,50)

    ########################
    # Make Jsons
    ########################
    if make_jsons:
        dh.MakeJson_Objects(dataset,showeridx_holder,labels,jdir,jcount,'Shower_obj',mc_dl)
        dh.MakeJson_Objects(dataset,trackidx_holder,labels,jdir,jcount,'Track_obj',mc_dl)


    ###########################
    # Identify Crossing Track 
    ###########################
    llshoweridx_holder, lltrackidx_holder  =cts.locallin(dataset,showeridx_holder,100,6,.6,0.7)

    ########################
    # Make Jsons
    ########################
    if make_jsons:
        dh.MakeJson_Objects(dataset,llshoweridx_holder,labels,jdir,jcount,'llShower_obj',mc_dl)
        dh.MakeJson_Objects(dataset,trackidx_holder+lltrackidx_holder,labels,jdir,jcount,'llTrack_obj',mc_dl)


    # Now take the tracks and carve out volumes using shower space points? 

    pell = mr.make_extend_lines_list(dataset,trackidx_holder+lltrackidx_holder,labels, 20)
    labels = mr.TrackExtend_sweep(dataset,labels,pell,10,1)
    # This is now goinng over all of the datapoints  This might be a little slow
    posttrackidx_holder = lh.label_to_idxholder(labels,25)

    if make_jsons:
        dh.MakeJson_Objects(dataset,posttrackidx_holder,labels,jdir,jcount,'post_obj',mc_dl)



    #################################################
    ############### not at clean ... sorry ##########
    #################################################


    showerlabels = mr.TrackExtend_sweep_ShowerLabels(dataset,labels,pell,10,1)
    # Do it right here... for now 
    # make the flat idx list for showers 
    flat_showeridx =  [item for sublist in llshoweridx_holder for  item in sublist ]
    for i in range(len(dataset)):
        if showerlabels==-1:
            continue
        if i in flat_showeridx:
            continue
        showerlabels[i] = -1

    postshoweridx_holder = lh.label_to_idxholder(showerlabels,25)

    ##### TEMP
    post_idx =  [item for sublist in postshoweridx_holder for  item in sublist ]
    plist = [ showerlabels[i] for i in post_idx]
    #print plist


    if make_jsons:
        dh.MakeJson_Objects(dataset,postshoweridx_holder,showerlabels,jdir,jcount,'post_showerONLY_obj',mc_dl)


    # Many things got clustered wrong with the mergingg and sweeping... so rewalk with the post showere dataset..... basically rebase
    rebase_dataset = [ dataset[i] for i in post_idx]
    rebase_labels = pc.walker(rebase_dataset,4,25) # Runs clustering and returns labels list 
    rebase_showeridx_holder = lh.label_to_idxholder(rebase_labels,25)

    strayidx_holder, remainidx_holder, rlabels = tss.stray_charge_removal(rebase_dataset,rebase_showeridx_holder,rebase_labels,100 , 30)

    if make_jsons:
        dh.MakeJson_Objects(rebase_dataset,remainidx_holder,rlabels,jdir,jcount,'post_remain_showerONLY_obj',mc_dl)

    # These are the remaining shower like clusters
    return rebase_dataset, rebase_showeridx_holder, rebase_labels 
    


