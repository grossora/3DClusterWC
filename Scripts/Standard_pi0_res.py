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
_save = True
#_save = True
#Show items?
_show = True 
#_show = True
#Where to save things? 
#fig_dir = os.getcwd()+'/Figs/test'
fig_dir = os.getcwd()+'/Figs/version1_sel'
#fig_dir = os.getcwd()+'/Figs/version_low'
if not os.path.isdir(fig_dir):
    print 'makeing this for you'
    os.makedirs(fig_dir) 




#bring in the data into pandas 
if(len(sys.argv)==1):
    df = pd.read_csv('../Out_text/Full_Ana_Pi0_pair.txt', sep=" ", header = None)
else:
    df = pd.read_csv('{}'.format(sys.argv[1]), sep=" ", header = None)

df.columns = ['jcount','N_objects','dalitz','vtx_pi_x','vtx_pi_y','vtx_pi_z','p_pi_x','p_pi_y','p_pi_z','p_pi_mag','vtx_gamma_x','vtx_gamma_y','vtx_gamma_z','p_gamma_x','p_gamma_y','p_gamma_z','p_gamma_mag','vtx_gamma_2_x','vtx_gamma_2_y','vtx_gamma_2_z','p_gamma_2_x','p_gamma_2_y','p_gamma_2_z','p_gamma_2_mag','gamma_angle','OMC_gamma_angle', 'tot_mc_q','tot_reco_q','tot_thresh_q', 'tot_shower_q', 'tot_track_q', 'frac_reco_per_mc', 'frac_thresh_per_reco','frac_shower_per_thresh','frac_track_per_thresh','frac_shower_per_reco' ,'frac_track_per_reco', 'vtx_diff','N_Aspts','showerA_q','N_Bspts','showerB_q','vtx_x','vtx_y','vtx_z','IP','RadL_A','RadL_B','angle']
###############################e
#remove out the dalitz decays just for now to make life easier
# Set up some useful Dataframes
df = df[df.dalitz==0]
ev_df = df.groupby('jcount').first()
#Split the dataframes into 1 shower and multi shower
df_one = df[df.N_objects==1]
df_mult = df[(df.N_objects>1)]
# A dataframe that looks at charge fraction
charge_frame = pd.concat([ev_df.tot_mc_q ,ev_df.tot_reco_q, ev_df.tot_thresh_q ,ev_df.tot_shower_q, ev_df.tot_track_q, ev_df.frac_reco_per_mc, ev_df.frac_thresh_per_reco ,ev_df.frac_shower_per_thresh, ev_df.frac_track_per_thresh ,ev_df.frac_shower_per_reco ,ev_df.frac_track_per_reco] , axis=1)
################################

# Have some standard plots
################################
# How many Shower Objects
################################
max_bin_ob = ev_df.N_objects.max()
plt.hist(ev_df.N_objects,range(0,max_bin_ob),facecolor = 'blue', alpha = 0.7)
plt.title('Number of Showers')
if _save:
    plt.savefig('{}/N_showers.png'.format(fig_dir))
if _show:
    plt.show()
plt.close()

################################
# Frame for the charge fraction
# not really needed just easier
################################
#charge_frame.hist(bins=40,facecolor='blue',alpha = 0.8)
show_charge = charge_frame.drop( ['tot_track_q','frac_track_per_reco'] ,axis=1)
show_charge.hist(bins=40,facecolor='blue',alpha = 0.8)
if _save:
    plt.savefig('{}/Charge_frame.png'.format(fig_dir))
if _show:
    plt.show()
plt.close()


################################
# FRACTION of reco / mc
################################
fig, axes = plt.subplots(nrows=1, ncols=3)
ax0, ax1, ax2 = axes.flatten()

ax0.hist(charge_frame.frac_reco_per_mc,bins=40,facecolor='green',alpha = 0.8)
ax0.set_title('Charge Fraction of reco / MC')
#plt.show()

ax1.hist(charge_frame.frac_shower_per_reco,bins=40,facecolor='green',alpha = 0.8)
ax1.set_title('Charge Fraction of shower / reco')
#plt.show()

ax2.hist(charge_frame.frac_shower_per_thresh,bins=40,facecolor='green',alpha = 0.8)
ax2.set_title('Charge Fraction of shower / thresh')
fig.tight_layout(rect=(0,0.33,1,.66))

if _save:
    plt.savefig('{}/Charge_frac.png'.format(fig_dir))
if _show:
    plt.show()
plt.close()


################################
# Missing Charge  
################################
plt.hist(( charge_frame.tot_thresh_q - (charge_frame.tot_shower_q +charge_frame.tot_track_q)  )/charge_frame.tot_thresh_q ,bins=40,facecolor='red',alpha = 0.8)
plt.title("Fraction of unclustered charge")
if _save:
    plt.savefig('{}/uncluster_Charge.png'.format(fig_dir))
if _show:
    plt.show()
plt.close()


################################
# Charge Resolution  
################################
plt.hist((charge_frame.tot_mc_q - 0.5*charge_frame.tot_reco_q )/charge_frame.tot_mc_q ,bins=40,facecolor='red',alpha = 0.8)
#plt.hist((charge_frame.tot_mc_q -0.5*charge_frame.tot_reco_q )/charge_frame.tot_mc_q ,bins=40,facecolor='red',alpha = 0.8)
plt.title('True-WCreco/True Charge Resolution')
if _save:
    plt.savefig('{}/Charge_res.png'.format(fig_dir))
if _show:
    plt.show()
plt.close()

plt.hist(1.-(charge_frame.tot_thresh_q -charge_frame.tot_shower_q )/charge_frame.tot_thresh_q ,bins=40,facecolor='red',alpha = 0.8)
plt.title('Clustering ')
plt.xlabel('1 - (Thresh - Tot_showers)/Thresh Charge')
if _save:
    plt.savefig('{}/Shower_Clustering.png'.format(fig_dir))
if _show:
    plt.show()
plt.close()
















################################
# vertex Resolution  
################################

#df_mult.vtx_diff
#df_mult.vtx_diff.hist(bins=40,range=(0,300), facecolor='green',alpha = 0.8)
#plt.show()

df_2 = df[(df.N_objects==2)]
df_3 = df[(df.N_objects==3)]
df_g4 = df[(df.N_objects>=4)]

df_mult.vtx_diff.hist(bins=40,range=(0,300), facecolor='black',alpha = 0.8,  label="All")
df_2.vtx_diff.hist(bins=40,range=(0,300),alpha = 0.7, label="2-Shower")
df_3.vtx_diff.hist(bins=40,range=(0,300),alpha = 0.6, label="3-Shower")
df_g4.vtx_diff.hist(bins=40,range=(0,300),facecolor = 'yellow',alpha = 0.1, label=">=4-Shower")
plt.xlabel('cm')
plt.title('reconstructed vertex difference')
plt.legend()

if _save:
    plt.savefig('{}/vertex_diff.png'.format(fig_dir))
if _show:
    plt.show()
plt.close()


df_2.vtx_diff.hist(bins=40,range=(0,300),alpha = 0.7, label="2-Shower")
plt.xlabel('cm')
plt.title('reconstructed vertex difference')
if _save:
    plt.savefig('{}/2showervertex_diff.png'.format(fig_dir))
if _show:
    plt.show()
plt.close()






print '==============================='
print ' Lets have a summary'
print '==============================='
print 'This is how many n=2 shower '
print df_2.shape[0]
print 'This is how many n=2 shower below 20cm'
print df_2[df.vtx_diff<20].shape[0]
print 'This this a fraction of '
print df_2[df.vtx_diff<20].shape[0]/df_2.shape[0]







# vertex res vs angle 
mdf = df_mult[(df_mult.vtx_diff<300)]
#sns.lmplot(x="showerA_q", y="vtx_diff",hue="N_objects",fit_reg=False, data=mdf)
#sns.lmplot(x="showerB_q", y="vtx_diff",hue="N_objects",fit_reg=False, data=mdf)
#plt.show()
plt.scatter(mdf.showerA_q+mdf.showerB_q, mdf.vtx_diff)
plt.show()



sns.lmplot(x="IP", y="vtx_diff",hue="N_objects",fit_reg=False, data=mdf)
plt.show()


sns.lmplot(x="angle", y="vtx_diff",hue="N_objects",fit_reg=False, data=mdf)
plt.show()

plt.scatter(mdf.vtx_z,mdf.vtx_y,c=mdf.vtx_diff,cmap=plt.cm.coolwarm)
plt.colorbar()
plt.show()

sns.lmplot(x="RadL_A", y="vtx_diff",hue="N_objects",fit_reg=False, data=mdf)
sns.lmplot(x="RadL_B", y="vtx_diff",hue="N_objects",fit_reg=False, data=mdf)
plt.show()




