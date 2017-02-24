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
import Selection.Reco_Clusters as Er

from datetime import datetime

#######################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#######################################
#Global Calls
debug = True
make_jsons = True
#Charge_thresh = 100000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
Charge_thresh = 4000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
method_name = 'test'
drun_dir = method_name
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
    if not SigEVT:
	continue
    print '^^^^ this is signal '

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


    ### Quick break out for finding file numbers
    jcount +=1
    continue

    ########################
    #Bring in  Dataset 
    ########################
    dataset = dh.ConvertWC_InTPC_thresh('{}'.format(f),Charge_thresh)

    #####################################################################
    #####################################################################
    ###########  Make the reconsutcion section here   ###################
    #####################################################################
    #####################################################################
    # Input will be dataset.... output will be selected pi0 clusters

    rebase_dataset, showeridx_holder, labels = Er.Reco_Shower_HolderLabels(dataset,mc_dl,jdir,jcount)
    print 'look we have something in a function'
    print '\n\n this is how many clusters we have ' , str(len(showeridx_holder))

    #####################################################################
    #####################################################################
    #####################################################################
    #####################################################################
    #####################################################################


    jcount +=1
    end = datetime.now()
    delta = end-start
    print 'time for an event :'
    print delta.seconds
    continue


#######################################################################################

    #####################################################################
    #####################################################################
    ###########  Make the selection section here   ######################
    #####################################################################
    #####################################################################

    # Input will be clusters .... output will be matched pairs
    

    

    #####################################################################
    #####################################################################
    #####################################################################
    #####################################################################
    #####################################################################






    ###########################
    #  Write the pi0 selection ana
    ###########################


    # First... How many remaing clusters shower objects do we have
    N_Showers = len(showeridx_holder)
    print ' this is how many showers we have ' , str(N_Showers)

    # Run some selection code and see what happens
    for a in range(len(showeridx_holder)):
        shrA = axfi.weightshowerfit(rebase_dataset,showeridx_holder[a])
        EA = selpz.corrected_energy(rebase_dataset,showeridx_holder[a])
        ChargeA = selpz.totcharge(rebase_dataset,showeridx_holder[a])
	print ' new pair '
        for b in range(a+1, len(showeridx_holder)):
            shrB = axfi.weightshowerfit(rebase_dataset,showeridx_holder[b])
            EB = selpz.corrected_energy(rebase_dataset,showeridx_holder[b])
            ChargeB = selpz.totcharge(rebase_dataset,showeridx_holder[b])
            vertex = selpz.findvtx(shrA,shrB)
            IP = selpz.findIP(shrA,shrB)
            print 'VERTEX ', str(vertex)
            print 'IP ', str(IP)
            SP_a = selpz.findRoughShowerStart(rebase_dataset,showeridx_holder[a],vertex)
            #print 'SP A : ', str(SP_a)
            radL_a = selpz.findconversionlength(vertex,SP_a)
            SP_b = selpz.findRoughShowerStart(rebase_dataset,showeridx_holder[b],vertex)
            #print 'SP B : ', str(SP_b)
            radL_b = selpz.findconversionlength(vertex,SP_b)
            print 'radL A', str(radL_a)
            print 'radL B', str(radL_b)

            angle = selpz.openingangle(shrA,shrB,vertex)
            #recomass = selpz.mass(EA,EB,angle)


	
	
    






