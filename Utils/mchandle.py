import math as math
#import ROOT
import libPyROOT as ROOT


xlo = 0
xhi = 256.35
ylo = -116.9
yhi = 116.9
zlo = 0
zhi = 1036.8


def mc_neutron_induced_contained(f):
    tf = ROOT.TFile("{}".format(f))
    tree = tf.Get("TMC")

    # Files to be run since we only want to do certain  
    Signal_event = []
#    id_counter = 0

    _x_particle = []
    _y_particle = []
    _z_particle = []
    _Ex_particle = []
    _Ey_particle = []
    _Ez_particle = []
    _pp_particle = []
    pi0_4mom = []
    daughter_4mom = []

    for i in tree:

        id_list = [x for x in i.mc_id]
        mother_list = [ x for x in i.mc_mother]
        pdg_list = [ x for x in i.mc_pdg]
        Sxyzt_list = [[x] for x in i.mc_startXYZT]
        Exyzt_list = [[x] for x in i.mc_endXYZT]
        Sxyzp_list = [[x] for x in i.mc_startMomentum]
        process_list = [ x for x in i.mc_process]
        # Sort out the xyztlist

        for itr in range(len(Sxyzt_list)):
            modu = itr%4
            if modu ==0:
                _x_particle.append(str(Sxyzt_list[itr]).split('[')[1].split(']')[0])
                _Ex_particle.append(str(Exyzt_list[itr]).split('[')[1].split(']')[0])
            if modu ==1:
                _y_particle.append(str(Sxyzt_list[itr]).split('[')[1].split(']')[0])
                _Ey_particle.append(str(Exyzt_list[itr]).split('[')[1].split(']')[0])
            if modu ==2:
                _z_particle.append(str(Sxyzt_list[itr]).split('[')[1].split(']')[0])
                _Ez_particle.append(str(Exyzt_list[itr]).split('[')[1].split(']')[0])
            if modu ==3:
                _pp_particle.append(str(Sxyzp_list[itr]).split('[')[1].split(']')[0])

        pi0_mothers=[]
        pi0_partid=[]
        for pdg in range(len(pdg_list)):
            if pdg_list[pdg]==111:
                #is the pi0 is not inside the TPC
                if float(_x_particle[pdg])<xlo or float(_x_particle[pdg])>xhi or float(_y_particle[pdg])<ylo or float(_y_particle[pdg])>yhi or float(_z_particle[pdg])<zlo or float(_z_particle[pdg])>zhi:
                    print' pi0 is outside '
                    continue
                pi0_id = id_list[pdg]
                pi0_4mom.append(float(_x_particle[pdg]))
                pi0_4mom.append(float(_y_particle[pdg]))
                pi0_4mom.append(float(_z_particle[pdg]))
                pi0_4mom.append(float(_pp_particle[pdg]))
                motherindex = id_list.index(mother_list[pdg])
                pi0_mothers.append(pdg_list[id_list.index(mother_list[pdg])])
                pi0_partid.append(pi0_id)

        # If there is not only one pi0 in the TPC continue
        if len(pi0_mothers)!=1 or len(pi0_mothers)==0:
            return False 

        # If the pi0 mom is not a neutron
        if pi0_mothers[0]!=2112:# is this a neutron? 
            return False


        for pdg in range(len(pdg_list)):
            if pdg_list[pdg]==22 or pdg_list[pdg]==-11 or pdg_list[pdg]==11:
                if mother_list[pdg]==0:
                    continue
                try:
                    mom = pdg_list[id_list.index(mother_list[pdg])]
                    if mom==111:
                        if pi0_partid[0] != mother_list[pdg]:
                            continue
                        if float(_Ex_particle[pdg])<xlo or float(_Ex_particle[pdg])>xhi or float(_Ey_particle[pdg])<ylo or float(_Ey_particle[pdg])>yhi or float(_Ez_particle[pdg])<zlo or float(_Ez_particle[pdg])>zhi:
                            print ' this is a bad daughter'
			    return False 
                except:
                    continue

    return True







def mc_neutron_induced_OBJ( f ):
    tf = ROOT.TFile("{}".format(f))
    tree = tf.Get("TMC")

    # Files to be run since we only want to do certain  
    Signal_event = []

    _x_particle = []
    _y_particle = []
    _z_particle = []
    _Ex_particle = []
    _Ey_particle = []
    _Ez_particle = []
    _pp_particle = []
    pi0_4mom = []
    daughter_4mom = []

    for i in tree:

        id_list = [x for x in i.mc_id]
        mother_list = [ x for x in i.mc_mother]
        pdg_list = [ x for x in i.mc_pdg]
        Sxyzt_list = [[x] for x in i.mc_startXYZT]
        Exyzt_list = [[x] for x in i.mc_endXYZT]
        Sxyzp_list = [[x] for x in i.mc_startMomentum]
        process_list = [ x for x in i.mc_process]
        # Sort out the xyztlist

        for itr in range(len(Sxyzt_list)):
            modu = itr%4
            if modu ==0:
                _x_particle.append(str(Sxyzt_list[itr]).split('[')[1].split(']')[0])
                _Ex_particle.append(str(Exyzt_list[itr]).split('[')[1].split(']')[0])
            if modu ==1:
                _y_particle.append(str(Sxyzt_list[itr]).split('[')[1].split(']')[0])
                _Ey_particle.append(str(Exyzt_list[itr]).split('[')[1].split(']')[0])
            if modu ==2:
                _z_particle.append(str(Sxyzt_list[itr]).split('[')[1].split(']')[0])
                _Ez_particle.append(str(Exyzt_list[itr]).split('[')[1].split(']')[0])
            if modu ==3:
                _pp_particle.append(str(Sxyzp_list[itr]).split('[')[1].split(']')[0])

        pi0_mothers=[]
        pi0_partid=[]
        for pdg in range(len(pdg_list)):
            if pdg_list[pdg]==111:
                #is the pi0 is not inside the TPC
                if float(_x_particle[pdg])<xlo or float(_x_particle[pdg])>xhi or float(_y_particle[pdg])<ylo or float(_y_particle[pdg])>yhi or float(_z_particle[pdg])<zlo or float(_z_particle[pdg])>zhi:
                    #print' pi0 is outside '
		    #print _x_particle[pdg]
		    #print _y_particle[pdg]
		    #print _z_particle[pdg]	
                    continue
                pi0_id = id_list[pdg]
                pi0_4mom.append(float(_x_particle[pdg]))
                pi0_4mom.append(float(_y_particle[pdg]))
                pi0_4mom.append(float(_z_particle[pdg]))
                pi0_4mom.append(float(_pp_particle[pdg]))
		try:
                    motherindex = id_list.index(mother_list[pdg])
		except ValueError:
                    for pdg in range(len(pdg_list)):
            	        if pdg_list[pdg]==22 or pdg_list[pdg]==-11 or pdg_list[pdg]==11:
                            try:
                    	        mom = pdg_list[id_list.index(mother_list[pdg])]
                                if mom!=111:
				    continue
			    except :
				continue
		            tdaughter_4mom = []
                            tdaughter_4mom.append(float(_Ex_particle[pdg]))
                            tdaughter_4mom.append(float(_Ey_particle[pdg]))
                            tdaughter_4mom.append(float(_Ez_particle[pdg]))
                            tdaughter_4mom.append(float(_pp_particle[pdg]))
                            daughter_4mom.append(tdaughter_4mom)
		    return pi0_4mom, daughter_4mom
		
                pi0_mothers.append(pdg_list[id_list.index(mother_list[pdg])])
                pi0_partid.append(pi0_id)

        # If there is not only one pi0 in the TPC continue
        if len(pi0_mothers)!=1:
            return False 

        # If the pi0 mom is not a neutron
        if pi0_mothers[0]!=2112:# is this a neutron? 
            return False


        for pdg in range(len(pdg_list)):
            if pdg_list[pdg]==22 or pdg_list[pdg]==-11 or pdg_list[pdg]==11:
                if mother_list[pdg]==0:
                    continue
                try:
                    mom = pdg_list[id_list.index(mother_list[pdg])]
                    if mom==111:
                        if pi0_partid[0] != mother_list[pdg]:
                            continue
                        #print ' this is the mother index list' , pi0_partid[0]
                        #print ' this is the id current list ' , str(mother_list[pdg])
                        if float(_Ex_particle[pdg])<xlo or float(_Ex_particle[pdg])>xhi or float(_Ey_particle[pdg])<ylo or float(_Ey_particle[pdg])>yhi or float(_Ez_particle[pdg])<zlo or float(_Ez_particle[pdg])>zhi:
			    continue
                        tdaughter_4mom = []
                        tdaughter_4mom.append(float(_Ex_particle[pdg]))
                        tdaughter_4mom.append(float(_Ey_particle[pdg]))
                        tdaughter_4mom.append(float(_Ez_particle[pdg]))
                        tdaughter_4mom.append(float(_pp_particle[pdg]))
                        daughter_4mom.append(tdaughter_4mom)
                except:
                    continue

    print 'From the MC Filter We are returning True'
    return pi0_4mom, daughter_4mom

















def oldmc_neutron_induced_OBJ( f ):
    tf = ROOT.TFile("{}".format(f))
    mctree = tf.Get("TMC")
    _x_particle = []
    _y_particle = []
    _z_particle = []
    _Ex_particle = []
    _Ey_particle = []
    _Ez_particle = []
    _pp_particle = []
    pi0_4mom = []
    daughter_4mom = []

    for i in mctree:
        id_list = [x for x in i.mc_id]
        mother_list = [ x for x in i.mc_mother]
        pdg_list = [ x for x in i.mc_pdg]
        Sxyzt_list = [[x] for x in i.mc_startXYZT]
        Exyzt_list = [[x] for x in i.mc_endXYZT]
        Sxyzp_list = [[x] for x in i.mc_startMomentum]

        # Sort out the xyztlist
        for itr in range(len(Sxyzt_list)):
            modu = itr%4
            if modu ==0:
                _x_particle.append(str(Sxyzt_list[itr]).split('[')[1].split(']')[0])
                _Ex_particle.append(str(Exyzt_list[itr]).split('[')[1].split(']')[0])
            if modu ==1:
                _y_particle.append(str(Sxyzt_list[itr]).split('[')[1].split(']')[0])
                _Ey_particle.append(str(Exyzt_list[itr]).split('[')[1].split(']')[0])
            if modu ==2:
                _z_particle.append(str(Sxyzt_list[itr]).split('[')[1].split(']')[0])
                _Ez_particle.append(str(Exyzt_list[itr]).split('[')[1].split(']')[0])
            if modu ==3:
                _pp_particle.append(str(Sxyzp_list[itr]).split('[')[1].split(']')[0])

        pi0_id = -1
        # ^^ This is a little hacked
        # This should be unique for neutron photon
        for pdg in range(len(pdg_list)):
            if pdg_list[pdg]==111:
                pi0_id = id_list[pdg]
                pi0_4mom.append(float(_x_particle[pdg]))
                pi0_4mom.append(float(_y_particle[pdg]))
                pi0_4mom.append(float(_z_particle[pdg]))
                pi0_4mom.append(float(_pp_particle[pdg]))

        for pdg in range(len(pdg_list)):
            if pdg_list[pdg]==22 or pdg_list[pdg]==-11 or pdg_list[pdg]==11:
                if mother_list[pdg]==0:
                    continue
                try:
                    mom = pdg_list[id_list.index(mother_list[pdg])]
                    if mom==111:
                        tdaughter_4mom = []
                        tdaughter_4mom.append(float(_Ex_particle[pdg]))
                        tdaughter_4mom.append(float(_Ey_particle[pdg]))
                        tdaughter_4mom.append(float(_Ez_particle[pdg]))
                        tdaughter_4mom.append(float(_pp_particle[pdg]))
                        daughter_4mom.append(tdaughter_4mom)
                except:
                    continue

    return pi0_4mom, daughter_4mom




def mc_Obj_points(obj_list):
    #print obj_list
    pi0_xyz = obj_list[0]
    gamma_xyz = obj_list[1]

    # The first entry in the list is a 4 position of the pi0
    space = 20*20*20 +  20* 3*len(gamma_xyz)
    dataset = [None for x in range(space)]
    #dataset = []
    mclab = 0 # This is hard code magic for coloring in the bee viewer
    box_size = 1
    density = 5
    # lower number is higher density
    # Fix this later on# lower number is higher density


    counter=0
    for i in range(0,box_size*100,density):
        for j in range(0,box_size*100,density):
	    for k in range(0,box_size*100,density):
		dataset[counter] = [pi0_xyz[0]-box_size +2.*box_size*k/100.,pi0_xyz[1]-box_size+2.*box_size*j/100.,pi0_xyz[2]-box_size+2.*box_size*i/100.]
		counter+=1
		#dataset.append([pi0_xyz[0]-box_size +2.*box_size*k/100.,pi0_xyz[1]-box_size+2.*box_size*j/100.,pi0_xyz[2]-box_size+2.*box_size*i/100.])

    # Draw a cross for the photons
    for a in range(len(gamma_xyz)):
        for i in range(0,box_size*100,density):
	    dataset[counter] = [gamma_xyz[a][0]-box_size +2.*box_size*i/100.,gamma_xyz[a][1],gamma_xyz[a][2]]# wali the X
	    counter+=1
	    dataset[counter] = [gamma_xyz[a][0],gamma_xyz[a][1]-box_size +2.*box_size*i/100.,gamma_xyz[a][2]]# wali the X
	    counter+=1
	    dataset[counter] = [gamma_xyz[a][0],gamma_xyz[a][1],gamma_xyz[a][2]-box_size +2.*box_size*i/100.]# wali the X
	    counter+=1

    # Draw a line between the pi0vtx and daughters

    # We are going to fill out a box around the region
    labels = [0 for a in range(len(dataset))]
    return dataset , labels
    
    


def mc_roi( f):
    tf = ROOT.TFile("{}".format(f))
    mctree = tf.Get("TMC")
    _x_particle = []
    _y_particle = []
    _z_particle = []
    _t_particle = []
    _px_particle = []
    _py_particle = []
    _pz_particle = []
    _pp_particle = []
    # Make the lists for things to look though
    for i in mctree:
	id_list = [x for x in i.mc_id]
	mother_list = [ x for x in i.mc_mother]
	pdg_list = [ x for x in i.mc_pdg]
	process_list = [ x for x in i.mc_process]
	xyzt_list = [[x] for x in i.mc_startXYZT]
	xyzp_list = [[x] for x in i.mc_startMomentum]
        # Sort out the xyztlist
        for itr in range(len(xyzt_list)):
            modu = itr%4
            if modu ==0:
                _x_particle.append(str(xyzt_list[itr]).split('[')[1].split(']')[0])
                _px_particle.append(str(xyzp_list[itr]).split('[')[1].split(']')[0])
            if modu ==1:
                _y_particle.append(str(xyzt_list[itr]).split('[')[1].split(']')[0])   
                _py_particle.append(str(xyzp_list[itr]).split('[')[1].split(']')[0])   
            if modu ==2:
                _z_particle.append(str(xyzt_list[itr]).split('[')[1].split(']')[0])
                _pz_particle.append(str(xyzp_list[itr]).split('[')[1].split(']')[0])   
            if modu ==3:
                _t_particle.append(str(xyzt_list[itr]).split('[')[1].split(']')[0])
                _pp_particle.append(str(xyzp_list[itr]).split('[')[1].split(']')[0])   
 
    # Get the pi0 list
    pi0_itr = []    
    pi0_mother_itr = []    
 
    for itr in range(len(pdg_list)):
        if pdg_list[itr]==111:
            pi0_itr.append(itr)
            pi0_mother_itr =  mother_list[itr]

    # Make the string It will be a vector of strings 
    ret_string_vec = [] 
    for a in range(len(pi0_itr)):
        N_pi0 = str(len(pi0_itr))
	ID_pi0 = str(a)
	xyzt_string = str(_x_particle[pi0_itr[a]])+' ' +str(_y_particle[pi0_itr[a]])+' '+str(_z_particle[pi0_itr[a]])+' '+str(_t_particle[pi0_itr[a]])
	xyzp_string = str(_px_particle[pi0_itr[a]])+' ' +str(_py_particle[pi0_itr[a]])+' '+str(_pz_particle[pi0_itr[a]])+' '+str(_pp_particle[pi0_itr[a]])
 	fstr = N_pi0+' ' + ID_pi0+' '+xyzt_string +' '+xyzp_string
	ret_string_vec.append(fstr)
    return ret_string_vec

def piz_mc_info(infile):
    #Returns a large string of of MC truth info which is specific and useful for pi0s
    f = ROOT.TFile("{}".format(infile))
    t = f.Get("TMC")
    for en in t:
	#Is this a non-dalitz
	if en.mc_pdg[1]!=22 or en.mc_pdg[2]!=22:
	    # Write out a bail list to return
	    bail = [-1 for x in xrange(0,25)]
            bails = str(bail).split('[')[1].rsplit(']')[0].replace(',','')
	    return bails
	vtx_pi_x = en.mc_startXYZT[0]
	vtx_pi_y = en.mc_startXYZT[1]
	vtx_pi_z = en.mc_startXYZT[2]
	#normalized momentum
	p_pi_x = en.mc_startMomentum[0]/en.mc_startMomentum[3]
	p_pi_y = en.mc_startMomentum[1]/en.mc_startMomentum[3]
	p_pi_z = en.mc_startMomentum[2]/en.mc_startMomentum[3]
	p_pi_mag = en.mc_startMomentum[3]

	# Now do the first gamma
	#The showerconversion point is supposed to be the end of the gamma
	vtx_gamma_x = en.mc_endXYZT[4]
	vtx_gamma_y = en.mc_endXYZT[5]
	vtx_gamma_z = en.mc_endXYZT[6]
	p_gamma_x = en.mc_startMomentum[4]/en.mc_startMomentum[7]
	p_gamma_y = en.mc_startMomentum[5]/en.mc_startMomentum[7]
	p_gamma_z = en.mc_startMomentum[6]/en.mc_startMomentum[7]
	p_gamma_mag = en.mc_startMomentum[7]
	# Now do the second gamma
	#The showerconversion point is supposed to be the end of the gamma
	vtx_gamma_2_x = en.mc_endXYZT[8]
	vtx_gamma_2_y = en.mc_endXYZT[9]
	vtx_gamma_2_z = en.mc_endXYZT[10]
	p_gamma_2_x = en.mc_startMomentum[8]/en.mc_startMomentum[11]
	p_gamma_2_y = en.mc_startMomentum[9]/en.mc_startMomentum[11]
	p_gamma_2_z = en.mc_startMomentum[10]/en.mc_startMomentum[11]
	p_gamma_2_mag = en.mc_startMomentum[11]

	# now do relationship of showers. 
	print p_gamma_x
	print p_gamma_y
	print p_gamma_z
	print p_gamma_2_x
	print p_gamma_2_y
	print p_gamma_2_z
	print p_gamma_mag
	print p_gamma_2_mag
	print p_gamma_mag* p_gamma_2_mag
	print (p_gamma_x*p_gamma_2_x+p_gamma_y*p_gamma_2_y+p_gamma_z*p_gamma_2_z)  
	#print (p_gamma_x*p_gamma_2_x+p_gamma_y*p_gamma_2_y+p_gamma_z*p_gamma_2_z) / (p_gamma_mag*p_gamma_2_mag)
	gamma_angle = math.acos((p_gamma_x*p_gamma_2_x+p_gamma_y*p_gamma_2_y+p_gamma_z*p_gamma_2_z))

	# Form the return string
	dalitz = 0
	ret = str(dalitz)+' '+str(vtx_pi_x)+' '+str(vtx_pi_y)+' '+str(vtx_pi_z)+' '+str(p_pi_x)+' '+str(p_pi_y)+' '+str(p_pi_z)+' '+str(p_pi_mag)+' '+str(vtx_gamma_x)+' '+str(vtx_gamma_y)+' '+str(vtx_gamma_z)+' '+str(p_gamma_x)+' '+str(p_gamma_y)+' '+str(p_gamma_z)+' '+str(p_gamma_mag)+' '+str(vtx_gamma_2_x)+' '+str(vtx_gamma_2_y)+' '+str(vtx_gamma_2_z)+' '+str(p_gamma_2_x)+' '+str(p_gamma_2_y)+' '+str(p_gamma_2_z)+' '+str(p_gamma_2_mag)+' '+str(gamma_angle) + ' '+ str(1-math.cos(gamma_angle))
	
	return ret 

	


def gamma_mc_info(infile):
    #Returns a large string of of MC truth info which is specific and useful for pi0s
    f = ROOT.TFile("{}".format(infile))
    t = f.Get("TMC")
    # the photon should be the first
    for en in t:
        vtx_gamma_x = en.mc_endXYZT[0]
        vtx_gamma_y = en.mc_endXYZT[1]
        vtx_gamma_z = en.mc_endXYZT[2]
        p_gamma_x = en.mc_startMomentum[0]/en.mc_startMomentum[3]
        p_gamma_y = en.mc_startMomentum[1]/en.mc_startMomentum[3]
        p_gamma_z = en.mc_startMomentum[2]/en.mc_startMomentum[3]
        p_gamma_mag = en.mc_startMomentum[3]
        ret = str(vtx_gamma_x)+' '+str(vtx_gamma_y)+' '+str(vtx_gamma_z)+' '+str(p_gamma_x)+' '+str(p_gamma_y)+' '+str(p_gamma_z)+' '+str(p_gamma_mag)
        return ret

def gamma_mc_dep(infile):
    #Returns a large string of of MC truth info which is specific and useful for pi0s
    f = ROOT.TFile("{}".format(infile))
    t = f.Get("T_true")
    # the photon should be the first
    qdep = 0.0
    for en in t:
        qdep +=en.q
    ret = str(qdep)
    return ret
