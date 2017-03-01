import numpy as np 
import Geo_Utils.axisfit as axfi
import SParams.selpizero as selpz



def CorrelatedObjects( dataset,idx_holder,labels):
    keptpairs = []
    if len(idx_holder) ==0:
	return keptpairs
    if len(idx_holder)==1:
	keptpairs = idx_holder
	return keptpairs

    for a in range(len(idx_holder)):
        shrA = axfi.weightshowerfit(dataset,idx_holder[a])
        EA = selpz.corrected_energy(dataset,idx_holder[a])
        ChargeA = selpz.totcharge(dataset,idx_holder[a])
        N_sptA = len(idx_holder[a])
        #print ' new pair '
        for b in range(a+1, len(idx_holder)):
            shrB = axfi.weightshowerfit(dataset,idx_holder[b])
            EB = selpz.corrected_energy(dataset,idx_holder[b])
            ChargeB = selpz.totcharge(dataset,idx_holder[b])
            N_sptB = len(idx_holder[b])
            vertex = selpz.findvtx(shrA,shrB)
            IP = selpz.findIP(shrA,shrB)
        #    print 'VERTEX ', str(vertex)
         #   print 'IP ', str(IP)
            SP_a = selpz.findRoughShowerStart(dataset,idx_holder[a],vertex)
            #print 'SP A : ', str(SP_a)
            radL_a = selpz.findconversionlength(vertex,SP_a)
            SP_b = selpz.findRoughShowerStart(dataset,idx_holder[b],vertex)
            #print 'SP B : ', str(SP_b)
            radL_b = selpz.findconversionlength(vertex,SP_b)
         #   print 'radL A', str(radL_a)
         #   print 'radL B', str(radL_b)
            angle = selpz.openingangle(shrA,shrB,vertex)
	    # If we pass the cuts.... keep this pair
	    # crap cut for fun
	    if IP>20: 
	        continue
	    if angle<0.3: 
	        continue
	    keptpairs.append(a)
	    keptpairs.append(b)

    # Clean up kept pairs
    retpairs = list(set(keptpairs))
    # make the output holder
    ret_holder = [ idx_holder[x] for x in retpairs]
    return ret_holder


