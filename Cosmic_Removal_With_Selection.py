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
import Geo_Utils.axisfit as axfi
import SParams.selpizero as selpz



from datetime import datetime

#######################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#######################################

#Global Calls
debug = True
#make_jsons = False 
make_jsons = True 
#Charge_thresh = 4000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
#Charge_thresh = 5000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
Charge_thresh = 3000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
method_name = 'test'
#method_name = 'Outputs'
drun_dir = method_name

First_pass_time = []
jcount = 0 

lookup = open('Out_text/pi0_sel_test.txt','a+')



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
#    if make_jsons:
#	dh.MakeJson_Objects(dataset,datasetidx_holder,labels,jdir,jcount,'Alg2_stitch_obj',mc_dl)

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
    llshoweridx_holder, lltrackidx_holder  =cts.locallin(dataset,showeridx_holder,100,6,.6,0.85)
    #llshoweridx_holder, lltrackidx_holder  =cts.locallin(dataset,showeridx_holder,100,6,.6,0.7)
    #llshoweridx_holder, lltrackidx_holder  =cts.locallin(dataset,showeridx_holder,100,6,.8,0.7)
    #llshoweridx_holder, lltrackidx_holder  =cts.locallin(dataset,showeridx_holder,50,6,.8,0.88)
    #llshoweridx_holder, lltrackidx_holder  =cts.locallin(dataset,showeridx_holder,50,6,.88,0.95)
    #llshoweridx_holder, lltrackidx_holder  =cts.locallin(dataset,showeridx_holder,50,6,.88,0.93)

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
    #################################################
    ####     Play Ground    #########################
    #################################################
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
    #print ' these are the labels that are in the holder ' 
    post_idx =  [item for sublist in postshoweridx_holder for  item in sublist ]
    plist = [ showerlabels[i] for i in post_idx]
    #print plist
    

    if make_jsons:
	dh.MakeJson_Objects(dataset,postshoweridx_holder,showerlabels,jdir,jcount,'post_showerONLY_obj',mc_dl)


    # Many things got clustered wrong with the mergingg and sweeping... so rewalk with the post showere dataset..... basically rebase
    rebase_dataset = [ dataset[i] for i in post_idx]
    rebase_labels = pc.walker(rebase_dataset,4,25) # Runs clustering and returns labels list 
    rebase_showeridx_holder = lh.label_to_idxholder(rebase_labels,25)

    #strayidx_holder, remainidx_holder, rlabels = tss.stray_charge_removal(rebase_dataset,rebase_showeridx_holder,rebase_labels,100 , 150)
    #strayidx_holder, remainidx_holder, rlabels = tss.stray_charge_removal(rebase_dataset,rebase_showeridx_holder,rebase_labels,100 , 20)
    strayidx_holder, remainidx_holder, rlabels = tss.stray_charge_removal(rebase_dataset,rebase_showeridx_holder,rebase_labels,100 , 30)

    if make_jsons:
	dh.MakeJson_Objects(rebase_dataset,remainidx_holder,rlabels,jdir,jcount,'post_remain_showerONLY_obj',mc_dl)



    jcount +=1
    end = datetime.now()
    delta = end-start
    print 'time for an event :'
    print delta.seconds
    continue



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

    jcount +=1
    end = datetime.now()
    delta = end-start
    print 'time for an event :'
    print delta.seconds




    ###########################
    #  Write the pi0 selection ana
    ###########################


    # First... How many remaing clusters shower objects do we have
    N_Showers = len(llshoweridx_holder)
    print ' this is how many showers we have ' , str(N_Showers)

    # Run some selection code and see what happens
    for a in range(len(llshoweridx_holder)):
        shrA = axfi.weightshowerfit(dataset,llshoweridx_holder[a])
        EA = selpz.corrected_energy(dataset,llshoweridx_holder[a])
        ChargeA = selpz.totcharge(dataset,llshoweridx_holder[a])
	print ' new pair '
        for b in range(a+1, len(llshoweridx_holder)):
            shrB = axfi.weightshowerfit(dataset,llshoweridx_holder[b])
            EB = selpz.corrected_energy(dataset,llshoweridx_holder[b])
            ChargeB = selpz.totcharge(dataset,llshoweridx_holder[b])
            vertex = selpz.findvtx(shrA,shrB)
            IP = selpz.findIP(shrA,shrB)
            print 'VERTEX ', str(vertex)
            print 'IP ', str(IP)
            SP_a = selpz.findRoughShowerStart(dataset,llshoweridx_holder[a],vertex)
            #print 'SP A : ', str(SP_a)
            radL_a = selpz.findconversionlength(vertex,SP_a)
            SP_b = selpz.findRoughShowerStart(dataset,llshoweridx_holder[b],vertex)
            #print 'SP B : ', str(SP_b)
            radL_b = selpz.findconversionlength(vertex,SP_b)
            print 'radL A', str(radL_a)
            print 'radL B', str(radL_b)

            angle = selpz.openingangle(shrA,shrB,vertex)
            #recomass = selpz.mass(EA,EB,angle)


	
	
    






