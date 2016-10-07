import math as math
import ROOT

def piz_mc_info(infile):
    #Returns a large string of of MC truth info which is specific and useful for pi0s
    f = ROOT.TFile("{}".format(infile))
    t = f.Get("TMC")
    for en in t:
	#Is this a non-dalitz
	if en.mc_pdg[1]!=22 or en.mc_pdg[2]!=22:
	    # Write out a bail list to return
	    bail = [-1 for x in xrange(0,23)]
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
