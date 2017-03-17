import numpy as np
import Utils.datahandle as dh

def rebase_spts(f,dataset,showeridx_holder, ROI,roi_buffer, Charge_Thresh):
    # Loop over the showeridx_ holder to find farthesst away point
    max_dist_sq = 0.0
    # we just look at the first one... .this hsould be a loop eventually
    roi_vtx = ROI[0][0]
    for h in range(len(showeridx_holder)):
	if h not in ROI[0][1:]:
	    continue
	for idx in showeridx_holder[h]:
	    tdist = pow(dataset[idx][0]-roi_vtx[0],2) +pow(dataset[idx][1]-roi_vtx[1],2) + pow(dataset[idx][2]-roi_vtx[2],2)
	    if tdist>max_dist_sq:
		print 'this is the tdist'
		print tdist
		max_dist_sq = tdist
    #Use the max value at the radius for the ROI
    #now loop over the rebase points
    
    
    print ' what is max_dist'
    print max_dist_sq
    rebase = dh.ConvertWC_InTPC_thresh('{}'.format(f),Charge_Thresh)
    print ' are we getting the rebase length' 
    len( rebase)

    roi_idx = []
    for i in range(len(rebase)):
	rebase_test_dist = pow(rebase[i][0]-roi_vtx[0],2) +pow(rebase[i][1]-roi_vtx[1],2) + pow(rebase[i][2]-roi_vtx[2],2)
	if rebase_test_dist<max_dist_sq+roi_buffer:
	    # keep this 
	    roi_idx.append(i)

    print ' ROI idx length' 
    len( roi_idx)
    # make the return rebase_dataset
    rebase_dataset = [ rebase[x] for x in roi_idx]

    return rebase_dataset
