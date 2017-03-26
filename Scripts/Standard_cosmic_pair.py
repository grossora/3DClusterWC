import os , sys
import pandas as pd
import numpy as np
import seaborn as sns
import pylab as plt
import math as math
import matplotlib.mlab as mlab
from scipy.stats import norm
import collections as col
from itertools import combinations
import seaborn as sns
#sns.set(style="white", color_codes=True ,{'' : True})
sns.set_style("white", {"axes.grid": True})
from matplotlib import colors
from matplotlib.colors import LogNorm

# Crap hack since path is messed up
sys.path.insert(0, "../")
import Geo_Utils.detector as detector 

# Save or show items? 
#_save = True
_save = False 
_show = True
#_show = False 

fig_dir = os.getcwd()+'/Figs/Standard_cosmicpi0'
if not os.path.isdir(fig_dir):
    print 'makeing this for you'
    os.makedirs(fig_dir)

#bring in the data into pandas 
if(len(sys.argv)==1):
    pdf = pd.read_csv('../Out_text/lhull_Ana_pair_Cosmic_pair.txt', sep=" ", header = None)
else:
    pdf = pd.read_csv('{}'.format(sys.argv[1]), sep=" ", header = None)

#Define the columns
pdf.columns = ['jcount','N_objects','dalitz','vtx_pi_x','vtx_pi_y','vtx_pi_z','p_pi_x','p_pi_y','p_pi_z','p_pi_mag','vtx_gamma_x','vtx_gamma_y','vtx_gamma_z','p_gamma_x','p_gamma_y','p_gamma_z','p_gamma_mag','vtx_gamma_2_x','vtx_gamma_2_y','vtx_gamma_2_z','p_gamma_2_x','p_gamma_2_y','p_gamma_2_z','p_gamma_2_mag','gamma_angle','OMC_gamma_angle', 'tot_mc_q','tot_reco_q','tot_thresh_q', 'tot_shower_q', 'tot_track_q', 'frac_reco_per_mc', 'frac_thresh_per_reco','frac_shower_per_thresh','frac_track_per_thresh','frac_shower_per_reco' ,'frac_track_per_reco', 'vtx_diff','N_Aspts','showerA_q','N_Bspts','showerB_q','vtx_x','vtx_y','vtx_z','IP','RadL_A','RadL_B','angle']
 
# Very first 'cut' ... which will be needed to be put into the main code
xlo = detector.GetX_Bounds()[0]
xhi = detector.GetX_Bounds()[1]
ylo = detector.GetY_Bounds()[0]
yhi = detector.GetY_Bounds()[1]
zlo = detector.GetZ_Bounds()[0]
zhi = detector.GetZ_Bounds()[1]
df = pdf[ (pdf.vtx_x>xlo) & (pdf.vtx_x<xhi) &(pdf.vtx_y> ylo) & (pdf.vtx_y<yhi)&  (pdf.vtx_z>zlo) & (pdf.vtx_z<zhi)]


################################
# Have some standard plots
################################
# How many Shower Objects
################################
ev_df = df.groupby('jcount').first()
max_bin_ob = ev_df.N_objects.max()
plt.hist(ev_df.N_objects,range(0,max_bin_ob),facecolor = 'blue', alpha = 0.7)
plt.title('Number of Showers')
if _save:
    plt.savefig('{}/N_showers.png'.format(fig_dir))
if _show:
    plt.show()
plt.close()


################################
# How many Pairs 
################################
pair_df = df.groupby('jcount')
ppl = pair_df['jcount'].count().hist(bins=500 ,range=(0,500),facecolor = 'blue', alpha = 0.7)
plt.show()

# What range would we like to look at ? 

#Fiducial Area
fxlo = xlo
fxhi = xhi
fylo = ylo
fyhi = yhi
#fzlo = 0 
#fzlo = 400 
fzlo = zhi/2
fzhi = zhi


# First make the MC Cut to see how many events we have in the region
truth_events = pdf[ (pdf.vtx_pi_x>fxlo) & (pdf.vtx_pi_x<fxhi) &(pdf.vtx_pi_y> fylo) & (pdf.vtx_pi_y<fyhi)&  (pdf.vtx_pi_z>fzlo) & (pdf.vtx_pi_z<fzhi)]
# How many events are in this region
Total_TruthEvents = len(truth_events.groupby('jcount').first().index)
print ' This is the totoal MC events in the fiducial area ' , str(Total_TruthEvents)


# This is already going to be true
fid_events = df[ (df.vtx_x>fxlo) & (df.vtx_x<fxhi) &(df.vtx_y> fylo) & (df.vtx_y<fyhi)&  (df.vtx_z>fzlo) & (df.vtx_z<fzhi)]
Total_fidEvents = len(fid_events.groupby('jcount').first().index)
Total_fidcandidate = len(fid_events.index)
print ' This is the total reco events in the fiducial area' , str(Total_fidEvents)
print ' This is the total reco vertex candidate in the fiducial area' , str(Total_fidcandidate)

print 'Now look at the breakout of the reco events in the fiducial volume'  
print '**** Remember this is just events that reco in the vertex... not pairs'  
print '**** Basically this is the best we can do with selection'  


# break apart the fid_events by truth 
# Inside
fid_events_Truein = fid_events[ (fid_events.vtx_pi_x>fxlo) & (fid_events.vtx_pi_x<fxhi) &(fid_events.vtx_pi_y> fylo) & (fid_events.vtx_pi_y<fyhi)&  (fid_events.vtx_pi_z>fzlo) & (fid_events.vtx_pi_z<fzhi)]
# outside
fid_events_Trueout = fid_events[ (fid_events.vtx_pi_x<fxlo) | (fid_events.vtx_pi_x>fxhi) |(fid_events.vtx_pi_y< fylo) | (fid_events.vtx_pi_y>fyhi)|  (fid_events.vtx_pi_z<fzlo) | (fid_events.vtx_pi_z>fzhi)]



Total_fidEvents_truein = len(fid_events_Truein.groupby('jcount').first().index)
Total_fidcandidate_truein = len(fid_events_Truein.index)
Total_fidEvents_trueout = len(fid_events_Trueout.groupby('jcount').first().index)
Total_fidcandidate_trueout = len(fid_events_Trueout.index)

print ' This is the total reco events in the TRUE fiducial area' , str(Total_fidEvents_truein)
print ' This is the total reco vertex candidate in the TRUE fiducial area' , str(Total_fidcandidate_truein)
print ' This is the total reco events outside of the TRUE fiducial area' , str(Total_fidEvents_trueout)
print ' This is the total reco vertex candidate outside of  the TRUE fiducial area' , str(Total_fidcandidate_trueout)

print ' ^^^^^ These dont mean too much yet... just a sense of feel for things'



################################
################################
# Make the cuts... 
#infered from pi0 distributions
################################
################################
_cuts = (fid_events.IP<5) & (fid_events.RadL_A+fid_events.RadL_B<60) & (fid_events.RadL_A+fid_events.RadL_B>20) &(fid_events.angle<2.5)&(fid_events.angle>0.4)&(fid_events.showerA_q+fid_events.showerB_q>1700000) & (fid_events.showerA_q>250000) & (fid_events.showerB_q>250000)

fid_eventsCUT = fid_events[_cuts]
# Lets see what we are left with
Total_fidEventsCUT = len(fid_eventsCUT.groupby('jcount').first().index)
Total_fidcandidateCUT = len(fid_eventsCUT.index)
print ' now lets move on to some cuts... here are the cuts we are using' 
print ' This is the total reco events in the fiducial area' , str(Total_fidEventsCUT)
print ' This is the total reco vertex candidate in the fiducial area' , str(Total_fidcandidateCUT)

##### 
print 'Now I can quickly make a true efficiecy for the 1 pair case. This is baselike efficency and purity of the signal sample'

# Get the 1 pair case
df_fidEvents_singlepair = fid_eventsCUT.drop_duplicates(subset='jcount' , keep=False)
# Make frame for which are Truein
# Inside
df_singlepair_Truein = df_fidEvents_singlepair[ (df_fidEvents_singlepair.vtx_pi_x>fxlo) & (df_fidEvents_singlepair.vtx_pi_x<fxhi) &(df_fidEvents_singlepair.vtx_pi_y> fylo) & (df_fidEvents_singlepair.vtx_pi_y<fyhi)&  (df_fidEvents_singlepair.vtx_pi_z>fzlo) & (df_fidEvents_singlepair.vtx_pi_z<fzhi)]
# outside
df_singlepair_Trueout = df_fidEvents_singlepair[ (df_fidEvents_singlepair.vtx_pi_x<fxlo) | (df_fidEvents_singlepair.vtx_pi_x>fxhi) |(df_fidEvents_singlepair.vtx_pi_y< fylo) | (df_fidEvents_singlepair.vtx_pi_y>fyhi)|  (df_fidEvents_singlepair.vtx_pi_z<fzlo) | (df_fidEvents_singlepair.vtx_pi_z>fzhi)]

# Now we can make a direct eff and purity 
Total_singlepair = len(df_fidEvents_singlepair.index)
Total_singlepair_in = len(df_singlepair_Truein.index)
Total_singlepair_out = len(df_singlepair_Trueout.index)


# Efficiency is Total_Singlepair_in / Total_TruthEvents
print 'EFFICIENCY : ' , str(1.0* Total_singlepair_in/Total_TruthEvents)
# Efficiency is Total_Singlepair_in / Total_TruthEvents
print 'PURTIY : ' , str(1.0* Total_singlepair_in/Total_singlepair)
# Background
print 'Background : ' , str(1.0* Total_singlepair_out/Total_singlepair)


# Lets quickly look at vertex resolution

n, bins, patches = plt.hist(df_singlepair_Truein.vtx_diff,bins=25,range=(0,500),facecolor='blue',alpha = 0.8)
n, bins, patches = plt.hist(df_singlepair_Trueout.vtx_diff,bins=25,range=(0,500),facecolor='red',alpha = 0.8)
plt.title('Vertex Diff ')
plt.xlabel('Distance (cm)')
plt.show()


print ''
print ' what about good events aka vtx withing 25cm'
# Get the 1 pair case
# Inside
df_singlepair_Truein_good = df_fidEvents_singlepair[(df_fidEvents_singlepair.vtx_diff<25)& (df_fidEvents_singlepair.vtx_pi_x>fxlo) & (df_fidEvents_singlepair.vtx_pi_x<fxhi) &(df_fidEvents_singlepair.vtx_pi_y> fylo) & (df_fidEvents_singlepair.vtx_pi_y<fyhi)&  (df_fidEvents_singlepair.vtx_pi_z>fzlo) & (df_fidEvents_singlepair.vtx_pi_z<fzhi)]
df_singlepair_Truein_bad = df_fidEvents_singlepair[ (df_fidEvents_singlepair.vtx_diff>25)&(df_fidEvents_singlepair.vtx_pi_x>fxlo) & (df_fidEvents_singlepair.vtx_pi_x<fxhi) &(df_fidEvents_singlepair.vtx_pi_y> fylo) & (df_fidEvents_singlepair.vtx_pi_y<fyhi)&  (df_fidEvents_singlepair.vtx_pi_z>fzlo) & (df_fidEvents_singlepair.vtx_pi_z<fzhi)]

# Now we can make a direct eff and purity 
#Total_singlepair = len(df_fidEvents_singlepair.index)
#Total_singlepair_in = len(df_singlepair_Truein.index)
Total_singlepair_in_good = len(df_singlepair_Truein_good.index)
Total_singlepair_in_bad = len(df_singlepair_Truein_bad.index)


# Efficiency is Total_Singlepair_in / Total_TruthEvents
print 'EFFICIENCY for Good [ROI]  events : ' , str(1.0* Total_singlepair_in_good/Total_TruthEvents)
# Efficiency is Total_Singlepair_in / Total_TruthEvents
print ' Good PURTIY of signal : ' , str(1.0* Total_singlepair_in_good/Total_singlepair)


n, bins, patches = plt.hist(df_fidEvents_singlepair[df_fidEvents_singlepair.vtx_diff<25].IP,bins=25,range=(0,5),facecolor='red',alpha = 0.8)
n, bins, patches = plt.hist(df_fidEvents_singlepair[df_fidEvents_singlepair.vtx_diff>25].IP,bins=25,range=(0,5),facecolor='blue',alpha = 0.5)
plt.title("first pass IP cuts " )
plt.show()


########
########

# look at the higher pair cases
df_fidEvents_multipair = fid_eventsCUT[fid_eventsCUT.duplicated(subset='jcount' , keep=False)]


multi_group = df_fidEvents_multipair.groupby('jcount')
multipair = multi_group['jcount'].count().hist(bins=10 ,range=(0,10),facecolor = 'blue', alpha = 0.7)
plt.title("Pair Multiplicity")
plt.show()
#Pair Multiplicicty
fid_eventsCUT.groupby('jcount')['jcount'].count().hist(bins=10 ,range=(0,10),facecolor = 'blue', alpha = 0.7)
plt.title("Pair Multiplicity")
plt.show()

print' WORKING AREA '

n, bins, patches = plt.hist(df_fidEvents_multipair.vtx_diff,bins=25,range=(0,500),facecolor='blue',alpha = 0.8)
plt.title('Vertex Diff ')
plt.xlabel('Distance (cm)')
plt.show()




####################################################################
###### Look at the multi and see where things are causeing problems
####################################################################


# Hack in cuts and over write
#_multicuts =  ((df_fidEvents_multipair.showerA_q - df_fidEvents_multipair.showerB_q)/(df_fidEvents_multipair.showerA_q + df_fidEvents_multipair.showerB_q)>-0.6) &((df_fidEvents_multipair.showerA_q - df_fidEvents_multipair.showerB_q)/(df_fidEvents_multipair.showerA_q + df_fidEvents_multipair.showerB_q)<0.6)   
#_multicuts = (df_fidEvents_multipair.angle>0.8)
_multicuts =  (df_fidEvents_multipair.IP>2.3)&(df_fidEvents_multipair.angle<2.0)&(df_fidEvents_multipair.angle>0.9)&((df_fidEvents_multipair.showerA_q - df_fidEvents_multipair.showerB_q)/(df_fidEvents_multipair.showerA_q + df_fidEvents_multipair.showerB_q)>-0.6) &((df_fidEvents_multipair.showerA_q - df_fidEvents_multipair.showerB_q)/(df_fidEvents_multipair.showerA_q + df_fidEvents_multipair.showerB_q)<0.6)   
df_fidEvents_multipair = df_fidEvents_multipair[_multicuts]

plt.hist2d(df_fidEvents_multipair.IP,df_fidEvents_multipair.vtx_diff,bins=30, range=[[0,30],[0,50]],cmap='viridis')
plt.xlabel('IP')
plt.ylabel('vtx_diff')
plt.title('IP')
plt.show()

# look at radL
plt.hist2d(df_fidEvents_multipair.RadL_A+df_fidEvents_multipair.RadL_B,df_fidEvents_multipair.vtx_diff, bins = 30,range=[[0,300],[0,500]] ,cmap ='viridis')
plt.xlabel('Length(cm)')
plt.ylabel('vtx_diff')
plt.title('RadL_SUM')
plt.show()

plt.hist2d(df_fidEvents_multipair.RadL_A-df_fidEvents_multipair.RadL_B,df_fidEvents_multipair.vtx_diff, bins = 30,range=[[-30,30],[0,500]] ,cmap ='viridis')
plt.xlabel('Length(cm)')
plt.ylabel('vtx_diff')
plt.title('RadL_dif')
plt.show()


# look at radL
plt.hist2d(df_fidEvents_multipair[df_fidEvents_multipair.RadL_A<df_fidEvents_multipair.RadL_B].RadL_A,df_fidEvents_multipair[df_fidEvents_multipair.RadL_A<df_fidEvents_multipair.RadL_B].vtx_diff, bins = 30,range=[[0,30],[0,500]] ,cmap ='viridis')
plt.hist2d(df_fidEvents_multipair[df_fidEvents_multipair.RadL_A>df_fidEvents_multipair.RadL_B].RadL_B,df_fidEvents_multipair[df_fidEvents_multipair.RadL_A>df_fidEvents_multipair.RadL_B].vtx_diff, bins = 30,range=[[0,30],[0,500]] ,cmap ='viridis')
plt.xlabel('Length(cm)')
plt.ylabel('vtx_diff')
plt.title('RadL')
plt.show()


#look at angle
plt.hist2d(df_fidEvents_multipair.angle,df_fidEvents_multipair.vtx_diff, bins = 30,range=[[0,3.14159],[0,500]] ,cmap ='viridis')
plt.xlabel('Radians')
plt.ylabel('vtx_diff')
plt.title('OpeningAngle')
plt.show()

#look at charge 
plt.hist2d(df_fidEvents_multipair.showerA_q,df_fidEvents_multipair.vtx_diff, bins = 30,range=[[0,1000000],[0,500]] ,cmap ='viridis')
plt.hist2d(df_fidEvents_multipair.showerB_q,df_fidEvents_multipair.vtx_diff, bins = 30,range=[[0,1000000],[0,500]] ,cmap ='viridis')
plt.xlabel('charge')
plt.ylabel('vtx_diff')
plt.title('shower_cluster Charge')
plt.show()


plt.hist2d(df_fidEvents_multipair.showerA_q+df_fidEvents_multipair.showerB_q ,df_fidEvents_multipair.vtx_diff, bins = 30,range=[[0,5000000],[0,500]] ,cmap ='viridis')
plt.xlabel('charge')
plt.ylabel('vtx_diff')
plt.title('shower_cluster sum Charge')
plt.show()

####### Lets look at histograms for above and below 25
#look at angle
n, bins, patches = plt.hist(df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff>25].angle,bins=30,range=(0,3.14159),facecolor='red',alpha = 0.8)
n, bins, patches = plt.hist(df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff<25].angle,bins=30,range=(0,3.14159),facecolor='blue',alpha = 0.5)
plt.xlabel('Radians')
plt.title('OpeningAngle')
plt.show()

#look at rad L 
n, bins, patches = plt.hist(df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff>25].RadL_A+df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff>25].RadL_B,bins=30,range=(0,100),facecolor='red',alpha = 0.8)
n, bins, patches = plt.hist(df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff<25].RadL_A+df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff<25].RadL_B,bins=30,range=(0,100),facecolor='blue',alpha = 0.5)
plt.xlabel('CM')
plt.title('Rlensum')
plt.show()

n, bins, patches = plt.hist(df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff>25].IP,bins=30,range=(0,5),facecolor='red',alpha = 0.8)
n, bins, patches = plt.hist(df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff<25].IP,bins=30,range=(0,5),facecolor='blue',alpha = 0.5)
plt.xlabel('cm')
plt.title('IP')
plt.show()



n, bins, patches = plt.hist(df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff>25].showerA_q,bins=50,range=(0,10000000),facecolor='red',alpha = 0.8)
n, bins, patches = plt.hist(df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff>25].showerB_q,bins=50,range=(0,10000000),facecolor='red',alpha = 0.8)
n, bins, patches = plt.hist(df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff<25].showerA_q,bins=50,range=(0,10000000),facecolor='blue',alpha = 0.5)
n, bins, patches = plt.hist(df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff<25].showerB_q,bins=50,range=(0,10000000),facecolor='blue',alpha = 0.5)
plt.xlabel('ccharge')
plt.title('charge')
plt.show()


n, bins, patches = plt.hist(df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff>25].showerA_q+df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff>25].showerB_q,bins=50,range=(0,10000000),facecolor='red',alpha = 0.8)
n, bins, patches = plt.hist(df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff<25].showerA_q+df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff<25].showerB_q,bins=50,range=(0,10000000),facecolor='blue',alpha = 0.5)
plt.xlabel('chargesum')
plt.title('chargesum')
plt.show()


n, bins, patches = plt.hist((df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff>25].showerA_q-df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff>25].showerB_q)/(df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff>25].showerA_q+df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff>25].showerB_q),bins=50,range=(-1,1),facecolor='red',alpha = 0.8)
n, bins, patches = plt.hist((df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff<25].showerA_q-df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff<25].showerB_q)/(df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff<25].showerA_q+df_fidEvents_multipair[df_fidEvents_multipair.vtx_diff<25].showerB_q),bins=50,range=(-1,1),facecolor='blue',alpha = 0.5)
plt.xlabel('chargeazy')
plt.title('chargeazy')
plt.show()

print ' ' 
print ' WORKING AREA FROM HACK ' 
df_fidEvents_multipair.groupby('jcount')['jcount'].count().hist(bins=10 ,range=(0,10),facecolor = 'blue', alpha = 0.7)
plt.title("Pair Multiplicity post np>1")
plt.show()

# Plot the vertex diff for the n=1 post 
df_post_singlepair = df_fidEvents_multipair.drop_duplicates(subset='jcount' , keep=False)
n, bins, patches = plt.hist(df_post_singlepair.vtx_diff,bins=4,range=(0,100),facecolor='blue',alpha = 0.8)
plt.title("multi case vertex diff")
plt.show()



#############3
# readout the final efficency and purty 


# What is the total selected
finalframe = [df_fidEvents_singlepair, df_post_singlepair]
df_sel = pd.concat(finalframe)

# FINAL EFFIENCY
print ' Final SELECTION'
total_fs = len(df_sel.index)
# sanity check 
if total_fs!=len(df_sel.drop_duplicates(subset='jcount' , keep=False).index):
    print ' Crazy stuff be EFFed UP!!!!!'


print '####################### ' 
print '####################### ' 
print '####################### ' 

print ' total final single pair selected events' , str(total_fs)

# How many are good
df_sel_good = df_sel[df_sel.vtx_diff<25]
total_fs_good = len(df_sel_good.index)
df_sel_bad = df_sel[df_sel.vtx_diff>25]
total_fs_bad = len(df_sel_bad.index)

print ' total Good single pair selected events' , str(total_fs_good)
print ' total Bad single pair selected events' , str(total_fs_bad)

print 'Final Selected EFF is : ' , str(1.0*total_fs/Total_TruthEvents)

print 'Final Selected Purity is : ' , str(1.0*total_fs_good/total_fs)


























##########################################
#Some genaric plots for some variables 
##########################################
plt.hist2d(df.IP,df.vtx_diff,bins=30, range=[[0,30],[0,50]],cmap='viridis')
plt.xlabel('IP')
plt.ylabel('vtx_diff')
plt.title('IP')
plt.show()

# look at radL
plt.hist2d(df.RadL_A+df.RadL_B,df.vtx_diff, bins = 30,range=[[0,300],[0,200]] ,cmap ='viridis')
plt.xlabel('Length(cm)')
plt.ylabel('vtx_diff')
plt.title('RadL')
plt.show()

#look at angle
plt.hist2d(df.angle,df.vtx_diff, bins = 30,range=[[0,3.14159],[0,200]] ,cmap ='viridis')
plt.xlabel('Radians')
plt.ylabel('vtx_diff')
plt.title('OpeningAngle')
plt.show()

#look at charge 
plt.hist2d(df.showerA_q,df.vtx_diff, bins = 30,range=[[0,1000000],[0,500]] ,cmap ='viridis')
plt.hist2d(df.showerB_q,df.vtx_diff, bins = 30,range=[[0,1000000],[0,500]] ,cmap ='viridis')
plt.xlabel('charge')
plt.ylabel('vtx_diff')
plt.title('shower_cluster Charge')
plt.show()


plt.hist2d(df.showerA_q+df.showerB_q ,df.vtx_diff, bins = 30,range=[[0,5000000],[0,500]] ,cmap ='viridis')
plt.xlabel('charge')
plt.ylabel('vtx_diff')
plt.title('shower_cluster sum Charge')
plt.show()


n, bins, patches = plt.hist(df.vtx_diff,bins=40,range=(0,1000),facecolor='red',alpha = 0.8)
plt.title('Vertex Diff number of events: {}'.format(int(n.sum(axis=0))))
plt.xlabel('Distance (cm)')
plt.show()

df_in = df[ (df.vtx_x>0) & (df.vtx_x<256) &(df.vtx_y> -116) & (df.vtx_y<116)&  (df.vtx_z>0) & (df.vtx_z<1056)]
plt.scatter(df_in.vtx_z,df_in.vtx_y,c=df_in.vtx_diff,cmap=plt.cm.jet)
plt.colorbar()
plt.title('in reconstructed y-z  with vertdiff ')
if _save:
    plt.savefig('{}/Shower_vertex_difference.png'.format(fig_dir))
plt.show()
plt.close()



#######################################################################################

# Add in cuts and plot previous
#_cuts = (df.IP<5) & (df.RadL_A+df.RadL_B>20) &(df.angle<2.5)&(df.angle>0.4)&(df.showerA_q+df.showerB_q>1700000) & (df.showerA_q>250000) & (df.showerB_q>250000)
#_cuts = (df.IP<5) & (df.RadL_A+df.RadL_B<60) & (df.RadL_A+df.RadL_B>20) &(df.angle<2.5)&(df.angle>0.4)&(df.showerA_q+df.showerB_q>1700000) & (df.showerA_q>250000) & (df.showerB_q>250000)&(df.vtx_x>0) & (df.vtx_x<256) &(df.vtx_y> -116) & (df.vtx_y<116)&  (df.vtx_z>400) & (df.vtx_z<1056)
_cuts = (df.IP<5) & (df.RadL_A+df.RadL_B<60) & (df.RadL_A+df.RadL_B>20) &(df.angle<2.5)&(df.angle>0.4)&(df.showerA_q+df.showerB_q>1700000) & (df.showerA_q>250000) & (df.showerB_q>250000)&(df.vtx_x>0) & (df.vtx_x<256) &(df.vtx_y> -116) & (df.vtx_y<116)&  (df.vtx_z>0) & (df.vtx_z<1056)
#_cuts = (df.IP<5) & (df.RadL_A+df.RadL_B>20) &(df.angle<2.5)&(df.angle>0.4)&(df.showerA_q+df.showerB_q>1700000) & (df.showerA_q>250000) & (df.showerB_q>250000)&(df.vtx_x>0) & (df.vtx_x<256) &(df.vtx_y> -116) & (df.vtx_y<116)&  (df.vtx_z>0) & (df.vtx_z<1056)

#df_in = df[ (df.vtx_x>0) & (df.vtx_x<256) &(df.vtx_y> -116) & (df.vtx_y<116)&  (df.vtx_z>0) & (df.vtx_z<1056)]

df_cuts = df[_cuts]
df_drop = df[_cuts].drop_duplicates(subset='jcount' , keep=False)
print ' are there any single cases ? ? ? ' 
print len(df_drop.index)
print ' out of this many events ' 
print len(ev_df.index)

ev_df_in = df_cuts.groupby('jcount').first()
max_bin_ob = ev_df_in.N_objects.max()
plt.hist(ev_df_in.N_objects,range(0,max_bin_ob),facecolor = 'blue', alpha = 0.7)
plt.title('Number of Showers _ Cuts')
plt.show()


plt.hist2d(df_cuts.IP,df_cuts.vtx_diff,bins=30, range=[[0,30],[0,50]],cmap='viridis')
plt.xlabel('IP')
plt.ylabel('vtx_diff')
plt.title('IP')
plt.show()

# look at radL
plt.hist2d(df_cuts.RadL_A+df_cuts.RadL_B,df_cuts.vtx_diff, bins = 30,range=[[0,300],[0,200]] ,cmap ='viridis')
plt.xlabel('Length(cm)')
plt.ylabel('vtx_diff')
plt.title('RadL')
plt.show()

#look at angle
plt.hist2d(df_cuts.angle,df_cuts.vtx_diff, bins = 30,range=[[0,3.14159],[0,200]] ,cmap ='viridis')
plt.xlabel('Radians')
plt.ylabel('vtx_diff')
plt.title('OpeningAngle')
plt.show()


#look at charge 
plt.hist2d(df_cuts.showerA_q,df_cuts.vtx_diff, bins = 30,range=[[0,1000000],[0,500]] ,cmap ='viridis')
plt.hist2d(df_cuts.showerB_q,df_cuts.vtx_diff, bins = 30,range=[[0,1000000],[0,500]] ,cmap ='viridis')
plt.xlabel('charge')
plt.ylabel('vtx_diff')
plt.title('shower_cluster Charge')
plt.show()


plt.hist2d(df_cuts.showerA_q+df_cuts.showerB_q ,df_cuts.vtx_diff, bins = 30,range=[[0,5000000],[0,500]] ,cmap ='viridis')
plt.xlabel('charge')
plt.ylabel('vtx_diff')
plt.title('shower_cluster sum Charge')
plt.show()


n, bins, patches = plt.hist(df_cuts.vtx_diff,bins=50,range=(0,1000),facecolor='red',alpha = 0.8)
plt.title('Vertex Diff number of events: {}'.format(int(n.sum(axis=0))))
plt.xlabel('Distance (cm)')
plt.show()

n, bins, patches = plt.hist(df_drop.vtx_diff,bins=25,range=(0,500),facecolor='red',alpha = 0.8)
plt.title('n=2 case Vertex Diff number of events: {}'.format(int(n.sum(axis=0))))
plt.xlabel('Distance (cm)')
plt.show()


plt.scatter(df_cuts.vtx_z,df_cuts.vtx_y,c=df_cuts.vtx_diff,cmap=plt.cm.jet)
plt.colorbar()
plt.title('in reconstructed y-z  with vertdiff ')
plt.show()


print ' This is the count for the selected events for drop '
print df_drop[df_drop.vtx_diff<20].jcount
print ' This is the count for the selected events for cut '
print df_cuts[df_cuts.vtx_diff<20].jcount


################# Now start to look at different variablesj
df_good =  df_cuts[df_cuts.vtx_diff<20]
df_bad =  df_cuts[df_cuts.vtx_diff>20]


n, bins, patches = plt.hist(df_bad.angle,bins=30,range=(0,3.15),facecolor='red',alpha = 0.4)
n, bins, patches = plt.hist(df_good.angle,bins=30,range=(0,3.15),facecolor='green',alpha = 0.8)
plt.xlabel('Radians')
plt.title('OpeningAngle')
plt.show()


n, bins, patches = plt.hist(df_bad.IP,bins=30,range=(0,20),facecolor='red',alpha = 0.4)
n, bins, patches = plt.hist(df_good.IP,bins=30,range=(0,20),facecolor='green',alpha = 0.8)
plt.xlabel('IP')
plt.title('IP')
plt.show()


n, bins, patches = plt.hist(df_bad.showerA_q+df_bad.showerB_q,bins=30,range=(0,20000000),facecolor='red',alpha = 0.4)
n, bins, patches = plt.hist(df_good.showerA_q+df_good.showerB_q,bins=30,range=(0,20000000),facecolor='green',alpha = 0.8)
plt.xlabel('TotalCharge')
plt.title('TotalCharge')
plt.show()

n, bins, patches = plt.hist(pow((df_bad.showerA_q-df_bad.showerB_q)*(df_bad.showerA_q-df_bad.showerB_q),0.5)/(df_bad.showerA_q+df_bad.showerB_q),bins=30,range=(0,1),facecolor='red',alpha = 0.4)
n, bins, patches = plt.hist(pow((df_good.showerA_q-df_good.showerB_q)*(df_good.showerA_q-df_good.showerB_q),0.5)    /(df_good.showerA_q+df_good.showerB_q),bins=30,range=(0,1),facecolor='green',alpha = 0.4)
plt.xlabel('asym')
plt.title('Charge Asym ')
plt.show()


n, bins, patches = plt.hist(df_bad.showerA_q/df_bad.N_Aspts,bins=30,range=(0,200000),facecolor='red',alpha = 0.4)
n, bins, patches = plt.hist(df_bad.showerB_q/df_bad.N_Bspts,bins=30,range=(0,200000),facecolor='red',alpha = 0.4)
n, bins, patches = plt.hist(df_good.showerA_q/df_good.N_Aspts,bins=30,range=(0,200000),facecolor='green',alpha = 0.4)
n, bins, patches = plt.hist(df_good.showerB_q/df_good.N_Bspts,bins=30,range=(0,200000),facecolor='green',alpha = 0.4)
plt.xlabel('TotalCharge/nspt')
plt.title('TotalCharge/nspt')
plt.show()


n, bins, patches = plt.hist(df_bad.N_Aspts,bins=30,range=(0,200),facecolor='red',alpha = 0.4)
n, bins, patches = plt.hist(df_bad.N_Bspts,bins=30,range=(0,200),facecolor='red',alpha = 0.4)
n, bins, patches = plt.hist(df_good.N_Aspts,bins=30,range=(0,200),facecolor='green',alpha = 0.4)
n, bins, patches = plt.hist(df_good.N_Bspts,bins=30,range=(0,200),facecolor='green',alpha = 0.4)
plt.xlabel('nspt')
plt.title('nspt')
plt.show()

n, bins, patches = plt.hist(df_bad.N_Aspts+df_bad.N_Bspts,bins=30,range=(0,200),facecolor='red',alpha = 0.4)
n, bins, patches = plt.hist(df_good.N_Aspts+df_good.N_Bspts,bins=30,range=(0,200),facecolor='green',alpha = 0.8)
plt.xlabel('sum of nspt')
plt.title('sum of nspt')
plt.show()




n, bins, patches = plt.hist(df_bad.vtx_z,bins=30,range=(0,1100),facecolor='red',alpha = 0.4)
n, bins, patches = plt.hist(df_good.vtx_z,bins=30,range=(0,1100),facecolor='green',alpha = 0.8)
plt.xlabel('xposition')
plt.title('xposition')
plt.show()







####### Print out an efficiency summary 

print ' #### Summary #### '
TotalEvents = len(ev_df.index)
print 'Total Events: ' , str(TotalEvents)
print '' 


TotalROI = len(df_cuts.index)
print 'Total number of candidtate ROIs: ' , str(TotalROI)
goodroi = len(df_good.index)
badroi = len(df_bad.index)
print ' Fraction of ROI within 20cm: ', str(1.*goodroi/TotalROI)
print ' Fraction of ROI greater than 20cm: ', str(1.*badroi/TotalROI)

print '' 

df_drop = df[_cuts].drop_duplicates(subset='jcount' , keep=False)
TotalSingleROI = len(df_drop.index)
df_good_drop = df_drop[df_drop.vtx_diff<20]
TotalGoodSingleROI = len(df_good_drop.index)
df_bad_drop = df_drop[df_drop.vtx_diff>20]
TotalBadSingleROI = len(df_bad_drop.index)
print 'Total number 1 ROIs ' , str(TotalSingleROI)
print 'Fraction of Good/TotalSingleROI  : ' ,str(1.*TotalGoodSingleROI/TotalSingleROI)
print 'Fraction of Bad/TotalSingleROI  : ' ,str(1.*TotalBadSingleROI/TotalSingleROI)

print '' 




######################################################3
######################################################3
######################################################3
print 'next, look at taking the detector in half.... basically at z>500'
print'' 

hdf = df[df.vtx_pi_z>500]
#hdf = df[df.vtx_z>500]
hev_df = hdf.groupby('jcount').first()


hTotalEvents = len(hev_df.index)
print 'Total Events: ' , str(hTotalEvents)
print '' 

hTotalROI = len(df_cuts[df_cuts.vtx_z>500].index)
print 'Total number of candidtate ROIs above z=500cm: ' , str(hTotalROI)
print 'Efficiency  z=500cm: ' , str(1.*hTotalROI/hTotalEvents)
hgoodroi = len(df_good[df_good.vtx_z>500].index)
hbadroi = len(df_bad[df_bad.vtx_z>500].index)
print ' Fraction of goodroi/totROI aka within 20cm: ', str(1.*hgoodroi/hTotalROI)
print ' Fraction of badroi/totROI aka greater than 20cm: ', str(1.*hbadroi/hTotalROI)

print '' 


hdf_drop = df[(_cuts) & (df.vtx_z>500)].drop_duplicates(subset='jcount' , keep=False)
hTotalSingleROI = len(hdf_drop.index)
hdf_good_drop = hdf_drop[hdf_drop.vtx_diff<20]
hTotalGoodSingleROI = len(hdf_good_drop.index)
hdf_bad_drop = hdf_drop[hdf_drop.vtx_diff>20]
hTotalBadSingleROI = len(hdf_bad_drop.index)
print 'Total number 1 ROIs ' , str(hTotalSingleROI)
print 'Fraction of Good/TotalSingleROI  : ' ,str(1.*hTotalGoodSingleROI/hTotalSingleROI)
print 'Fraction of Bad/TotalSingleROI  : ' ,str(1.*hTotalBadSingleROI/hTotalSingleROI)

print '' 






