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
    df = pd.read_csv('../Out_text/new_single_sel_ana_bad_wire.txt', sep=" ", header = None)
else:
    df = pd.read_csv('{}'.format(sys.argv[1]), sep=" ", header = None)

df.columns = ['id','totq_mc','totq_reco','totq_thresh','totq_shower','totq_track','frac_reco_mc','frac_thresh_reco','frac_shower_thresh','frac_track_thresh','vtx_x','vtx_y','vtx_z','N_Showers' ,'N_sptA','charge_A', 'N_sptB','charge_B','reco_vtx_x','reco_vtx_y','reco_vtx_z','IP','radl_A','radl_B','angle']


ev_df = df.groupby('id').first()
#make histogram of Nshowers

his = np.histogram(ev_df.N_Showers,bins=max(ev_df.N_Showers))
fig, ax = plt.subplots()
offset = .4
plt.bar(his[1][1:],his[0], color='Blue')
ax.set_xticks(his[1][1:] + offset)
xil = [ str(x) for x in range(max(ev_df.N_Showers))]
ax.set_xticklabels(xil )
plt.title('Number of Showers from Single pi0', fontsize=18)
plt.yticks(fontsize=18)
plt.xticks(fontsize=18)
plt.show()

print len(ev_df)

df_justtwo = df[df.N_Showers==2]
df_moretwo = df[df.N_Showers>2]
print ' length of 2 shower' 
print len(df_justtwo)

#Vertex Resolution 


n, bins, patches = plt.hist(df_justtwo.vtx_x - df_justtwo.reco_vtx_x,bins=50 , facecolor='blue', alpha=0.75)
plt.show()


n, bins, patches = plt.hist(df_justtwo.vtx_y - df_justtwo.reco_vtx_y,bins=50 , facecolor='blue', alpha=0.75)
plt.show()


n, bins, patches = plt.hist(df_justtwo.vtx_z - df_justtwo.reco_vtx_z,bins=50 , facecolor='blue', alpha=0.75)
plt.show()

vtx_offset = pow( pow(df_justtwo.vtx_x -df_justtwo.reco_vtx_x ,2) + pow(df_justtwo.vtx_y -df_justtwo.reco_vtx_y ,2)+ pow(df_justtwo.vtx_z -df_justtwo.reco_vtx_z ,2),0.5)
n, bins, patches = plt.hist(vtx_offset,bins=50 , facecolor='blue', alpha=0.75)
plt.show()




#### Look at IP 
n, bins, patches = plt.hist(df_justtwo.IP ,bins=100 , facecolor='blue', alpha=0.75,normed=True)
n, bins, patches = plt.hist(df_moretwo.IP ,bins=100 , facecolor='red', alpha=0.75, normed=True)
plt.title("IP")
plt.xlim([0,100])
plt.show()



n, bins, patches = plt.hist(df_justtwo.angle ,bins=20 , facecolor='blue', alpha=0.75, normed=True)
n, bins, patches = plt.hist(df_moretwo.angle ,bins=20 , facecolor='red', alpha=0.75, normed=True)
plt.title("angle Norm")
plt.show()


'''
# Make a few Plots 
#n, bins, patches = plt.hist(df.frac_reco_mc,bins=10 , facecolor='blue', alpha=0.75)

# Make scatter plot for MC and reco
plt.scatter(df.totq_mc,df.totq_reco)
plt.title('WC Charge vs True Charge',fontsize=18)
plt.ylabel('Total Reco Charge',fontsize=18)
plt.xlabel('Total MC Charge',fontsize=18)
plt.show()

########
# Check if the charge fraction is dependent on some given position information
########
plt.scatter(df.totq_reco,df.totq_mc-0.5*df.totq_reco)
plt.title('WC Charge vs Charge Difference',fontsize=18)
plt.xlabel('Total Reco Charge',fontsize=18)
plt.ylabel('Total Charge Dif',fontsize=18)
plt.show()

########
# Histogram of resolution 
########
n, bins, patches = plt.hist((df.totq_mc-0.5*df.totq_reco)/df.totq_mc,bins=30 , facecolor='blue', alpha=0.75)
plt.title('Total Charge Resolution',fontsize=18)
plt.xlabel('resolution of total charge', fontsize=18)
plt.show()


########
# Position Dependent resolutions 
########
plt.scatter(df.vtx_z, df.vtx_y, c = (df.totq_mc-0.5*df.totq_reco)/df.totq_mc, cmap='jet', s=100)
#clim=(0.0, 0.7)
plt.title('yz pos vs res',fontsize=18)
plt.xlabel('Z-Position',fontsize=18)
plt.ylabel('Y-Position',fontsize=18)
plt.colorbar()
plt.show()

plt.scatter(df.vtx_z, df.vtx_x, c = (df.totq_mc-0.5*df.totq_reco)/df.totq_mc, cmap='jet', s=100)
plt.title('xz pos vs res',fontsize=18)
plt.xlabel('Z-Position',fontsize=18)
plt.ylabel('x-Position',fontsize=18)
plt.colorbar()
plt.show()

plt.scatter(df.vtx_x, df.vtx_y, c = (df.totq_mc-0.5*df.totq_reco)/df.totq_mc, cmap='jet', s=100)
plt.title('xy pos vs res',fontsize=18)
plt.xlabel('X-Position',fontsize=18)
plt.ylabel('Y-Position',fontsize=18)
plt.colorbar()
plt.show()




n, bins, patches = plt.hist(df.frac_thresh_reco,bins=30 , facecolor='blue', alpha=0.75)
plt.title('Fraction of represented charge from Thresholding at q>3000',fontsize=18)
plt.xlabel('Fraction of charge',fontsize=18)
plt.show()

n, bins, patches = plt.hist(df.totq_shower/df.totq_thresh,bins=30 , facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(df.totq_shower/df.totq_thresh)
aavg = np.average(df.totq_shower/df.totq_thresh)
plt.title(r'Fraction of Shower Tracks from Threshold Charge'  '\n' r'average=%.3f' %(aavg), fontsize=18)
#plt.title(r'Fraction of Shower Tracks from Threshold Charge'  '\n' r' :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma), fontsize=18)
plt.xlabel('Charge Fraction',fontsize=18)

#plt.ylabel('Total MC Charge',fontsize=18)
plt.show()


########
# Check if the charge fraction is dependent on some given position information
########
plt.scatter(df.totq_thresh,df.totq_shower/df.totq_thresh)
plt.title('Shower_frac vs Charge above threshold',fontsize=18)
plt.ylabel('shower charge frac',fontsize=18)
plt.xlabel('Charge',fontsize=18)
plt.show()



########
# Shower Position Dependent resolutions 
########
plt.scatter(df.vtx_z, df.vtx_y, c = df.totq_shower/df.totq_thresh, cmap='jet', s=100)
#clim=(0.0, 0.7)
plt.title('yz pos vs Shower_Frac',fontsize=18)
plt.xlabel('Z-Position',fontsize=18)
plt.ylabel('Y-Position',fontsize=18)
plt.colorbar()
plt.show()

plt.scatter(df.vtx_z, df.vtx_x, c = df.totq_shower/df.totq_thresh, cmap='jet', s=100)
plt.title('xz pos vs Shower_Frac',fontsize=18)
plt.xlabel('Z-Position',fontsize=18)
plt.ylabel('x-Position',fontsize=18)
plt.colorbar()
plt.show()

plt.scatter(df.vtx_x, df.vtx_y, c = df.totq_shower/df.totq_thresh, cmap='jet', s=100)
plt.title('xy pos vs Shower_Frac',fontsize=18)
plt.xlabel('X-Position',fontsize=18)
plt.ylabel('Y-Position',fontsize=18)
plt.colorbar()
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

'''