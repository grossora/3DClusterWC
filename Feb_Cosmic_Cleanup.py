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
make_jsons = False
#make_jsons = True
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
    ''' 
    SigEVT =  mh.mc_neutron_induced_contained(f)
    print ' Is this a signal'
    if not SigEVT:
	continue
    print '^^^^ this is signal '
    ''' 

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

    #####################################################################
    #####################################################################
    ###########  Make the reconsutcion section here   ###################
    #####################################################################
    #####################################################################
    # Input will be dataset.... output will be selected pi0 clusters

    rebase_dataset, showeridx_holder, labels = Er.Reco_Shower_HolderLabels(dataset,mc_dl,jdir,jcount,make_jsons)
    print 'look we have something in a function'
    print '\n\n this is how many clusters we have ' , str(len(showeridx_holder))

    #####################################################################
    #####################################################################
    #####################################################################
    #####################################################################
    #####################################################################

#    jcount +=1
#    end = datetime.now()
#    delta = end-start
#    print 'time for an event :'
#    print delta.seconds
   # continue

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
    #6 Pi0 vtx 
    vtx_x = mc_dl[0][0][0]
    vtx_y = mc_dl[0][0][1]
    vtx_z = mc_dl[0][0][2]


    mcfullrecoline = str(jcount)+' '+str(vtx_x)+' '+str(vtx_y)+' '+str(vtx_z)
    #mcfullrecoline = str(jcount)+ ' '+ str(totmc)+' ' +str(totreco)+' ' +str(totreco_thresh) + ' ' +str(tot_shower)+ ' ' + str(tot_track)+' ' + str(totreco/totmc)+' ' + str(totreco_thresh/totreco)+' ' + str(tot_shower/totreco_thresh)+' ' + str(tot_track/totreco_thresh)+' '+str(vtx_x)+' '+str(vtx_y)+' '+str(vtx_z)


    # First... How many remaing clusters shower objects do we have
    N_Showers = len(showeridx_holder)
    print ' this is how many showers we have ' , str(N_Showers)

    # Fill out if we have N_shower==0 
    if N_Showers==0:

        dummy = [-1 for x in range(11)]
        dummyline = str(dummy).replace(',','')[1:-1]
        line = mcfullrecoline +' '+ str(N_Showers)+' '+dummyline +'\n'
        lookup.writelines(line)


    # Pairs that get keept with old cuts
    keptpairs = []

    # Run some selection code and see what happens
    for a in range(len(showeridx_holder)):

        shrA = axfi.weightshowerfit(rebase_dataset,showeridx_holder[a])
        EA = selpz.corrected_energy(rebase_dataset,showeridx_holder[a])
        ChargeA = selpz.totcharge(rebase_dataset,showeridx_holder[a])
	N_sptA = len(showeridx_holder[a])
	print ' new pair '

        if N_Showers==1:
            dummy = [-1 for x in range(9)]
            dummyline = str(dummy).replace(',','')[1:-1]
            aline =  str(N_Showers) + ' ' + str(N_sptA) + ' ' + str(ChargeA)
            line = mcfullrecoline +' '+aline+' '+ dummyline +'\n'
            lookup.writelines(line)
	    continue 

        for b in range(a+1, len(showeridx_holder)):
            shrB = axfi.weightshowerfit(rebase_dataset,showeridx_holder[b])
            EB = selpz.corrected_energy(rebase_dataset,showeridx_holder[b])
            ChargeB = selpz.totcharge(rebase_dataset,showeridx_holder[b])
	    N_sptB = len(showeridx_holder[b])
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

            # make the selection line
            selection_line = str(N_Showers) + ' ' + str(N_sptA) + ' ' + str(ChargeA) + ' '+ str(N_sptB) + ' '+ str(ChargeB) + ' '+ str(vertex[0]) + ' '+ str(vertex[1]) + ' '+ str(vertex[2]) + ' '+ str(IP) + ' '+ str(radL_a) + ' '+ str(radL_b) + ' '+ str(angle)
            line = mcfullrecoline+' '+selection_line+'\n'
            lookup.writelines(line)


            #Keep cuts 
	    if IP>20:
		continue
	    if angle <0.3:
		continue
	    if radL_a >70 or radL_b>70:
		continue		
	    keptpairs.append(a)
	    keptpairs.append(b)
	    

		
            #recomass = selpz.mass(EA,EB,angle)

    #Flatten the kept:
    kholder = []
    for a in keptpairs:
	kholder.append(showeridx_holder[a])
    if make_jsons:
        dh.MakeJson_Objects(dataset,kholder,labels,jdir,jcount,'SELshower', mc_dl)

    jcount +=1
    end = datetime.now()
    delta = end-start
    print 'time for an event :'
    print delta.seconds
 
	
	
    






