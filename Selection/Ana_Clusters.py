import numpy as np
from sklearn.decomposition import PCA
from scipy.spatial import ConvexHull

import Utils.datahandle as dh
import Utils.mchandle as mh
import Geo_Utils.axisfit as axfi
import Geo_Utils.wpca as wp 
import SParams.selpizero as selpz


def Ana_Object(dataset, holder, jcount,mc_dl, filename = 'test_ana_obj'):
    lookup = open('Out_text/{}.txt'.format(filename),'a+')
    for a in holder:
	n_objects = len(holder)
	n_spts = len(a)
	points_v = []
	points_wts_v = []
	q_v = []
	length = -999
	area = -999
	volume = -999
	pav = [ -999, -999, -999]
	pavr = [ -999, -999, -999]

	for i in a:
	    q_v.append(dataset[i][3])
	    pt = [ dataset[i][0],dataset[i][1],dataset[i][2]]
	    wt_q = [ dataset[i][3],dataset[i][3],dataset[i][3]]
            points_v.append(pt)
            points_wts_v.append(wt_q)
	q_tot = np.sum(q_v)
	avg_xyz = np.average(points_v,axis=0) 
	Wavg_xyz = np.average(points_v,axis=0, weights = q_v) 
	####################
	#try to make a hull
	####################
        try:
            hull = ConvexHull(points_v)
            min_bd = hull.min_bound
            max_bd = hull.max_bound
            # distance using NP 
            x_min = min_bd[0]
            y_min = min_bd[1]
            z_min = min_bd[2]
            x_max = max_bd[0]
            y_max = max_bd[1]
            z_max = max_bd[2]
            length = pow((x_max-x_min)*(x_max-x_min) + (y_max-y_min)*(y_max-y_min) + (z_max-z_min)*(z_max-z_min),0.5)
            #length = pow((x_max-x_min)*(x_max-x_min) + (z_max-z_min)*(z_max-z_min) + (z_max-z_min)*(z_max-z_min),0.5)
	    area = hull.area
	    volume = hull.volume

        except:
	    good_hull = False
	####################
	#try to make a hull
	####################
        try:
            #pca = PCA(n_components=3)
            #pca.fit(points_v)
            pca = wp.WPCA(n_components=3)
            pca.fit(points_v,weights= points_wts_v )
	    pav =  pca.explained_variance_
	    pavr =  pca.explained_variance_ratio_
 
        except:
	    good_PCA = False
	
        # Make the string
	hull_string = str(length) + ' ' + str(area) + ' ' + str(volume)
	pca_string = str(pav[0]) + ' ' + str(pav[1]) + ' ' + str(pav[2]) + ' ' +str(pavr[0]) + ' ' + str(pavr[1]) + ' ' + str(pavr[2])
	pts_string = str(q_tot) + ' ' + str(avg_xyz[0])+' ' + str(avg_xyz[1])+' ' + str(avg_xyz[2])+ ' ' + str(Wavg_xyz[0])+' ' + str(Wavg_xyz[1])+' ' + str(Wavg_xyz[2])
        mc_string = F_pi0_vtx(mc_dl)
	ret_string = str(jcount)+' '+mc_string +' '+str(n_objects)+' '+str(n_spts)+ ' ' + pts_string + ' ' + hull_string +' ' + pca_string+ '\n'
	
	# Write the string to the file
	lookup.writelines(ret_string)

    lookup.close()
    return


#==========================================================================================================
def Pi0_Ana_Object(f, Charge_thresh, dataset, shower_holder, track_holder, jcount,mc_dl,ts='shower', filename = 'pi0_ana_obj'):
    lookup = open('Out_text/{}.txt'.format(filename),'a+')
    if ts=='shower':
	holder = shower_holder
    if ts=='track':
	holder = track_holder
    for a in holder:
	n_objects = len(holder)
	n_spts = len(a)
	points_v = []
	points_wts_v = []
	q_v = []
	length = -999
	area = -999
	volume = -999
	pav = [ -999, -999, -999]
	pavr = [ -999, -999, -999]
	good_hull = True
	good_PCA = True

	for i in a:
	    q_v.append(dataset[i][3])
	    pt = [ dataset[i][0],dataset[i][1],dataset[i][2]]
	    wt_q = [ dataset[i][3],dataset[i][3],dataset[i][3]]
            points_v.append(pt)
            points_wts_v.append(wt_q)
	q_tot = np.sum(q_v)
	avg_xyz = np.average(points_v,axis=0) 
	Wavg_xyz = np.average(points_v,axis=0, weights = q_v) 
	####################
	#try to make a hull
	####################
        try:
            hull = ConvexHull(points_v)
            min_bd = hull.min_bound
            max_bd = hull.max_bound
            # distance using NP 
            x_min = min_bd[0]
            y_min = min_bd[1]
            z_min = min_bd[2]
            x_max = max_bd[0]
            y_max = max_bd[1]
            z_max = max_bd[2]
            length = pow((x_max-x_min)*(x_max-x_min) + (y_max-y_min)*(y_max-y_min) + (z_max-z_min)*(z_max-z_min),0.5)
            #length = pow((x_max-x_min)*(x_max-x_min) + (z_max-z_min)*(z_max-z_min) + (z_max-z_min)*(z_max-z_min),0.5)
	    area = hull.area
	    volume = hull.volume

        except:
	    good_hull = False
	####################
	#try to make a hull
	####################
        try:
            #pca = PCA(n_components=3)
            #pca.fit(points_v)
            pca = wp.WPCA(n_components=3)
            pca.fit(points_v,weights= points_wts_v )
	    pav =  pca.explained_variance_
	    pavr =  pca.explained_variance_ratio_
	    test_string = str(pav[0]) + ' ' + str(pav[1]) + ' ' + str(pav[2]) + ' ' +str(pavr[0]) + ' ' + str(pavr[1]) + ' ' + str(pavr[2])
 
        except:
	    good_PCA = False
	
        # Make the string
	hull_string = '-1' + ' ' + '-1' + ' ' +'-1' 
	if good_hull:
	    hull_string = str(length) + ' ' + str(area) + ' ' + str(volume)
	pca_string = '-1' + ' ' + '-1' + ' ' + '-1' + ' ' +'-1' + ' ' + '-1' + ' ' + '-1'
	if good_PCA:
	    pca_string = str(pav[0]) + ' ' + str(pav[1]) + ' ' + str(pav[2]) + ' ' +str(pavr[0]) + ' ' + str(pavr[1]) + ' ' + str(pavr[2])
	pts_string = str(q_tot) + ' ' + str(avg_xyz[0])+' ' + str(avg_xyz[1])+' ' + str(avg_xyz[2])+ ' ' + str(Wavg_xyz[0])+' ' + str(Wavg_xyz[1])+' ' + str(Wavg_xyz[2])
	mc_string = F_pi0_vtx(mc_dl)
	dep_string = F_mc_pi0_fracs(f, dataset,Charge_thresh,shower_holder,track_holder,mc_dl)
	ret_string = str(jcount)+' '+mc_string +' '+dep_string+' '+str(n_objects)+' '+str(n_spts)+ ' ' + pts_string + ' ' + hull_string +' ' + pca_string+ '\n'
	
	# Write the string to the file
	lookup.writelines(ret_string)

    lookup.close()
    return


#==========================================================================================================
def Ana_Pi0_mc_pair_vtx(f,Charge_thresh,dataset,jcount, shower_holder, track_holder,  mc_dl,filename = 'pi0_pair_ana' ,ts='shower'):
    lookup = open('Out_text/{}.txt'.format(filename),'a+')

    mc_string = mh.piz_mc_info(f)
    dep_string = F_mc_pi0_fracs(f, dataset,Charge_thresh,shower_holder,track_holder,mc_dl)

    if ts=='shower':
	holder = shower_holder
    if ts=='track':
	holder = track_holder

    # Loop over the pairs and return the vertex string
    N_Showers = len(holder)
    if len(holder) ==0:
	# Return the string with -9
	fill = str('-9 ')*12
        fillline = str(jcount)+ ' '+ str(N_Showers)  + ' ' + mc_string+ ' '+dep_string+' '+ fill.rsplit(' ',1)[0] + '\n'  
	lookup.writelines(fillline)
	lookup.close()
	return
        
    if len(holder) ==1:
	# Fill this with what we can eventually
	fill = str('-1 ')*12
        fillline = str(jcount)+ ' '+ str(N_Showers)  + ' ' + mc_string+ ' '+dep_string+' '+ fill.rsplit(' ',1)[0] + '\n'  
	lookup.writelines(fillline)
	lookup.close()
	return
 
    for a in range(len(holder)):
        shrA = axfi.weightshowerfit(dataset,holder[a])
        EA = selpz.corrected_energy(dataset,holder[a])
        ChargeA = selpz.totcharge(dataset,holder[a])
        N_sptA = len(holder[a])

        for b in range(a+1,len(holder)):
            shrB = axfi.weightshowerfit(dataset,holder[b])
            EB = selpz.corrected_energy(dataset,holder[b])
            ChargeB = selpz.totcharge(dataset,holder[b])
            N_sptB = len(holder[b])
            vertex = selpz.findvtx(shrA,shrB)
            IP = selpz.findIP(shrA,shrB)

            SP_a = selpz.findRoughShowerStart(dataset,holder[a],vertex)
            radL_a = selpz.findconversionlength(vertex,SP_a)
            SP_b = selpz.findRoughShowerStart(dataset,holder[b],vertex)
            radL_b = selpz.findconversionlength(vertex,SP_b)
            angle = selpz.openingangle(shrA,shrB,vertex)

            selection_line = str(N_sptA) + ' ' + str(ChargeA) + ' '+ str(N_sptB) + ' '+ str(ChargeB) + ' '+ str(vertex[0]) + ' '+ str(vertex[1]) + ' '+ str(vertex[2]) + ' '+ str(IP) + ' '+ str(radL_a) + ' '+ str(radL_b) + ' '+ str(angle)
	    
	    # Distance to vertex  This can be better... ugly
	    vtx_diff = pow( pow(vertex[0]-mc_dl[0][0][0],2) + pow(vertex[1]-mc_dl[0][0][1],2)+ pow(vertex[2]-mc_dl[0][0][2],2), 0.5)
           # mcfullrecoline = str(jcount)+ ' '+ str(N_Showers)  + ' ' + mc_string+ ' '+str(vtx_diff)+' '+ selection_line + '\n'  
            mcfullrecoline = str(jcount)+ ' '+ str(N_Showers)  + ' ' + mc_string+' '+ dep_string+ ' '+str(vtx_diff)+' '+ selection_line + '\n'  

            #mcfullrecoline = str(jcount)+ ' '+ str(N_Showers)  + ' ' + mc_string+ ' '+str(vtx_diff)+' '+ selection_line + '\n'  
	    lookup.writelines(mcfullrecoline)
    lookup.close()
    return 





#==========================================================================================================
def Ana_CPi0_mc_pair_vtx(f,Charge_thresh,dataset,jcount, shower_holder, track_holder,  mc_dl,filename = 'pi0_pair_ana' ,ts='shower'):
    lookup = open('Out_text/{}.txt'.format(filename),'a+')

    mc_string = mh.piz_mc_info(f)
    dep_string = F_mc_pi0_fracs(f, dataset,Charge_thresh,shower_holder,track_holder,mc_dl)

    if ts=='shower':
	holder = shower_holder
    if ts=='track':
	holder = track_holder

    # Loop over the pairs and return the vertex string
    N_Showers = len(holder)
    if len(holder) ==0:
	# Return the string with -9
	fill = str('-9 ')*12
        fillline = str(jcount)+ ' '+ str(N_Showers)  + ' ' + mc_string+ ' '+dep_string+' '+ fill.rsplit(' ',1)[0] + '\n'  
	lookup.writelines(fillline)
	lookup.close()
	return
        
    if len(holder) ==1:
	# Fill this with what we can eventually
	fill = str('-1 ')*12
        fillline = str(jcount)+ ' '+ str(N_Showers)  + ' ' + mc_string+ ' '+dep_string+' '+ fill.rsplit(' ',1)[0] + '\n'  
	lookup.writelines(fillline)
	lookup.close()
	return
 
    for a in range(len(holder)):
        shrA = axfi.weightshowerfit(dataset,holder[a])
        EA = selpz.corrected_energy(dataset,holder[a])
        ChargeA = selpz.totcharge(dataset,holder[a])
        N_sptA = len(holder[a])

        for b in range(a+1,len(holder)):
            shrB = axfi.weightshowerfit(dataset,holder[b])
            EB = selpz.corrected_energy(dataset,holder[b])
            ChargeB = selpz.totcharge(dataset,holder[b])
            N_sptB = len(holder[b])
            vertex = selpz.findvtx(shrA,shrB)
            IP = selpz.findIP(shrA,shrB)

            SP_a = selpz.findRoughShowerStart(dataset,holder[a],vertex)
            radL_a = selpz.findconversionlength(vertex,SP_a)
            SP_b = selpz.findRoughShowerStart(dataset,holder[b],vertex)
            radL_b = selpz.findconversionlength(vertex,SP_b)
            angle = selpz.openingangle(shrA,shrB,vertex)


	    #### THIS IS UGLY
       #     if IP>20:
      #          continue
     #       if angle<0.2:
    #            continue
   #         if angle>2.94:
  #              continue
 #           if radL_a>50 and radL_b>50:
#                continue


	    

            selection_line = str(N_sptA) + ' ' + str(ChargeA) + ' '+ str(N_sptB) + ' '+ str(ChargeB) + ' '+ str(vertex[0]) + ' '+ str(vertex[1]) + ' '+ str(vertex[2]) + ' '+ str(IP) + ' '+ str(radL_a) + ' '+ str(radL_b) + ' '+ str(angle)
	    
	    # Distance to vertex  This can be better... ugly
	    vtx_diff = pow( pow(vertex[0]-mc_dl[0][0][0],2) + pow(vertex[1]-mc_dl[0][0][1],2)+ pow(vertex[2]-mc_dl[0][0][2],2), 0.5)
           # mcfullrecoline = str(jcount)+ ' '+ str(N_Showers)  + ' ' + mc_string+ ' '+str(vtx_diff)+' '+ selection_line + '\n'  
            mcfullrecoline = str(jcount)+ ' '+ str(N_Showers)  + ' ' + mc_string+' '+ dep_string+ ' '+str(vtx_diff)+' '+ selection_line + '\n'  

            #mcfullrecoline = str(jcount)+ ' '+ str(N_Showers)  + ' ' + mc_string+ ' '+str(vtx_diff)+' '+ selection_line + '\n'  
	    lookup.writelines(mcfullrecoline)
    lookup.close()
    return 










###########################################################################################################################
#########################     non counted utility stype fillers      ######################################################
###########################################################################################################################


#==========================================================================================================
def F_pi0_vtx(mc_dl):
    vtx_x = mc_dl[0][0][0]
    vtx_y = mc_dl[0][0][1]
    vtx_z = mc_dl[0][0][2]
    ret_string = str(vtx_x)+ ' ' +  str(vtx_y)+ ' '+ str(vtx_z)
    return ret_string 
#==========================================================================================================
def F_mc_pi0_fracs(f,dataset,Charge_thresh , showeridx_holder, trackidx_holder, mc_dl):
    #1 Total MC spts Charge 
    totmc = dh.Get_Total_MC_Charge(f)

    #2 Total Reco spts Charge
    totreco = dh.Get_Total_Reco_Charge(f)

    #3 Total Reco_Thres spts Charge
    totreco_thresh = dh.Get_Total_Thresh_Charge(f,Charge_thresh)

    #4 Total Shower spts Charge
    #tot_shower = dh.Get_Total_Object_Charge(dataset,llshoweridx_holder)
    tot_shower = dh.Get_Total_Object_Charge(dataset,showeridx_holder)

    #5 Total Track spts Charge
    tot_track = dh.Get_Total_Object_Charge(dataset,trackidx_holder)


    mcfullrecoline = str(totmc)+' ' +str(totreco)+' ' +str(totreco_thresh) + ' ' +str(tot_shower)+ ' ' + str(tot_track)+' ' + str(totreco/totmc)+' ' + str(totreco_thresh/totreco)+' ' + str(tot_shower/totreco_thresh)+' ' + str(tot_track/totreco_thresh)+' ' + str(tot_shower/totreco)+' ' + str(tot_track/totreco)
    return mcfullrecoline


