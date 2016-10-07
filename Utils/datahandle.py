import numpy as np
import ROOT


#Need to define detector volumes

def Unique(infile): 
    #returns all unique
    b = np.ascontiguousarray(infile).view(np.dtype((np.void, infile.dtype.itemsize * infile.shape[1])))
    _, idx = np.unique(b, return_index=True)
    return infile[idx]

def DuplicateIDX(lst,value):
    #returns a list of duplicated 
    return [i for i, x in enumerate(lst) if x == value]

def FileIsGood(infile):
    fi = ROOT.TFile('{}'.format(infile))
    rt = fi.Get("T_rec")
    if rt.GetEntries()==0:
	return False
    return True

def ConvertWC(infile):
    #Bring in the file 
    f = ROOT.TFile("{}".format(infile))
    t = f.Get("T_rec_charge")
    # Parse into an array 
    sptarray = []
    for entry in t:
	if entry.q!=0.0: 
	    sptarray.append([entry.x,entry.y,entry.z,entry.q])
    #make this an ndarray    
    spta = np.asanyarray(sptarray)
    #Make sure all points are unique
    cleanspta = Unique(spta)
    return cleanspta

def ConvertWC_InTPC(infile):
    #Bring in the file 
    f = ROOT.TFile("{}".format(infile))
    t = f.Get("T_rec_charge")
    # Parse into an array 
    sptarray = []
    for entry in t:
	if entry.q!=0.0 and entry.x>0 and entry.x<256: 
	    sptarray.append([entry.x,entry.y,entry.z,entry.q])
    #make this an ndarray    
    spta = np.asanyarray(sptarray)
    cleanspta = Unique(spta)
    return cleanspta

def ConvertWC_InRange(infile,xlo,xhi,ylo,yhi,zlo,zhi):
    #Bring in the file 
    f = ROOT.TFile("{}".format(infile))
    t = f.Get("T_rec_charge")
    # Parse into an array 
    sptarray = []
    for entry in t:
	if entry.q!=0.0 and entry.x>xlo and entry.x<xhi and entry.y>ylo and entry.y<yhi and entry.z>zlo and entry.z<zhi: 
	    sptarray.append([entry.x,entry.y,entry.z,entry.q])
    #make this an ndarray    
    spta = np.asanyarray(sptarray)
    cleanspta = Unique(spta)
    return cleanspta
 
def ConvertWCMC(infile):
    #Bring in the file 
    f = ROOT.TFile("{}".format(infile))
    t = f.Get("T_true")
    # Parse into an array 
    sptarray = []
    for entry in t:
	sptarray.append([entry.x,entry.y,entry.z,entry.q])
    #make this an ndarray    
    spta = np.asanyarray(sptarray)
    return spta

def ConvertWC_points(infile):
    #Bring in the file 
    f = ROOT.TFile("{}".format(infile))
    t = f.Get("T_rec_charge")
    # Parse into an array 
    sptarray = []
    for entry in t:
	if entry.q!=0.0: 
	    sptarray.append([entry.x,entry.y,entry.z])
    #make this an ndarray    
    spta = np.asanyarray(sptarray)
    return spta


