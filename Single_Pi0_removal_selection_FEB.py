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
make_jsons = True 
##Charge_thresh = 5000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
Charge_thresh = 4000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
#Charge_thresh = 3000 # Need to be set better This is used to mask over low charge spacepoints when bringing them into the Dataset
method_name = 'pi0sel_ana'
drun_dir = method_name

lookup = open('Out_text/test.txt','a+')
#lookup = open('Out_text/new_single_sel_ana_bad_wire.txt','a+')

#######################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#######################################

jcount = -1 
for f in sys.argv[1:]:
    jcount +=1
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
    #print mc_dl


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
    #tot_shower = dh.Get_Total_Object_Charge(dataset,llshoweridx_holder)
    tot_shower = dh.Get_Total_Object_Charge(rebase_dataset,showeridx_holder)

    #5 Total Track spts Charge
    # Hack for now... need to fix
    lltrackidx_holder = []
    
    tot_track = dh.Get_Total_Object_Charge(rebase_dataset,lltrackidx_holder)

    #6 Pi0 vtx 
    vtx_x = mc_dl[0][0][0]
    vtx_y = mc_dl[0][0][1]
    vtx_z = mc_dl[0][0][2]


    mcfullrecoline = str(jcount)+ ' '+ str(totmc)+' ' +str(totreco)+' ' +str(totreco_thresh) + ' ' +str(tot_shower)+ ' ' + str(tot_track)+' ' + str(totreco/totmc)+' ' + str(totreco_thresh/totreco)+' ' + str(tot_shower/totreco_thresh)+' ' + str(tot_track/totreco_thresh)+' '+str(vtx_x)+' '+str(vtx_y)+' '+str(vtx_z) 

    # Now Run the selection code
    # First... How many remaing clusters shower objects do we have
    N_Showers = len(showeridx_holder)
    # Fill out if we have N_shower==0 
    if N_Showers==0:

	dummy = [-1 for x in range(11)]
	dummyline = str(dummy).replace(',','')[1:-1]
	line = mcfullrecoline +' '+ str(N_Showers)+' '+dummyline +'\n'
        lookup.writelines(line)

    # Run some selection code and see what happens
    for a in range(len(showeridx_holder)):

	N_sptA = len(showeridx_holder[a])
	# This Makes a shower object Note This is not a defined direction 
        shrA = axfi.weightshowerfit(rebase_dataset,showeridx_holder[a])
	# This is the total sum charge
        ChargeA = selpz.totcharge(rebase_dataset,showeridx_holder[a])

        #EA = selpz.corrected_energy(dataset,llshoweridx_holder[a])
        print ' new pair '
	if N_Showers==1:
	    dummy = [-1 for x in range(9)]
	    dummyline = str(dummy).replace(',','')[1:-1]
	    aline =  str(N_Showers) + ' ' + str(N_sptA) + ' ' + str(ChargeA)
	    line = mcfullrecoline +' '+aline+' '+ dummyline +'\n'
            lookup.writelines(line)

        for b in range(a+1, len(showeridx_holder)):

	    N_sptB = len(showeridx_holder[a])
            shrB = axfi.weightshowerfit(rebase_dataset,showeridx_holder[b])
            ChargeB = selpz.totcharge(rebase_dataset,showeridx_holder[b])

            #EB = selpz.corrected_energy(dataset,llshoweridx_holder[b])

	    # Now obejcts that relate to both showers
            vertex = selpz.findvtx(shrA,shrB)
            IP = selpz.findIP(shrA,shrB)
            SP_a = selpz.findRoughShowerStart(rebase_dataset,showeridx_holder[a],vertex)
            radL_a = selpz.findconversionlength(vertex,SP_a)
            SP_b = selpz.findRoughShowerStart(rebase_dataset,showeridx_holder[b],vertex)
            radL_b = selpz.findconversionlength(vertex,SP_b)
            angle = selpz.openingangle(shrA,shrB,vertex)

            #print 'VERTEX ', str(vertex)
            #print 'IP ', str(IP)
            #print 'radL A', str(radL_a)
            #print 'radL B', str(radL_b)
	

	    # make the selection line
	    selection_line = str(N_Showers) + ' ' + str(N_sptA) + ' ' + str(ChargeA) + ' '+ str(N_sptB) + ' '+ str(ChargeB) + ' '+ str(vertex[0]) + ' '+ str(vertex[1]) + ' '+ str(vertex[2]) + ' '+ str(IP) + ' '+ str(radL_a) + ' '+ str(radL_b) + ' '+ str(angle) 
	    line = mcfullrecoline+' '+selection_line+'\n'

            lookup.writelines(line)



    ###########################

    end = datetime.now()
    delta = end-start
    print 'time for an event :'
    print delta.seconds
    print ' count ' , str(jcount)


lookup.close()
