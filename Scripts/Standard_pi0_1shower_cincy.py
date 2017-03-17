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

#bring in the data into pandas 
if(len(sys.argv)==1):
    df_shower = pd.read_csv('../Out_text/lhullShower_pi0.txt', sep=" ", header = None)
else:
    #deprecated
    df_shower = pd.read_csv('{}'.format(sys.argv[1]), sep=" ", header = None)

df_shower.columns = ['jcount','mc_x','mc_y','mc_z','tot_mc_q','tot_reco_q','tot_threco_q', 'tot_shower_q', 'tot_track_q', 'frac_reco_per_mc', 'frac_thresh_per_reco','frac_shower_per_thresh','frac_track_per_thresh','frac_shower_per_reco' ,'frac_track_per_reco'      ,'N_objects', 'N_spts', 'tot_q','avg_x','avg_y','avg_z','wavg_x','wavg_y','wavg_z', 'hull_length', 'hull_area','hull_volume','pca_0','pca_1','pca_2','pca_0r','pca_1r','pca_2r']

# Have some standard plots
ev_df = df_shower.groupby('jcount').first()

# How many Shower Objects
#plt.hist(ev_df.N_objects, facecolor = 'red', alpha = 0.6)
max_bin_ob = ev_df.N_objects.max()
plt.hist(ev_df.N_objects,range(0,max_bin_ob),facecolor = 'blue', alpha = 0.7)
plt.title('number of reco shower objects')
plt.show()

#df_one = df_shower[df_shower.N_objects==2]
df_one = df_shower[df_shower.N_objects==1]
print ' this is the n=1 case ' 

#How close is the wavg to the mc_vtx

plt.hist( pow(pow(df_one.mc_x -df_one.wavg_x,2)+pow(df_one.mc_z -df_one.wavg_z,2)+pow(df_one.mc_z -df_one.wavg_z,2),0.5)  ,bins = 40, facecolor = 'blue', alpha = 0.7)
plt.title('truthvtx_WAVG diff')
plt.show()

# Look at this difference for some parameters
#plt.scatter( pow(pow(df_shower.mc_x -df_shower.wavg_x,2)+pow(df_shower.mc_z -df_shower.wavg_z,2)+pow(df_shower.mc_z -df_shower.wavg_z,2),0.5)  , facecolor = 'blue', alpha = 0.7)
plt.scatter(df_one.N_spts, pow(pow(df_one.mc_x -df_one.wavg_x,2)+pow(df_one.mc_z -df_one.wavg_z,2)+pow(df_one.mc_z -df_one.wavg_z,2),0.5)  , facecolor = 'blue', alpha = 0.7)
plt.title('N_SPTS: truthvtx_WAVG diff')
plt.xlabel('N_SPTS')
plt.ylabel('truthvtx_WAVG diff')
plt.show()

# look at charge
plt.scatter(df_one.tot_q, pow(pow(df_one.mc_x -df_one.wavg_x,2)+pow(df_one.mc_z -df_one.wavg_z,2)+pow(df_one.mc_z -df_one.wavg_z,2),0.5)  , facecolor = 'blue', alpha = 0.7)
plt.title('tot_q: truthvtx_WAVG diff')
plt.xlabel('tot_q')
plt.ylabel('truthvtx_WAVG diff')
plt.show()

#What about PCA
plt.scatter(df_one.pca_0r, pow(pow(df_one.mc_x -df_one.wavg_x,2)+pow(df_one.mc_z -df_one.wavg_z,2)+pow(df_one.mc_z -df_one.wavg_z,2),0.5)  , facecolor = 'blue', alpha = 0.7)
plt.scatter(df_one.pca_1r, pow(pow(df_one.mc_x -df_one.wavg_x,2)+pow(df_one.mc_z -df_one.wavg_z,2)+pow(df_one.mc_z -df_one.wavg_z,2),0.5)  , facecolor = 'red', alpha = 0.7)
plt.scatter(df_one.pca_2r, pow(pow(df_one.mc_x -df_one.wavg_x,2)+pow(df_one.mc_z -df_one.wavg_z,2)+pow(df_one.mc_z -df_one.wavg_z,2),0.5)  , facecolor = 'green', alpha = 0.7)
plt.title('various pca: truthvtx_WAVG diff')
plt.xlabel('pca_ratio')
plt.ylabel('truthvtx_WAVG diff')
plt.show()

# Look at hull
plt.scatter(df_one.hull_area, pow(pow(df_one.mc_x -df_one.wavg_x,2)+pow(df_one.mc_z -df_one.wavg_z,2)+pow(df_one.mc_z -df_one.wavg_z,2),0.5)  , facecolor = 'green', alpha = 0.7)
plt.title('hull_area: truthvtx_WAVG diff')
plt.xlabel('area')
plt.ylabel('truthvtx_WAVG diff')
plt.show()

plt.scatter(df_one.hull_volume, pow(pow(df_one.mc_x -df_one.wavg_x,2)+pow(df_one.mc_z -df_one.wavg_z,2)+pow(df_one.mc_z -df_one.wavg_z,2),0.5)  , facecolor = 'green', alpha = 0.7)
plt.title('hull_volume: truthvtx_WAVG diff')
plt.xlabel('volume')
plt.ylabel('truthvtx_WAVG diff')
plt.show()

plt.scatter(df_one.hull_length, pow(pow(df_one.mc_x -df_one.wavg_x,2)+pow(df_one.mc_z -df_one.wavg_z,2)+pow(df_one.mc_z -df_one.wavg_z,2),0.5)  , facecolor = 'green', alpha = 0.7)
plt.title('hull_length: truthvtx_WAVG diff')
plt.xlabel('length')
plt.ylabel('truthvtx_WAVG diff')
plt.show()
