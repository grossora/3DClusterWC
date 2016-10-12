import sys
import pandas as pd 
import numpy as np
import seaborn as sns 
import pylab as plt
import math as math
import matplotlib.mlab as mlab
from scipy.stats import norm
import collections as col
from operator import itemgetter
from itertools import combinations
sns.set()

#bring in the data into pandas 
if(len(sys.argv)==1):
    df = pd.read_csv('../Out_text/PiZero_Selection_Params.txt', sep=" ", header = None)
else:
    df = pd.read_csv('{}'.format(sys.argv[1]), sep=" ", header = None)
   
#df.columns = ['dirnum','fnum','dalitz','mc_pi_vtx_x','mc_pi_vtx_y','mc_pi_vtx_z','mc_pi_mom_x','mc_pi_mom_y','mc_pi_mom_z','mc_pi_mom_mag','mc_gamma_A_vtx_x','mc_gamma_A_vtx_y','mc_gamma_A_vtx_z','mc_gamma_A_mom_x','mc_gamma_A_mom_y','mc_gamma_A_mom_z','mc_gamma_A_mom_mag','mc_gamma_B_vtx_x','mc_gamma_B_vtx_y','mc_gamma_B_vtx_z','mc_gamma_B_mom_x','mc_gamma_B_mom_y','mc_gamma_B_mom_z','mc_gamma_B_mom_mag','mc_opening_angle','mc_OMcos','mass','pi_vtx_x','pi_vtx_y','pi_vtx_z','Energy_A','gamma_A_vtx_x','gamma_A_vtx_y','gamma_A_vtx_z','Energy_B','gamma_B_vtx_x','gamma_B_vtx_y','gamma_B_vtx_z','opening_angle','OMcos','IP','conversion_A','conversion_B']

df.columns = ['dirnum','fnum','dalitz','mc_pi_vtx_x','mc_pi_vtx_y','mc_pi_vtx_z','mc_pi_mom_x','mc_pi_mom_y','mc_pi_mom_z','mc_pi_mom_mag','mc_gamma_A_vtx_x','mc_gamma_A_vtx_y','mc_gamma_A_vtx_z','mc_gamma_A_mom_x','mc_gamma_A_mom_y','mc_gamma_A_mom_z','mc_gamma_A_mom_mag','mc_gamma_B_vtx_x','mc_gamma_B_vtx_y','mc_gamma_B_vtx_z','mc_gamma_B_mom_x','mc_gamma_B_mom_y','mc_gamma_B_mom_z','mc_gamma_B_mom_mag','mc_opening_angle','mc_OMcos','mass','pi_vtx_x','pi_vtx_y','pi_vtx_z','Energy_A','Charge_A','gamma_A_vtx_x','gamma_A_vtx_y','gamma_A_vtx_z','Energy_B','Charge_A','gamma_B_vtx_x','gamma_B_vtx_y','gamma_B_vtx_z','opening_angle','OMcos','IP','conversion_A','conversion_B']

# First find out how many different files we have
def Nshowers_v(df):
    fam = []
    for index, row in df.iterrows():
        d = row['dirnum']
        fi = row['fnum']
        v = int(d)*10000+int(fi)
        fam.append(v)

    #Get the nshowers 
    #first get max values for doubles 
    mult_max = max(col.Counter(fam).values())
    # Solve the nC2 up till n
    nspot=[]
    z=2
    nc2=0
    while nc2 <mult_max:
        nc2 = len([x for x in combinations(np.arange(0,z),2)])
        nspot.append(nc2)
        z +=1
    #print nspot
    # now loop thorugh the famil and put i in 
    nshowers = []
    test = col.Counter(col.Counter(fam).values())
    for m in nspot:
        nshowers.append(test[m])
    #print nshowers
    return nshowers
#######################################################################################################################################################################
#######################################################################################################################################################################
#######################################################################################################################################################################
#######################################################################################################################################################################
fam = []
for index, row in df.iterrows():
    d = row['dirnum']
    fi = row['fnum']
    v = int(d)*10000+int(fi)
    fam.append(v)
print 'total number of files processed:  ', str(len(col.Counter(fam)))

#########################################
##### First show things if proc is unique 
#########################################
df_uni = df.drop_duplicates(subset=['dirnum','fnum'],keep=False) 
print 'size of uni  ' , len(df_uni)
print Nshowers_v(df_uni)

df_dup = df[df.duplicated(['dirnum','fnum'],keep=False)]
print 'size of dup  ' , len(df_dup)
print Nshowers_v(df_dup)

#fail modes 
# -1 ==> Dalitz
# -2 ==> Bad File 
# -3 ==> N Space points too large 
# -4 ==> For now : Nshowers < 2 
# -5 ==> Nshowers == 0
fail_list = np.zeros(4)
for index, row in df_uni.iterrows():
    # lets break things up into what failure mode
    if row['mc_pi_vtx_x']==-1:
        fail_list[0] +=1
    if row['mc_pi_vtx_x']==-2:
        fail_list[1] +=1
    if row['mc_pi_vtx_x']==-3:
        fail_list[2] +=1
    if row['mc_pi_vtx_x']==-4:
        fail_list[3] +=1
print ' this is the fail list '
print fail_list


# Let's look at the 3 Shower case in particular 

#showergroups = [ [-1,-1] for x in range(0,len(df_dup))]
showergroups = [ [index,int(row['dirnum'])*100000 +int(row['fnum'])  ] for index, row in df_dup.iterrows()]
showergroups_sorted = sorted(showergroups,key=itemgetter(1))

shr_gp_idx = []
tmp_gp = []
for i in xrange(0,len(showergroups_sorted)):
    tmp_gp.append(showergroups_sorted[i][0])
    if i==len(showergroups_sorted)-1:
	shr_gp_idx.append(tmp_gp)
	break
    if showergroups_sorted[i][1] != showergroups_sorted[i+1][1]:
	shr_gp_idx.append(tmp_gp)
	tmp_gp = []
    

#print shr_gp_idx 
#


# Now loop over the new grouped list and only look at the 3 shower case

for z in shr_gp_idx:
    #print '============'
    if len(z) == 3:
#	print 'look we have 3'
#	print df_dup.loc[z[0]]['fnum']
#	print df_dup.loc[z[1]]['fnum']
#	print df_dup.loc[z[2]]['fnum']


	ep = [df_dup.loc[z[0]]['Energy_A'],df_dup.loc[z[0]]['Energy_B'],df_dup.loc[z[1]]['Energy_A'],df_dup.loc[z[1]]['Energy_B'],df_dup.loc[z[2]]['Energy_A'],df_dup.loc[z[2]]['Energy_B']]
        sep = sorted(ep)
	lo = sep[0]
	mid = sep[2]
	hi = sep[4]
	

	# This is real shitty
	for s in xrange(0,3):
	    if df_dup.loc[z[s]]['Energy_A'] == hi and df_dup.loc[z[s]]['Energy_B'] == lo:
	        hilo = s
	    if df_dup.loc[z[s]]['Energy_A'] == lo and df_dup.loc[z[s]]['Energy_B'] == hi:
	        hilo = s
	    if df_dup.loc[z[s]]['Energy_A'] == mid and df_dup.loc[z[s]]['Energy_B'] == lo:
	        midlo = s
	    if df_dup.loc[z[s]]['Energy_A'] == lo and df_dup.loc[z[s]]['Energy_B'] == mid:
	        midlo = s
	    if df_dup.loc[z[s]]['Energy_A'] == mid and df_dup.loc[z[s]]['Energy_B'] == hi:
	        midhi = s
	    if df_dup.loc[z[s]]['Energy_A'] == hi and df_dup.loc[z[s]]['Energy_B'] == mid:
	        midhi = s
	# These are the hilo midlo midhi pairs	
#	print ' here is the hi lo'
#	print hilo
#	print ' here is the midlo'
#	print midlo
#	print ' here is the midlo'
#	print midhi
	
	# This get the hi and low A or B for Energy 
	if df_dup.loc[z[hilo]]['Energy_A'] == hi and df_dup.loc[z[hilo]]['Energy_B'] == lo:
	    hi_str = 'A'
	    lo_str = 'B'
	if df_dup.loc[z[hilo]]['Energy_A'] == lo and df_dup.loc[z[hilo]]['Energy_B'] == hi:
	    hi_str = 'B'
	    lo_str = 'A'
	if df_dup.loc[z[midlo]]['Energy_A'] == mid:
	    mid_str = 'A'
	if df_dup.loc[z[midlo]]['Energy_B'] == mid:
	    mid_str = 'B'

#	print 'hi shower', hi_str
#	print 'mid shower', mid_str
#	print 'lo shower', lo_str
	

	##### What to plot?
	# Sorted Energy 
	# Angle Dif 
	# IP
	
	
	##### Largest WRT Smallest
	### Starting for single showers	
#	print 'using format'
#	print df_dup.loc[z[hilo]]['Energy_{}'.format(hi_str)]

	
	
	

	

