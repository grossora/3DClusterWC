import sys, os
import Utils.datahandle as dh
import Clustering.protocluster as pc
import Utils.labelhanle as lh
import Merging.stitcher as st
import Merging.merger as mr 
import Utils.mchandle as mh
import TS_Qual.ts_separation as tss


#######################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#######################################

#Global Calls
debug = True
#make_jsons = False 
make_jsons = True 
Charge_thresh = 3000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
#Charge_thresh = 4000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
#Charge_thresh = 5000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
method_name = 'test_ts'
#method_name = 'test_4000_d4_m25_ST_l50_r20_d10'
drun_dir = method_name

#######################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#######################################

jcount = 0 
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
    # if the file is bad then continue and fill 
    ########################
    if not file_info[0]:
        continue

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
    # make the data dir for json 
    ########################
    jdir = os.getcwd() + '/Bjson/'+drun_dir+ '/'+str(jcount)   # This still is global and can be used later
    if make_jsons:
        if not os.path.isdir(jdir):
            print 'NO DIR.... making one for you'
            os.makedirs(jdir)
 
    if make_jsons:
	dh.MakeJson(f,dataset,labels,jdir,jcount,'Alg1_first_pass')


    # Pick up here with cluister stictch algos
    #######################
    #  Stitch track like clusters
    #######################
    d, labels = st.Track_Stitcher_epts(dataset,datasetidx_holder,labels,50,20,10)
    #d, labels = st.Track_Stitcher_epts(dataset,datasetidx_holder,labels,50,10,5)
 
    if make_jsons:
	dh.MakeJson(f,dataset,labels,jdir,jcount,'Alg2_stitch')

    datasetidx_holder = lh.label_to_idxholder(labels,10) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  
    if make_jsons:
	dh.MakeJson_Objects(f,dataset,datasetidx_holder,labels,jdir,jcount,'Alg2_stitch_obj')


    # Sort out the tracks
    ell = mr.make_extend_lines_list(dataset,datasetidx_holder,labels)
    labels = mr.TrackExtend_sweep(dataset,labels,ell, 10)
    datasetidx_holder = lh.label_to_idxholder(labels,10) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  
 
    if make_jsons:
	dh.MakeJson_Objects(f,dataset,datasetidx_holder,labels,jdir,jcount,'Alg3_sweep_obj')
    # Try to loop over again

    ell = mr.make_extend_lines_list(dataset,datasetidx_holder,labels)
    labels = mr.TrackExtend_sweep(dataset,labels,ell, 10)
    datasetidx_holder = lh.label_to_idxholder(labels,10) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  

    if make_jsons:
	dh.MakeJson_Objects(f,dataset,datasetidx_holder,labels,jdir,jcount,'Alg4_sweep_obj')

    d, labels = st.Track_Stitcher_epts(dataset,datasetidx_holder,labels,20,20,10)
    #labels = st.hull_touch(dataset,datasetidx_holder,labels,2)
    datasetidx_holder = lh.label_to_idxholder(labels,10) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  
   
    if make_jsons:
	dh.MakeJson_Objects(f,dataset,datasetidx_holder,labels,jdir,jcount,'Alg5_stitch_obj')

    # Sort out the tracks
    ell = mr.make_extend_lines_list(dataset,datasetidx_holder,labels)
    labels = mr.TrackExtend_sweep(dataset,labels,ell, 10)
    datasetidx_holder = lh.label_to_idxholder(labels,10) # Converts the labels list into a list of indexvalues for datasets  [ [ list of index], [list of indexes].. [] ]  
    
    if make_jsons:
	dh.MakeJson(f,dataset,labels,jdir,jcount,'Alg6_sweep')
	dh.MakeJson_Objects(f,dataset,datasetidx_holder,labels,jdir,jcount,'Alg6_sweep_obj')


    ###########################
    # track Shower Seperation 
    ###########################
    showeridx_holder, trackidx_holder  =tss.clusterspread(dataset,datasetidx_holder,0.9,10)


    if make_jsons:
	dh.MakeJson_Objects(f,dataset,showeridx_holder,labels,jdir,jcount,'Shower_obj')
	dh.MakeJson_Objects(f,dataset,trackidx_holder,labels,jdir,jcount,'Track_obj')





    jcount +=1
