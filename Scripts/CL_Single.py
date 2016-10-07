import pandas as pd 
import seaborn as sns 
import pylab as plt
import numpy as np
import math as math
from scipy import stats
from scipy.stats import norm



sns.set()

#bring in the data into pandas 

data = pd.read_csv('../CL_Param_Opt_Photon_Single.txt', sep=" ", header = None)
data.columns = ['dirnum','fnum','dist_cl','clss','merge_angle','mc_gamma_x','mc_gamma_y','mc_gamma_z','mc_gamma_px','mc_gamma_py','mc_gamma_pz','mc_gamma_p','dep_charge','selected_charge','frac_selected','frac_remaining','angle_dif','num_clutsers']

def charge_to_mev(tot):
    lifetime = 1.16
    recomb = 1./.62
    W = 23.6/1000000
    toadc = 0.0011
    mev = tot* W * recomb * lifetime * toadc
    #mev = 1.2*mev 
    return mev

def charge_to_mev_var(tot,xpos):
    #rough convert to time 
    time =  xpos*2.32/256.
    z = time/8.0
    lifetime = pow(math.e,z)
    recomb = 1./.62
    W = 23.6/1000000
    toadc = 0.0011
    mev = tot* W * recomb * lifetime * toadc
    return mev

##### First Plot the total wirecell charge vs the deposit charge
total_charge = []
sel_charge = []
dep_charge = []
res_charge = []
tr_energy = []
dep_res_charge = []
x_pos = []
y_pos = []
z_pos = []
for index, row in data.iterrows():
    tc = row['selected_charge']/row['frac_selected']
    sc = row['selected_charge']
    dc = row['dep_charge']
    tre = row['mc_gamma_p']
    x = row['mc_gamma_x']
    y = row['mc_gamma_y']
    z = row['mc_gamma_z']
    if dc<100000:
	continue
    rc = (tc-sc)/tc
    dr = (dc-tc)/dc
    total_charge.append(tc)
    sel_charge.append(sc)
    dep_charge.append(dc)
    res_charge.append(rc)
    dep_res_charge.append(dr)
    tr_energy.append(tre)
    x_pos.append(x)
    y_pos.append(y)
    z_pos.append(z)


#######
#First let's check out the  the total wirecell charge collection vrs the total deposit
#######
plt.scatter(total_charge,dep_charge)
plt.title('Reconstructed Charge vs True Deposit Charge')
plt.xlabel(r'Q$_{reco}$',fontsize=18)
plt.ylabel(r'Q$_{dep}$',fontsize=18)
plt.xlim([0,40000000])
plt.ylim([0,20000000])
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/Reco_True_DepCharge.png')
plt.show()


# There is an ofset... let's fix that for WC 
eslope, eintercept, er_value, ep_value, estd_err = stats.linregress(np.asarray(total_charge),np.asarray(dep_charge) - np.asarray(total_charge))
print 'ENERGY FIT', eslope,'  intercept ',eintercept

# now lets try to fit the charge for WC and see what we get 
total_charge_fit = [ x +eslope*x + eintercept for x in total_charge]
energy_charge = [ charge_to_mev_var(total_charge[x] +eslope*total_charge[x] + eintercept,x_pos[x]) for x in xrange(0,len(total_charge))]
old_energy_charge = [ charge_to_mev(total_charge[x] +eslope*total_charge[x] + eintercept) for x in xrange(0,len(total_charge))]

#######
# Look at resolution
#######
plt.hist((np.asarray(dep_charge) - np.asarray(total_charge_fit))/np.asarray(dep_charge) , 60, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit((np.asarray(dep_charge) -np.asarray(total_charge_fit)) /np.asarray(dep_charge) )
plt.title(r'WC Charge Resolution$_c$ :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.xlim([-0.3,.3])
plt.xlabel('Resolution',fontsize=16)
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/charge_resolution.png')
plt.show()

#######
# Look at energy resolution
#######
plt.hist((np.asarray(tr_energy)- np.asarray(energy_charge))/np.asarray(tr_energy), 60, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit((np.asarray(tr_energy)- np.asarray(energy_charge))/np.asarray(tr_energy))
plt.title(r'WC Energy Resolution$_c$ :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.xlim([-0.1,1])
plt.xlabel('Resolution',fontsize=16)
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/energy_resolution.png')
plt.show()

#######
# Look at OLD energy resolution
#######
plt.hist((np.asarray(tr_energy)- np.asarray(old_energy_charge))/np.asarray(tr_energy), 60, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit((np.asarray(tr_energy)- np.asarray(old_energy_charge))/np.asarray(tr_energy))
plt.title(r'WC OLD Energy Resolution$_c$ :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.xlim([-0.1,1])
plt.xlabel('Resolution',fontsize=16)
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/old_energy_resolution.png')
plt.show()



#######
# Look at resolution vs x
#######
plt.scatter((np.asarray(tr_energy)- np.asarray(energy_charge))/np.asarray(tr_energy),np.asarray(x_pos) )
plt.title('Energy Resolution vs X-pos')
plt.xlabel('Resolution',fontsize=18)
plt.ylabel('X-Position(cm)',fontsize=18)
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/energyres_x.png')
plt.show()

#######
# Look at resolution OLD vs x
#######
plt.scatter((np.asarray(tr_energy)- np.asarray(old_energy_charge))/np.asarray(tr_energy),np.asarray(x_pos) )
plt.title('Energy Resolution(avg lifetime) vs X-pos')
plt.xlabel('Resolution',fontsize=18)
plt.ylabel('X-Position(cm)',fontsize=18)
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/oldenergyres_x.png')
plt.show()

#######
# Look at resolution vs y
#######
plt.scatter((np.asarray(tr_energy)- np.asarray(energy_charge))/np.asarray(tr_energy),np.asarray(y_pos) )
plt.title('Energy Resolution vs Y-pos')
plt.xlabel('Resolution',fontsize=18)
plt.ylabel('Y-Position(cm)',fontsize=18)
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/energyres_y.png')
plt.show()

#######
# Look at resolution OLD vs y
#######
plt.scatter((np.asarray(tr_energy)- np.asarray(old_energy_charge))/np.asarray(tr_energy),np.asarray(y_pos) )
plt.title('Energy Resolution(avg lifetime) vs Y-pos')
plt.xlabel('Resolution',fontsize=18)
plt.ylabel('Y-Position(cm)',fontsize=18)
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/oldenergyres_y.png')
plt.show()

#######
# Look at resolution vs Z
#######
plt.scatter((np.asarray(tr_energy)- np.asarray(energy_charge))/np.asarray(tr_energy),np.asarray(y_pos) )
plt.title('Energy Resolution vs Z-pos')
plt.xlabel('Resolution',fontsize=18)
plt.ylabel('Z-Position(cm)',fontsize=18)
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/energyres_z.png')
plt.show()

#######
# Look at resolution OLD vs z
#######
plt.scatter((np.asarray(tr_energy)- np.asarray(old_energy_charge))/np.asarray(tr_energy),np.asarray(z_pos) )
plt.title('Energy Resolution(avg lifetime) vs Z-pos')
plt.xlabel('Resolution',fontsize=18)
plt.ylabel('z-Position(cm)',fontsize=18)
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/oldenergyres_z.png')
plt.show()


#### Now plot the good and bad resolution
#### Look at the hi and lo res


res = (np.asarray(tr_energy)- np.asarray(energy_charge))/np.asarray(tr_energy)
hi_idx = []
lo_idx = []
hi_x = []
hi_y = []
hi_z = []
lo_x = []
lo_y = []
lo_z = []
for a in xrange(0,len(res)):
    if res[a] >0.3:
        hi_idx.append(a)
	hi_x.append(x_pos[a])
	hi_y.append(y_pos[a])
	hi_z.append(z_pos[a])
    if res[a] <0.3:
        lo_idx.append(a)
	lo_x.append(x_pos[a])
	lo_y.append(y_pos[a])
	lo_z.append(z_pos[a])

#Sort based on res
xylo = sns.jointplot(np.asarray(lo_x),np.asarray(lo_y),stat_func=None, space=0, color="g")
xylo.set_axis_labels("x-position", "y-position")
plt.title('xy-position for Good Resolution ')
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/escape_lo_xy.png')
plt.show()

xyhi = sns.jointplot(np.asarray(hi_x),np.asarray(hi_y), stat_func=None,space=0, color="g")
xyhi.set_axis_labels("x-position", "y-position")
plt.title('xy-position for Poor Resolution ')
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/escape_hi_xy.png')
plt.show()

xzlo = sns.jointplot(np.asarray(lo_x),np.asarray(lo_z),stat_func=None, space=0, color="g")
xzlo.set_axis_labels("x-position", "z-position")
plt.title('xz-position for Good Resolution ')
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/escape_lo_xz.png')
plt.show()

xzhi = sns.jointplot(np.asarray(hi_x),np.asarray(hi_z), stat_func=None,space=0, color="g")
xzhi.set_axis_labels("x-position", "z-position")
plt.title('xz-position for Poor Resolution ')
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/escape_hi_xz.png')
plt.show()

yzlo = sns.jointplot(np.asarray(lo_y),np.asarray(lo_z),stat_func=None, space=0, color="g")
yzlo.set_axis_labels("y-position", "z-position")
plt.title('yz-position for Good Resolution ')
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/escape_lo_yz.png')
plt.show()

yzhi = sns.jointplot(np.asarray(hi_y),np.asarray(hi_z), stat_func=None,space=0, color="g")
yzhi.set_axis_labels("y-position", "z-position")
plt.title('yz-position for Poor Resolution ')
plt.savefig('/home/ryan/Documents/WireCell/10_3_16/escape_hi_yz.png')
plt.show()



















######################################################################################
######################################################################################
plt.scatter((np.asarray(tr_energy)- np.asarray(energy_charge))/np.asarray(tr_energy),np.asarray(y_pos) )
plt.title('energy resolution vs Y pos')
plt.show()
plt.scatter((np.asarray(tr_energy)- np.asarray(energy_charge))/np.asarray(tr_energy),np.asarray(z_pos) )
plt.title('energy resolution vs Z pos')
plt.show()





plt.scatter(sel_charge,total_charge)
plt.title('selected charge vs wc Charge')
plt.show()

plt.hist(res_charge, 20, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(res_charge)
plt.title(r'chargeresolution :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()


plt.hist(data.frac_selected, 20, facecolor='blue', alpha=0.75)
plt.title('fraction of selected charge')
plt.show()



#### Working with energy
plt.scatter(energy_charge,tr_energy)
plt.title('recoenergy vs true energy')
plt.show()


