import pandas as pd 
import seaborn as sns 
import pylab as plt
import math as math
import numpy as np
from scipy import stats
from scipy.stats import norm



sns.set()

#bring in the data into pandas 

#data = pd.read_csv('../CL_Param_Opt_Photon_third.txt', sep=" ", header = None)
#data = pd.read_csv('../CL_Param_Opt_Photon_OLD.txt', sep=" ", header = None)
data = pd.read_csv('../CL_Param_Opt_Photon.txt', sep=" ", header = None)
data.columns = ['dirnum','fnum','dist_cl','clss','merge_angle','mc_gamma_x','mc_gamma_y','mc_gamma_z','mc_gamma_px','mc_gamma_py','mc_gamma_pz','mc_gamma_p','selected_charge','frac_selected','frac_remaining','angle_dif','num_clutsers']
#data.columns = ['NN_Distance','Min_ForCluser','Charge_Selection_Efficiency','Proccess','NClusters']

#data.drop_duplicates(['dist_cl','merge_angle','frac_selected'])

def charge_to_mev_var(tot,xpos):
    time =  xpos*2.32/256.
    z = time/8.0
    lifetime = pow(math.e,z)
    #recomb = 1./.64
    recomb = 1./.62
    W = 23.6/1000000
    toadc = 0.0013
    eslope = -0.463135096874
    eintercept = 77157.7811293
    tot_WC = tot +eslope*tot + eintercept
    mev = tot_WC* W * recomb * lifetime * toadc
    #mev = 1.2*mev 
    return mev



############################
#### Picking a clsdd########
# Make the master list 
dist_list = [x for x in xrange(6,22,3)]
mergea_list = [x for x in np.arange(0.15,.36,0.1)]
###########################
sel = []
for it in data.index:
    if data['clss'].loc[it]==50:
        sel.append(it)
data_sel = data.loc[sel]
# Now we need to average each of the 
fll = []
for d in dist_list:
    for m in mergea_list:
	#Select these out from the data
	sell = []
	for it in data_sel.index:
	    if data_sel['dist_cl'].loc[it]==d:
		if data_sel['merge_angle'].loc[it]==m:
		    sell.append(it)
	tsel = data.loc[sell]
	avg = tsel['frac_selected'].mean()
	fll.append(avg)
la = [ [fll[x],fll[x+1],fll[x+2]] for x in xrange(0,len(fll)-3,3)]	
la.reverse()
la = np.round(la,3)

ts = np.array(la) 
ax = sns.heatmap(ts,annot=True,fmt=' ')
ax.set_yticklabels(['6','9','12','15','18','21'])
ax.set_xticklabels(['0.15','0.25','0.35'])
ax.set_xlabel('Maximum Merging Angle')
ax.set_ylabel('Maximum Clustering Length')
plt.show()



charge = []
mcenergy = []
xpos = []
adif = []
for index, row in data.iterrows():
    if row['dist_cl'] == 9 and row['clss'] ==50 and row['merge_angle']==0.35:
	charge.append(row['selected_charge'])
	mcenergy.append(row['mc_gamma_p'])
	xpos.append(row['mc_gamma_x'])
	adif.append(row['angle_dif']*180./3.14159265)

energy = [charge_to_mev_var(charge[x],xpos[x]) for x in xrange(0,len(charge))]

#### Make the hist for new energy 

plt.hist((np.asarray(mcenergy) - np.asarray(energy))/np.asarray(mcenergy) , 40, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit((np.asarray(mcenergy) - np.asarray(energy))/np.asarray(mcenergy))
plt.title(r'WC + Clustering Energy Resolution$_c$ :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.xlabel('Resolution',fontsize=16)
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/Photon_clus_energyresolution.png')
plt.show()

plt.hist(np.asarray(adif), 50, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(np.asarray(adif))
plt.title(r'Angular Resolution single photons:  $_c$ :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.xlabel('Degree',fontsize=16)
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/Photon_angle_res.png')
plt.show()









########################################
########################################
########################################
#  Pick some values and fit
########################################

# Using Paramso
p_dl = 12
#p_me = 0.15
#p_cs = 150
#p_dl = 12
p_me = 0.35
p_cs = 50

#Make a df for this
fit = []
for it in data.index:
    if data['clss'].loc[it]== p_cs and data['dist_cl'].loc[it]==p_dl and data['merge_angle'].loc[it]==p_me:
        fit.append(it)
data_fit = data.loc[fit]

sel_ch_avg = data_fit['frac_selected'].mean()
print 'averge fraction selected charge ', str(sel_ch_avg)

##### Looking at the collected charge

# What is the collection resolution for this... true - sele / true
fsel = np.array(data_fit.frac_selected )
plt.hist(fsel, 20, facecolor='blue', alpha=0.75)
plt.title('Fraction of Clustered charge for : CL = 9cm and MA = 0.3')
plt.xlabel(r'$Q_{clust}/Q_{reco}$')
plt.show()
## is this depentend on things...
xpos = np.array(data_fit.mc_gamma_x)
ypos = np.array(data_fit.mc_gamma_y)
zpos = np.array(data_fit.mc_gamma_z)
mce = np.array(data_fit.mc_gamma_p)
sel_charge = np.array(data_fit.selected_charge)



# See how things look for above and below 90% clusters
sns.jointplot(mce, fsel)
plt.show()
sns.jointplot(mce, fsel, kind="hex")
plt.show()
sns.jointplot(sel_charge, fsel, kind="hex")
plt.show()


sns.jointplot(fsel, ypos)
plt.show()
sns.jointplot(fsel, zpos)
plt.show()






#Now we are going to need to fit the collected charge as a function of Energy 
# First a general fit... Then a fit based on collected charge

t_Energy = np.array(data_fit.mc_gamma_p)
sel_charge = np.array(data_fit.selected_charge)

print 'Number of entries in the fit', str(len(sel_charge))
print 'Number of entries in the fit', str(len(fit))
eslope, eintercept, er_value, ep_value, estd_err = stats.linregress(sel_charge,t_Energy)
print 'ENERGY FIT', eslope,'  intercept ',eintercept



#plt.scatter(sel_charge,t_Energy)
plt.show()






print data.size








# Plot of effiency 
sns.jointplot('dist_cl','frac_selected' ,data=data,kind="kde",space=0, color="#4CB391")
#sns.jointplot(data['dist_cl'],data['frac_selected'] , kind="hex", stat_func=kendalltau, color="#4CB391")

plt.show()

sns.jointplot('dist_cl','frac_selected' ,data=data,space=0, color="#4CB391")
plt.show()

sns.jointplot('angle_dif','frac_selected' ,data=data,space=0, color="#4CB391")
plt.show()

sns.jointplot('merge_angle','frac_selected' ,data=data,space=0,kind='kde', color="#4CB391")
plt.show()

sns.jointplot('dist_cl','angle_dif' ,data=data,space=0, color="#4CB391")
plt.show()


sel = []
for it in data.index:
    if data['angle_dif'].loc[it]< 1:
        sel.append(it)

df_sel = data.loc[sel]

mass_ars = df_sel.angle_dif
n, bins, patches = plt.hist(mass_ars, 20, facecolor='blue', alpha=0.75)
#n, bins, patches = plt.hist(mass_ar, 35, normed=1, facecolor='blue', alpha=0.75)
#(mu, sigma) = norm.fit(mass_ars)
plt.title('angle dif')
#plt.title(r'$\mathrm{(True-Reco) / True:}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()

sns.lmplot(x="selected_charge", y="mc_gamma_p", hue="dist_cl", data=data, size=10)
plt.show()


