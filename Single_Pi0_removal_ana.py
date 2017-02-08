import sys, os
import Utils.datahandle as dh
import Clustering.protocluster as pc
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
make_jsons = False 
#make_jsons = True 
Charge_thresh = 3000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
#Charge_thresh = 4000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
#Charge_thresh = 5000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
method_name = 'pi0test'
#method_name = 'test_ts'
#method_name = 'test_4000_d4_m25_ST_l50_r20_d10'
drun_dir = method_name

lookup = open('Out_text/single_ana_bad_wire.txt','a+')
##lookup = open('Out_text/single_ana.txt','a+')
#lookup = open('Out_text/test.txt','a+')

#######################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#######################################

jcount = 0 

for f in sys.argv[1:]:
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



    if make_jsons:
	dh.MakeJson(dataset,labels,jdir,jcount,'Alg1_first_pass',mc_dl)

    # Pick up here with cluister stictch algos
    #######################
    #  Stitch track like clusters
    #######################
    d, labels = st.Track_Stitcher_epts(dataset,datasetidx_holder,labels,50,20,10,20 )
    #d, labels = st.Track_Stitcher_epts(dataset,datasetidx_holder,labels,50,10,5)
 
    if make_jsons:
	dh.MakeJson(dataset,labels,jdir,jcount,'Alg2_stitch',mc_dl)

    datasetidx_holder = lh.label_to_idxholder(labels,10) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  
    if make_jsons:
	dh.MakeJson_Objects(dataset,datasetidx_holder,labels,jdir,jcount,'Alg2_stitch_obj',mc_dl)

    # Sort out the tracks
    ell = mr.make_extend_lines_list(dataset,datasetidx_holder,labels,20)
    labels = mr.TrackExtend_sweep(dataset,labels,ell, 10)
    datasetidx_holder = lh.label_to_idxholder(labels,10) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  
 
    if make_jsons:
	dh.MakeJson_Objects(dataset,datasetidx_holder,labels,jdir,jcount,'Alg3_sweep_obj', mc_dl)

    d, labels = st.Track_Stitcher_epts(dataset,datasetidx_holder,labels,20,20,2,20)
    datasetidx_holder = lh.label_to_idxholder(labels,10) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  
   
    if make_jsons:
        dh.MakeJson_Objects(dataset,datasetidx_holder,labels,jdir,jcount,'Alg4_stitch_obj', mc_dl)

    # Sort out the tracks
    ell = mr.make_extend_lines_list(dataset,datasetidx_holder,labels,10)
    labels = mr.TrackExtend_sweep(dataset,labels,ell, 10)
    datasetidx_holder = lh.label_to_idxholder(labels,10) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  
    
    if make_jsons:
	dh.MakeJson(dataset,labels,jdir,jcount,'Alg6_sweep',mc_dl)
	dh.MakeJson_Objects(dataset,datasetidx_holder,labels,jdir,jcount,'Alg6_sweep_obj',mc_dl)


    ###########################
    # track Shower Seperation 
    ###########################

    showeridx_holder, trackidx_holder  =tss.clusterspread(dataset,datasetidx_holder,900,50)


    if make_jsons:
	dh.MakeJson_Objects(dataset,showeridx_holder,labels,jdir,jcount,'Shower_obj',mc_dl)
	dh.MakeJson_Objects(dataset,trackidx_holder,labels,jdir,jcount,'Track_obj',mc_dl)


    llshoweridx_holder, lltrackidx_holder  =cts.locallin(dataset,showeridx_holder,50,6,.88,0.93)

    if make_jsons:
	dh.MakeJson_Objects(dataset,llshoweridx_holder,labels,jdir,jcount,'llShower_obj',mc_dl)
	dh.MakeJson_Objects(dataset,trackidx_holder+lltrackidx_holder,labels,jdir,jcount,'llTrack_obj',mc_dl)


    ###########################
    # Ana for Out 
    ###########################
    #1 Total MC spts Charge 
    totmc = dh.Get_Total_MC_Charge(f)
    
    #2 Total Reco spts Charge
    totreco = dh.Get_Total_Reco_Charge(f)

    #3 Total Reco_Thres spts Charge
    totreco_thresh = dh.Get_Total_Thresh_Charge(f,Charge_thresh)

    #4 Total Shower spts Charge
    tot_shower = dh.Get_Total_Object_Charge(dataset,showeridx_holder)

    #5 Total Track spts Charge
    tot_track = dh.Get_Total_Object_Charge(dataset,trackidx_holder)

    #6 Pi0 vtx 
    vtx_x = mc_dl[0][0][0]
    vtx_y = mc_dl[0][0][1]
    vtx_z = mc_dl[0][0][2]
 
    print ' this is the vertex' 
    print str(vtx_x)
    print str(vtx_y)
    print str(vtx_z)


    
    line = str(totmc)+' ' +str(totreco)+' ' +str(totreco_thresh) + ' ' +str(tot_shower)+ ' ' + str(tot_track)+' ' + str(totreco/totmc)+' ' + str(totreco_thresh/totreco)+' ' + str(tot_shower/totreco_thresh)+' ' + str(tot_track/totreco_thresh)+' '+str(vtx_x)+' '+str(vtx_y)+' '+str(vtx_z) +'\n'
    print line
    lookup.writelines(line)


    ###########################



    jcount +=1
    end = datetime.now()
    delta = end-start
    print 'time for an event :'
    print delta.seconds


lookup.close()
