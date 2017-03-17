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

from datetime import datetime
   
#################################################################################
#################################################################################
#################################################################################


def Reco_trackshower( dataset, mc_dl , jdir, jcount , make_jsons=True,timer=False):
    # Need some type of config 
    min_spts = 20
    nn_dist = 6
    # This will take in a dataset and file information
    # Returns a rebased dataset, clustered index holder for showers, labels :  with candidate shower events 
    ########################
    # cluster the event into something 
    ########################
    time_v = []  #  Walker, js, Stitch, js, cluster_sep, 2js, extend, 2js, stray, js
    start = datetime.now()

    labels = pc.walker(dataset,nn_dist,min_spts) # Runs clustering and returns labels list 
    if timer:
	tdelta = datetime.now() - start 
	time_v.append(tdelta.seconds)
        start = datetime.now()

    datasetidx_holder = lh.label_to_idxholder(labels,min_spts) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  

    if timer:
	tdelta = datetime.now() - start 
	time_v.append(tdelta.seconds)
        start = datetime.now()

    ########################
    # Make Jsons
    ########################
    if make_jsons:
        dh.MakeJson(dataset,labels,jdir,jcount,'Alg1_first_pass',mc_dl)
    if timer:
	tdelta = datetime.now() - start 
	time_v.append(tdelta.seconds)
        start = datetime.now()

    #######################
    #  Stitch track like clusters
    #######################
    d, labels = st.Track_Stitcher_epts(dataset,datasetidx_holder,labels,100,20,2.0,0.16,10 )
    # STICH :  dataset,datasetidx_holder,labels,gap_dist,k_radius,min_pdelta, angle_error,min_clust_length
    datasetidx_holder = lh.label_to_idxholder(labels,min_spts) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  
    if timer:
	tdelta = datetime.now() - start 
	time_v.append(tdelta.seconds)
        start = datetime.now()

    ########################
    # Make Jsons
    ########################
    if make_jsons:
        dh.MakeJson_Objects(dataset,datasetidx_holder,labels,jdir,jcount,'Alg2_stitch_obj', mc_dl)
    if timer:
	tdelta = datetime.now() - start 
	time_v.append(tdelta.seconds)
        start = datetime.now()

    ###########################
    # track Shower Seperation 
    # based on length 
    ###########################
    #showeridx_holder, trackidx_holder  =tss.clusterlength_sep(dataset,datasetidx_holder,50)
    showeridx_holder, trackidx_holder  =tss.cluster_lhull_length_cut(dataset,datasetidx_holder,50)
    #showeridx_holder, trackidx_holder  =tss.clusterspread(dataset,datasetidx_holder,5000,50)
    if timer:
	tdelta = datetime.now() - start 
	time_v.append(tdelta.seconds)
        start = datetime.now()
 
    ########################
    # Make Jsons
    ########################
    if make_jsons:
        dh.MakeJson_Objects(dataset,showeridx_holder,labels,jdir,jcount,'Shower_len_obj',mc_dl)
        dh.MakeJson_Objects(dataset,trackidx_holder,labels,jdir,jcount,'Track_len_obj',mc_dl)
    if timer:
	tdelta = datetime.now() - start 
	time_v.append(tdelta.seconds)
        start = datetime.now()

    ########################
    # Sweep the shower objects using track volumes
    ########################
    ell = mr.make_extend_lines_list(dataset,trackidx_holder,labels)
    #ell = mr.make_extend_lines_list(dataset,trackidx_holder,labels, 10)

    showeridx_holder, Strackidx_holder, labels = mr.TrackExtend_sweep_holders(dataset,showeridx_holder,labels,ell,10)
    #showeridx_holder, Strackidx_holder, labels = mr.TrackExtend_sweep_holders(dataset,showeridx_holder,labels,ell,5)
    #datasetidx_holder = lh.label_to_idxholder(labels,25) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  
    if timer:
	tdelta = datetime.now() - start 
	time_v.append(tdelta.seconds)
        start = datetime.now()

    ########################
    # Make Jsons
    ########################
    if make_jsons:
        dh.MakeJson_Objects(dataset,Strackidx_holder,labels,jdir,jcount,'Alg3_T_sweep_obj', mc_dl)
        dh.MakeJson_Objects(dataset,showeridx_holder,labels,jdir,jcount,'Alg3_S_sweep_obj', mc_dl)
    if timer:
	tdelta = datetime.now() - start 
	time_v.append(tdelta.seconds)
        start = datetime.now()
    # cut out showers based on PCA cuts 
    ########################

    out_shower_holder , in_tracks_holder = tss.clusterspreadR(dataset,showeridx_holder, vari_lo=0.99, vari_hi=1, moment = 0 )
    out2_shower_holder , in2_tracks_holder = tss.clusterspreadR(dataset,out_shower_holder, vari_lo=0.0, vari_hi=0.002, moment = 1 )
    
    ########################
    # Make Jsons
    ########################
    if make_jsons:
        dh.MakeJson_Objects(dataset,out2_shower_holder,labels,jdir,jcount,'PCA_shower_obj', mc_dl)
        dh.MakeJson_Objects(dataset,in2_tracks_holder+in_tracks_holder,labels,jdir,jcount,'PCA_track_obj', mc_dl)

    #if timer: 
    #    return trackidx_holder , out2_shower_holder , labels, time_v
    #return trackidx_holder , out2_shower_holder , labels



    # Carefull with keeping objects
    strayidx_holder, showeridx_holder, rlabels = tss.stray_charge_removal(dataset,showeridx_holder,labels,100 , 30)
    #strayidx_holder, remainidx_holder, rlabels = tss.stray_charge_removal(dataset,showeridx_holder,labels,100 , 30)
    ########################
    # Make Jsons
    ########################
    if make_jsons:
        dh.MakeJson_Objects(dataset,showeridx_holder,labels,jdir,jcount,'remain_shower_obj', mc_dl)

    if timer: 
        return trackidx_holder , showeridx_holder , labels, time_v
    return trackidx_holder , showeridx_holder , labels



#############################################################################################################

def rebase_Full_reco(dataset,mc_dl , jdir, jcount , make_jsons=True,timer=False):
    # Start of a robust clustering and reco	

    ########################
    # cluster using tight NN
    ########################
    labels = pc.crawlernn(dataset, 4, 20 ) # Runs clustering and returns labels list 
    datasetidx_holder = lh.label_to_idxholder(labels,20) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  

    ########################
    # Make Jsons
    ########################
    if make_jsons:
        dh.MakeJson(dataset,labels,jdir,jcount,'rebase_Alg1',mc_dl)

    trackidx_holder = []
    showeridx_holder = []

    return trackidx_holder , showeridx_holder , labels

#############################################################################################################


##########################3
### OLD OLD OLD
##########################3


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
    ell = mr.make_extend_lines_list(dataset,datasetidx_holder,labels, 20) #<== RG This can be changed
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
 

'''
    strayidx_holder, remainidx_holder, rlabels = tss.stray_charge_removal(dataset,showeridx_holder,labels,100 , 36)
    if timer:
	tdelta = datetime.now() - start 
	time_v.append(tdelta.microseconds/1000.)
        start = datetime.now()
    if make_jsons:
        dh.MakeJson_Objects(dataset,remainidx_holder,rlabels,jdir,jcount,'post_remain_showerONLY_obj',mc_dl)
    if timer:
	tdelta = datetime.now() - start 
	time_v.append(tdelta.microseconds/1000.)
        start = datetime.now()

    # Find out which showers are left
    # This is not correct
    if timer: 
        return trackidx_holder , remainidx_holder , rlabels, time_v
    return trackidx_holder , remainidx_holder , rlabels
'''
