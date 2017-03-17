import os 
import sys
import pandas as pd
import numpy as np
import seaborn as sns
import pylab as plt
import math as math
import matplotlib.mlab as mlab
from scipy.stats import norm
import collections as col
from itertools import combinations
#sns.set()
import seaborn as sns
#sns.set(style="white", color_codes=True ,{'' : True})
sns.set_style("white", {"axes.grid": True})
from matplotlib import colors
from matplotlib.colors import LogNorm





# Save items? 
#_save = True
_save = True
#Show items?
_show = True

fig_dir = os.getcwd()+'/Figs/Cincy/Standard_cosmicpi0'
if not os.path.isdir(fig_dir):
    print 'makeing this for you'
    os.makedirs(fig_dir)

#bring in the data into pandas 
if(len(sys.argv)==1):
    df = pd.read_csv('../Out_text/lhull_Ana_pair_Cosmic_pair.txt', sep=" ", header = None)
    #df = pd.read_csv('../Out_text/cosmics_vertex_ana.txt', sep=" ", header = None)
else:
    #deprecated
    df = pd.read_csv('{}'.format(sys.argv[1]), sep=" ", header = None)

df.columns = ['jcount','N_objects','dalitz','vtx_pi_x','vtx_pi_y','vtx_pi_z','p_pi_x','p_pi_y','p_pi_z','p_pi_mag','vtx_gamma_x','vtx_gamma_y','vtx_gamma_z','p_gamma_x','p_gamma_y','p_gamma_z','p_gamma_mag','vtx_gamma_2_x','vtx_gamma_2_y','vtx_gamma_2_z','p_gamma_2_x','p_gamma_2_y','p_gamma_2_z','p_gamma_2_mag','gamma_angle','OMC_gamma_angle', 'tot_mc_q','tot_reco_q','tot_thresh_q', 'tot_shower_q', 'tot_track_q', 'frac_reco_per_mc', 'frac_thresh_per_reco','frac_shower_per_thresh','frac_track_per_thresh','frac_shower_per_reco' ,'frac_track_per_reco', 'vtx_diff','N_Aspts','showerA_q','N_Bspts','showerB_q','vtx_x','vtx_y','vtx_z','IP','RadL_A','RadL_B','angle']

 

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

#######################################################################################

# Add in cuts and plot previous
#_cuts = (df.IP<5) & (df.RadL_A+df.RadL_B>20) &(df.angle<2.5)&(df.angle>0.4)&(df.showerA_q+df.showerB_q>1700000) & (df.showerA_q>250000) & (df.showerB_q>250000)
_cuts = (df.IP<5) & (df.RadL_A+df.RadL_B<60) & (df.RadL_A+df.RadL_B>20) &(df.angle<2.5)&(df.angle>0.4)&(df.showerA_q+df.showerB_q>1700000) & (df.showerA_q>250000) & (df.showerB_q>250000)&(df.vtx_x>0) & (df.vtx_x<256) &(df.vtx_y> -116) & (df.vtx_y<116)&  (df.vtx_z>0) & (df.vtx_z<1056)
#_cuts = (df.IP<5) & (df.RadL_A+df.RadL_B>20) &(df.angle<2.5)&(df.angle>0.4)&(df.showerA_q+df.showerB_q>1700000) & (df.showerA_q>250000) & (df.showerB_q>250000)&(df.vtx_x>0) & (df.vtx_x<256) &(df.vtx_y> -116) & (df.vtx_y<116)&  (df.vtx_z>0) & (df.vtx_z<1056)

#df_in = df[ (df.vtx_x>0) & (df.vtx_x<256) &(df.vtx_y> -116) & (df.vtx_y<116)&  (df.vtx_z>0) & (df.vtx_z<1056)]

df_cuts = df[_cuts]
df_drop = df[_cuts].drop_duplicates(subset='jcount' , keep=False)
print ' are there any single cases ? ? ? ' 
print len(df_drop.index)
print ' out of this many events ' 
print len(ev_df.index)


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






























'''

###############################################################################################


##########################################
#Some genaric plots for some variables 
##########################################

# look at IP
plt.scatter(df.IP,df.vtx_diff, facecolor = 'blue', alpha = 0.5)
plt.xlim(0,30)
plt.ylim(0,1000)
plt.xlabel('IP')
plt.ylabel('vtx_diff')
plt.title('IP')
plt.show()

plt.hist2d(df.IP,df.vtx_diff,bins=50, range=[[0,30],[0,1000]],cmap='viridis')
plt.xlabel('IP')
plt.ylabel('vtx_diff')
plt.title('IP')
plt.show()


# look at radL
plt.scatter(df.RadL_A,df.vtx_diff, facecolor = 'blue', alpha = 0.5)
plt.scatter(df.RadL_B,df.vtx_diff, facecolor = 'red', alpha = 0.5)
plt.xlabel('Length(cm)')
plt.ylabel('vtx_diff')
plt.title('RadL')
plt.show()

plt.scatter(df.RadL_A+df.RadL_B,df.vtx_diff, facecolor = 'green', alpha = 0.5)
plt.xlabel('Length(cm)')
plt.ylabel('vtx_diff')
plt.title('RadLA+RadLB')
plt.show()

# Look at angle
plt.scatter(df.angle,df.vtx_diff, facecolor = 'blue', alpha = 0.5)
plt.xlabel('Radians')
plt.ylabel('vtx_diff')
plt.title('OpeningAngle')
plt.show()

# We also want to look at charge
plt.scatter(df.showerA_q,df.vtx_diff, facecolor = 'blue', alpha = 0.5)
plt.scatter(df.showerB_q,df.vtx_diff, facecolor = 'red', alpha = 0.5)
plt.xlabel('charge')
plt.ylabel('vtx_diff')
plt.title('shower_cluster Charge')
plt.show()

# We also want to look at charge
plt.scatter(df.showerA_q/df.N_Aspts,df.vtx_diff, facecolor = 'blue', alpha = 0.5) 
plt.scatter(df.showerB_q/df.N_Bspts,df.vtx_diff, facecolor = 'red', alpha = 0.5) 
plt.xlabel('charge/spts') 
plt.ylabel('vtx_diff') 
plt.title('charge/spts') 
plt.show() 
 


n, bins, patches = plt.hist(df.showerA_q,bins=40,range=(0,10000000) ,facecolor='blue',alpha = 0.8)
n, bins, patches = plt.hist(df.showerB_q,bins=40,range=(0,10000000) ,facecolor='red',alpha = 0.8)
plt.xlabel('charge')
plt.title('shower_cluster Charge')
plt.show()

n, bins, patches = plt.hist(df.showerA_q+df.showerB_q,bins=40,range=(0,6000000) ,facecolor='blue',alpha = 0.8)
plt.show()


n, bins, patches = plt.hist(df.showerA_q,bins=40,range=(0,2000000),facecolor='blue',alpha = 0.8)
n, bins, patches = plt.hist(df.showerB_q,bins=40,range=(0,2000000),facecolor='red',alpha = 0.8)
plt.xlabel('charge')
plt.title('shower_cluster Charge')
plt.show()


# We also want to look at charge
plt.scatter(df.N_Aspts,df.vtx_diff, facecolor = 'blue', alpha = 0.5)
plt.scatter(df.N_Bspts,df.vtx_diff, facecolor = 'red', alpha = 0.5)
plt.xlabel('spts')
plt.ylabel('vtx_diff')
plt.title('spts')
plt.show()



# What is going on with the location of reconstruction
plt.scatter(df.vtx_z,df.vtx_y, facecolor = 'blue', alpha = 0.5)
plt.title('reconstructed y-z')
plt.show()

#Make things reconstruct inside
df_in = df[ (df.vtx_x>0) & (df.vtx_x<256) &(df.vtx_y> -116) & (df.vtx_y<116)&  (df.vtx_z>0) & (df.vtx_z<1056)]


plt.scatter(df_in.vtx_z,df_in.vtx_y, facecolor = 'blue', alpha = 0.5)
plt.title('in+ reconstructed y-z  ')
plt.show()

plt.scatter(df_in.vtx_z,df_in.vtx_y,c=df_in.vtx_diff,cmap=plt.cm.jet)
#plt.scatter(df_in.vtx_z,df_in.vtx_y,c=df_in.vtx_diff,cmap=plt.cm.coolwarm)
plt.colorbar()
plt.title('in+ reconstructed y-z  with vertdiff ')
plt.show()

sns.lmplot(x='vtx_z',y='vtx_diff',data=df_in, scatter_kws = {'facecolors':'green'})
plt.show()




################
# Make cuts and see which satisy
################
_cuts = (df.IP<5) & (df.RadL_A+df.RadL_B>20) &(df.angle<2.5)&(df.angle>0.4)&(df.showerA_q+df.showerB_q>1700000) & (df.showerA_q>250000) & (df.showerB_q>250000)
#_cuts = (df.IP<5) & (df.RadL_A+df.RadL_B>20) &(df.angle<2.5)&(df.angle>0.4)
#_cuts = (df.IP<20) & (df.RadL_A+df.RadL_B>20)& (df.RadL_A+df.RadL_B<150) &(df.angle<2.0)&(df.angle>0.4)

df_cuts = df[_cuts]
df_drop = df[_cuts].drop_duplicates(subset='jcount' , keep=False)

print df_drop

n, bins, patches = plt.hist(df_cuts.vtx_diff,bins=40,facecolor='red',alpha = 0.8)
#print n.sum(axis=0)
##print np.bincount(n.astype(int))
plt.title('Vertex Diff number of events: {}'.format(int(n.sum(axis=0))))
plt.xlabel('Distance (cm)')
plt.show()



#Look at scatter plots post cuts



# look at IP
plt.scatter(df_cuts.IP,df_cuts.vtx_diff, facecolor = 'blue', alpha = 0.5)
plt.xlabel('IP')
plt.ylabel('vtx_diff')
plt.title('IP')
plt.show()


# look at radL
plt.scatter(df_cuts.RadL_A,df_cuts.vtx_diff, facecolor = 'blue', alpha = 0.5)
plt.scatter(df_cuts.RadL_B,df_cuts.vtx_diff, facecolor = 'red', alpha = 0.5)
plt.xlabel('Length(cm)')
plt.ylabel('vtx_diff')
plt.title('RadL')
plt.show()

plt.scatter(df_cuts.RadL_A+df_cuts.RadL_B,df_cuts.vtx_diff, facecolor = 'green', alpha = 0.5)
plt.xlabel('Length(cm)')
plt.ylabel('vtx_diff')
plt.title('RadLA+RadLB')
plt.show()

# Look at angle
plt.scatter(df_cuts.angle,df_cuts.vtx_diff, facecolor = 'blue', alpha = 0.5)
plt.xlabel('Radians')
plt.ylabel('vtx_diff')
plt.title('OpeningAngle')
plt.show()

# We also want to look at charge
plt.scatter(df_cuts.showerA_q,df_cuts.vtx_diff, facecolor = 'blue', alpha = 0.5)
plt.scatter(df_cuts.showerB_q,df_cuts.vtx_diff, facecolor = 'red', alpha = 0.5)
plt.xlabel('charge')
plt.ylabel('vtx_diff')
plt.title('shower_cluster Charge')
plt.show()

n, bins, patches = plt.hist(df_cuts.showerA_q,bins=40,facecolor='blue',alpha = 0.8)
n, bins, patches = plt.hist(df_cuts.showerB_q,bins=40,facecolor='red',alpha = 0.8)
plt.xlabel('charge')
plt.title('shower_cluster Charge')
plt.show()

n, bins, patches = plt.hist(df_cuts.showerA_q,bins=40,range=(0,2000000),facecolor='blue',alpha = 0.8)
n, bins, patches = plt.hist(df_cuts.showerB_q,bins=40,range=(0,2000000),facecolor='red',alpha = 0.8)
plt.xlabel('charge')
plt.title('shower_cluster Charge')
plt.show()





















# Drop out first col
df_one = df[df.N_objects==1]
df_one = df_one.drop('jcount',1)

df_mult = df[(df.N_objects>1) &(df.IP>0) &(df.vtx_diff<300)]
#df_mult = df[(df.N_objects>1) &(df.IP>0)]

df_mult = df_mult.drop('jcount',1)


df_mult.hist(bins=40,facecolor='blue',alpha = 0.8)
plt.show()




df_mult.vtx_diff.hist(bins=40,range=(0,100))
df_mult[df_mult.IP<10].vtx_diff.hist(bins=40,range=(0,100))

plt.show()
'''
