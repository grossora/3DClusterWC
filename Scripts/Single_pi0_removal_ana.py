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
sns.set()

#bring in the data into pandas 
if(len(sys.argv)==1):
    df = pd.read_csv('../Out_text/test.txt', sep=" ", header = None)
else:
    df = pd.read_csv('{}'.format(sys.argv[1]), sep=" ", header = None)


df.columns = ['totq_mc','totq_reco','totq_thresh','totq_shower','totq_track','frac_reco_mc','frac_thresh_reco','frac_shower_thresh','frac_track_thresh','vtx_x','vtx_y','vtx_z']

print 'number of events ', str(len(df.index))


# Make a few Plots 

#n, bins, patches = plt.hist(df.frac_reco_mc,bins=10 , facecolor='blue', alpha=0.75)

# Make scatter plot for MC and reco
plt.scatter(df.totq_reco,df.totq_mc)
plt.title('WC Charge vs True Charge',fontsize=18)
plt.xlabel('Total Reco Charge',fontsize=18)
plt.ylabel('Total MC Charge',fontsize=18)
plt.show()


n, bins, patches = plt.hist(df.frac_thresh_reco,bins=30 , facecolor='blue', alpha=0.75)
plt.title('Fraction of represented charge from Thresholding at q>3000',fontsize=18)
plt.xlabel('Fraction of charge',fontsize=18)
#plt.ylabel('Total MC Charge',fontsize=18)
plt.show()

n, bins, patches = plt.hist(df.frac_reco_mc,bins=30 , facecolor='blue', alpha=0.75)
plt.title('Fraction RECO /MC',fontsize=18)
plt.xlabel('Fraction of charge',fontsize=18)
#plt.ylabel('Total MC Charge',fontsize=18)
plt.show()


#n, bins, patches = plt.hist(hists,bins=20 ,align='mid', color=colors, label=labels)
n, bins, patches = plt.hist(df.frac_shower_thresh,bins=40 , facecolor='blue', alpha=0.9, label="shower")
n, bins, patches = plt.hist(df.frac_track_thresh,bins=40 , facecolor='red', alpha=0.5,label="track")
plt.legend(prop={'size': 10})
#plt.set_title('bars with legend')
plt.title('Reconstructed Single pi0',fontsize=18)
plt.xlabel('Fraction of charge',fontsize=18)
#plt.ylabel('Total MC Charge',fontsize=18)
plt.show()









