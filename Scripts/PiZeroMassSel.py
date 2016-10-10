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
    df = pd.read_csv('../Out_text/PiZero_Selection_Params_Cleaned.txt', sep=" ", header = None)
else:
    df = pd.read_csv('{}'.format(sys.argv[2]), sep=" ", header = None)
   
df.columns = ['dirnum','fnum','dalitz','mc_pi_vtx_x','mc_pi_vtx_y','mc_pi_vtx_z','mc_pi_mom_x','mc_pi_mom_y','mc_pi_mom_z','mc_pi_mom_mag','mc_gamma_A_vtx_x','mc_gamma_A_vtx_y','mc_gamma_A_vtx_z','mc_gamma_A_mom_x','mc_gamma_A_mom_y','mc_gamma_A_mom_z','mc_gamma_A_mom_mag','mc_gamma_B_vtx_x','mc_gamma_B_vtx_y','mc_gamma_B_vtx_z','mc_gamma_B_mom_x','mc_gamma_B_mom_y','mc_gamma_B_mom_z','mc_gamma_B_mom_mag','mc_opening_angle','mc_OMcos','mass','pi_vtx_x','pi_vtx_y','pi_vtx_z','Energy_A','gamma_A_vtx_x','gamma_A_vtx_y','gamma_A_vtx_z','Energy_B','gamma_B_vtx_x','gamma_B_vtx_y','gamma_B_vtx_z','opening_angle','OMcos','IP','conversion_A','conversion_B']

# First find out how many different files we have
fam = []
for index, row in df.iterrows():
    d = row['dirnum']
    fi = row['fnum']
    v = int(d)*10000+int(fi)
    fam.append(v)

print len(fam)
print 'total number of files processed'
print len(col.Counter(fam))

#Get the nshowers 
#first get max values for doubles 
mult_max = max(col.Counter(fam).values())
# Solve the nC2 up till n
nspot=[]
z=2
nc2=0
while nc2 <mult_max:
    nc2 = len([x for x in combinations(np.arange(1,z),2)])
    nspot.append(nc2)
    z +=1
print nspot
# now loop thorugh the famil and put i in 
nshowers = []
test = col.Counter(col.Counter(fam).values())
for m in nspot:
    nshowers.append(test[m])
print nshowers

#



#########################################
##### First show things if proc is unique 
#########################################
df_uni = df.drop_duplicates(subset=['dirnum','fnum'],keep=False) 
print 'size of uni  ' , len(df_uni)

df_dup = df[df.duplicated(['dirnum','fnum'],keep=False)]
print 'size of dup  ' , len(df_dup)

'''
df_dub = pd.concat([df,df_uni])
df_gpby = df.groupby(list(df_dub.columns))
idx = [x[0] for x in df_gpby.indices.values() if len(x) == 1]
df_dup = df_dub.iloc[idx]
print 'size of dup  ' , len(df_dup)
'''

#Here Plot some things 
#First we want to look at True - reco for angle... we really want that to be the best we can.
#First we don't worry about charge mixing  
####################
# Things I need
####################
mc_roa_y = df_uni.mc_opening_angle - df_uni.opening_angle 
roa_x = df_uni.opening_angle 
mc_roa_x = df_uni.mc_opening_angle 

####################
#Make the ploting variable for the mc-diff
####################
#Plot a histogram of the angular diferance
n, bins, patches = plt.hist(mc_roa_y, 20, facecolor='blue', alpha=0.75)
#df_uni.hist(ax=axes[0], alpha=0.9, color='blue')
(mu, sigma) = norm.fit(mc_roa_y)
plt.title(r'True opening angle-Reco opening angle :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()

#### But wait... Hhere is all this spread coming from
plt.scatter(roa_x,mc_roa_y)
plt.title('Difference in Opening Angle vs Reco Opening Angle')
plt.xlabel('RecoOpeningAngle (Rads)')
plt.show()

# What is the True spread coming from 
##### Oh... we have problems with large and small angles... 
# Is there problems anywhere else? 
plt.scatter(mc_roa_x,mc_roa_y)
plt.title('Difference in Opening Angle vs Reco Opening Angle')
plt.xlabel('RecoOpeningAngle (Rads)')
plt.show()

# CheCK IP
rIP = df_uni.IP
plt.scatter(rIP,mc_roa_y)
plt.title('Difference in Opening Angle vs IP')
plt.ylabel('MCOpeningAngle (Rads)')
plt.xlabel('IP')
plt.show()

##### OK.... Now we need to try to look at energy of things 
# We are going to need to correct the energy as a function of charge and as a fucntion of drift 
#First we are going to have to correct for the charge... 
def charge_to_mev(tot,xpos):
    time =  xpos*2.32/256.
    z = time/8.0
    lifetime = pow(math.e,z)
    recomb = 1./.62
    W = 23.6/1000000
    toadc = 0.0013
    #toadc = 0.00077
    eslope = -0.463135096874
    eintercept = 77157.7811293
    tot_WC = tot +eslope*tot + eintercept
    mev = tot_WC* W * recomb * lifetime * toadc
    mev = 1.2*mev 
    return mev



# so this will be for tot charge.... 
# Then we need to correct for cluster eff 

def soft_energy(mev): 
    MeV = mev * (1.0) 
    return MeV

##########
### Nope... so let's just make the anlge cut there everyone will make 
# But we have to make on cut on large angle too... 
#Lets do that and see what we are left with. 




lo_angle = .25
hi_angle = 1.8
min_esum = 135.
min_energy = 40.
max_asym = 0.9
## Magic cuts

'''
## Real magic

lo_angle = .35
hi_angle = 1.7
#hi_angle = 1.5
#hi_angle = 2.0
min_esum = 135.
min_energy = 40.
#max_asym = 1.9
max_asym = 0.9
## Magic cuts


###
lo_angle = .35
hi_angle = 1.7
min_esum = 100.
min_energy = 30.
max_asym = 0.9


'''
##
#############################################
print 'state work'
ss = []
for it in df.index: 
    mevA = charge_to_mev(df['Energy_A'].loc[it],df['gamma_A_vtx_x'].loc[it])
    MeVA = soft_energy(mevA)
    mevB = charge_to_mev(df['Energy_B'].loc[it],df['gamma_B_vtx_x'].loc[it])
    MeVB = soft_energy(mevB)
    esum = mevA+mevB
    asym = math.fabs((mevA-mevB)/(mevA+mevB))
    #if asym<max_asym and esum>min_esum:
    if esum>min_esum and asym<max_asym and MeVA>min_energy and MeVB>min_energy :
    #if esum>min_esum and asym<max_asym and MeVA>min_energy and MeVB>min_energy and df['opening_angle'].loc[it]<hi_angle and df['opening_angle'].loc[it]>lo_angle:
    #if df['opening_angle'].loc[it]<hi_angle and df['opening_angle'].loc[it]>lo_angle:
    #if df['opening_angle'].loc[it]<hi_angle and df['opening_angle'].loc[it]>lo_angle and esum>min_esum :
    #if df['opening_angle'].loc[it]<hi_angle and df['opening_angle'].loc[it]>lo_angle and asym<max_asym:
    #if df['opening_angle'].loc[it]<hi_angle and df['opening_angle'].loc[it]>lo_angle and esum>min_esum and asym<max_asym and MeVA>min_energy and MeVB>min_energy:
    #if df['opening_angle'].loc[it]<hi_angle and df['opening_angle'].loc[it]>lo_angle and esum>min_esum and asym<max_asym:
    #if df['opening_angle'].loc[it]<hi_angle and df['opening_angle'].loc[it]>lo_angle and esum>min_esum:
    #if df['opening_angle'].loc[it]<hi_angle and df['opening_angle'].loc[it]>lo_angle:
	ss.append(it)

newdf = df.loc[ss]
df_sel = newdf.drop_duplicates(subset=['dirnum','fnum'])
print 'working size  of uni  ' , len(df_sel)

#############################################
# Ok... well now lets look at opening angle resolution
# So first this will go in as an angle... but really it's in a cosine... so we have to be carful 
# repeate from before
mc_roa_y = np.asarray(df_sel.mc_opening_angle) - np.asarray(df_sel.opening_angle)
roa_x = np.asarray(df_sel.opening_angle)
radl_A = np.asarray(df_sel.conversion_A)
radl_B = np.asarray(df_sel.conversion_B)
radl_AB = np.concatenate([radl_A,radl_B])
#Plot a histogram of the angular diferance

### 

n, bins, patches = plt.hist(mc_roa_y, 20, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(mc_roa_y)
plt.title(r'True opening angle-Reco opening angle :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()

#### But wait... Hhere is all this spread cossss from
plt.scatter(roa_x,mc_roa_y)
plt.title('Difference in Opening Angle vs Reco Opening Angle')
plt.xlabel('RecoOpeningAngle (Rads)')
plt.ylabel('OpeningAnlge difference (Rads)')
#plt.savefig('/home/ryan/Documents/WireCell/10_3_16/pi0_angledif_vs_recoangle.png')
plt.show()

##### Oh... we have problems with large and small angles... 
# Is there problems anywhere else? 

# CheCK IP
rIP = df_sel.IP
plt.scatter(rIP,mc_roa_y)
plt.title('Difference in Opening Angle vs IP')
plt.ylabel('OpeningAnlge difference (Rads)')
plt.xlabel('IP')
#plt.savefig('/home/ryan/Documents/WireCell/10_3_16/pi0_angledif_vs_ip.png')
plt.show()


# Now for OMC
#Plot a histogram of the angular diferance
n, bins, patches = plt.hist(radl_AB, 20, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(radl_AB)
plt.title(r'Photon Conversion length :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.xlabel('Length(cm)')
plt.show()


# Now for OMC
mcr_omc_sel = np.sqrt(np.asarray(df_sel.mc_OMcos)) - np.sqrt(np.asarray(df_sel.OMcos))
#Plot a histogram of the angular diferance
n, bins, patches = plt.hist(mcr_omc_sel, 20, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(mcr_omc_sel)
plt.title(r'SELECTED True OMC - reco OMC :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()


e_a= []
e_b= []
omc= []

mce_a= []
mce_b= []
mcomc= []
for index, row in df_sel.iterrows():
    mevA = charge_to_mev(row['Energy_A'],row['gamma_A_vtx_x'])
    MeVA = soft_energy(mevA)
    e_a.append(MeVA)
    mevB = charge_to_mev(row['Energy_B'],row['gamma_B_vtx_x'])
    MeVB = soft_energy(mevB)
    e_b.append(MeVB)
    Omc = row['OMcos']
    omc.append(Omc)
    mce_a.append(row['mc_gamma_A_mom_mag'])
    mce_b.append(row['mc_gamma_B_mom_mag'])
    mcomc.append(row['mc_OMcos'])


###### Now first lets look at the resolution for sqrt(EE)
# Working in numpy arrays 
E_A = np.asarray(e_a)
E_B = np.asarray(e_b)
OMC = np.asarray(omc)
MCE_A = np.asarray(mce_a)
MCE_B = np.asarray(mce_b)
MCOMC = np.asarray(mcomc)

#print E_B

mcr_ee_y = np.sqrt(np.asarray(df_sel.mc_gamma_A_mom_mag)* np.asarray(df_sel.mc_gamma_B_mom_mag))*1000 
mcr_ee_sdf =  np.sqrt(E_A*E_B)
#mcr_ee_y = np.sqrt(df_uni.mc_gamma_A_mom_mag* df_uni.mc_gamma_B_mom_mag)*1000 - np.sqrt(E_A*E_B)
mcr_ee_y_res = (np.sqrt(np.asarray(df_sel.mc_gamma_A_mom_mag)* np.asarray(df_sel.mc_gamma_B_mom_mag))*1000 - np.sqrt(E_A*E_B))/(np.sqrt(np.asarray(df_sel.mc_gamma_A_mom_mag)* np.asarray(df_sel.mc_gamma_B_mom_mag))*1000)

#Lets look hot the sqrt ee resolution
n, bins, patches = plt.hist(mcr_ee_y_res, 20, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(mcr_ee_y_res)
plt.title(r'sqrt(EE) resolution :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()

# How does this look as a function of EA or EB
plt.scatter(E_A+E_B,MCE_A+MCE_B)
plt.title('MC EA+EB vs EA+EB')
plt.xlabel('Reco EA+EB (MeV)')
plt.ylabel('Truth EA+EB (MeV)')

plt.show()

#
# How does this look as a function of EA or EB
plt.scatter(mcr_ee_sdf,mcr_ee_y)
plt.title('truth vs eaEB')
plt.xlabel('EAeb ( MeV )')
plt.show()

# How does this look as a function of EA or EB
aasy = (E_A - E_B)/(E_A +E_B)
asy = np.sqrt(aasy*aasy)
plt.scatter(asy,mcr_ee_y_res)
plt.title('E1E2 Resolution vs Energy Asymetery ')
plt.xlabel('asym')
plt.ylabel('E1E2 Resolution')
plt.show()



# How does this look as a function of EA or EB
plt.scatter(E_A,mcr_ee_y_res)
plt.title('sqrt(EE) Res vs EA')
plt.xlabel('EA ( MeV )')
plt.show()


plt.scatter(E_B,mcr_ee_y_res)
plt.title('sqrt(EE) Res vs EB')
plt.xlabel('EB ( MeV )')
plt.show()

# About the sum 
plt.scatter(E_A+E_B,mcr_ee_y_res)
plt.title('E1E2 Resolution vs Total deposit energy (E1+E2) ')
plt.xlabel('EA+EB ( MeV )')
plt.ylabel('E1E2 Resolution')
plt.show()








######
## ok... make a mass

nmass =  np.sqrt(2.*E_A*E_B*OMC)
rmass = [x for x in nmass if x<400]

n, bins, patches = plt.hist(rmass, 30, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(rmass)
plt.title(r' mass :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
#plt.savefig('/home/ryan/Documents/WireCell/10_3_16/pi0_mass.png')
plt.xlabel(' Mass (MeV)')
plt.ylabel(' Events / 12 MeV')
plt.show()

nmcErOmass =  np.sqrt(2.*MCE_A*MCE_B*OMC)*1000
mcErOmass = [x for x in nmcErOmass if x<400]
nrEmcOmass =  np.sqrt(2.*E_A*E_B*MCOMC)
rEmcOmass = [x for x in nrEmcOmass if x<400]

n, bins, patches = plt.hist(mcErOmass, 34, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(mcErOmass)
plt.title(r'mc Energy Reco OMC mass!! :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
#plt.savefig('/home/ryan/Documents/WireCell/10_3_16/pi0_massMCEnergy.png')
plt.xlabel(' Mass (MeV)')
plt.ylabel(' Events / 12 MeV')
plt.show()

n, bins, patches = plt.hist(rEmcOmass, 34, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(rEmcOmass)
plt.title(r'reco Energy mc OMC mass!! :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
#plt.savefig('/home/ryan/Documents/WireCell/10_3_16/pi0_massMCAngle.png')
plt.xlabel(' Mass (MeV)')
plt.ylabel(' Events / 12 MeV')
plt.show()


n, bins, patches = plt.hist([rmass,mcErOmass,rEmcOmass], 40, alpha=0.75,histtype='bar')
plt.title('reco Energy mc OMC mass')
#plt.savefig('/home/ryan/Documents/WireCell/10_3_16/pi0_massMCAngle.png')
plt.xlabel(' Mass (MeV)')
plt.ylabel(' Events / 12 MeV')
plt.show()












####################
#  Opening angle 
####################
sns.lmplot(x='mc_opening_angle',y='opening_angle',data=df_uni)
plt.show()
#Make the ploting variables
mc_roa_y = df_uni.mc_opening_angle - df_uni.opening_angle 
roa_x = df_uni.opening_angle 
#Plot a histogram of the angular diferance
n, bins, patches = plt.hist(mc_roa_y, 20, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(mc_roa_y)
#plt.title(r'True opening angle-Reco opening angle : \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.title(r'True opening angle-Reco opening angle :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()

plt.scatter(roa_x,mc_roa_y)
plt.title('Difference in Opening Angle vs Reco Opening Angle')
plt.xlabel('RecoOpeningAngle (Rads)')
plt.show()

mc_roa_x = df_uni.mc_opening_angle 
plt.scatter(mc_roa_x,mc_roa_y)
plt.title('Difference in Opening Angle vs Truth Opening Angle')
plt.xlabel('MCOpeningAngle (Rads)')
plt.show()

#
r_sume = df_uni.Energy_B +df_uni.Energy_A  
plt.scatter(r_sume,mc_roa_y)
plt.title('Difference in Opening Angle vs sum of energy')
plt.ylabel('MCOpeningAngle (Rads)')
plt.xlabel('sum of E')
plt.show()


# IP
rIP = df_uni.IP
plt.scatter(rIP,mc_roa_y)
plt.title('Difference in Opening Angle vs IP')
plt.ylabel('MCOpeningAngle (Rads)')
plt.xlabel('IP')
plt.show()











############ STOP 
############ STOP 
############ STOP 
############ STOP 























###################
# Make some simple cuts to handle resolution and keep track of eff

cut = []
for it in df_uni.index:
    if df_uni['opening_angle'].loc[it]<2.0 and df_uni['opening_angle'].loc[it]>.35:
        cut.append(it)
df_sel = df_uni.loc[cut]

mc_roa_y_sel = df_sel.mc_opening_angle - df_sel.opening_angle 
roa_x_sel = df_sel.opening_angle 
#Plot a histogram of the angular diferance
n, bins, patches = plt.hist(mc_roa_y_sel, 20, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(mc_roa_y_sel)
#plt.title(r'True opening angle-Reco opening angle : \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.title(r'SELECTED True opening angle-Reco opening angle :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()

# Now for OMC
mcr_omc_sel = np.sqrt(df_sel.mc_OMcos) - np.sqrt(df_sel.OMcos)
#Plot a histogram of the angular diferance
n, bins, patches = plt.hist(mcr_omc_sel, 20, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(mcr_omc_sel)
#plt.title(r'True opening angle-Reco opening angle : \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.title(r'SELECTED True OMC - reco OMC :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()


print 'how many events we have', str(len(df_sel) )
#CHeck whats left
rIP = df_sel.IP
plt.scatter(rIP,mc_roa_y_sel)
plt.title('from selDifference in Opening Angle vs IP')
plt.ylabel('MCOpeningAngle (Rads)')
plt.xlabel('IP')
plt.show()








#########################################################################
# Next look at the dups and see what we get form the simple angle cut 
#########################################################################

cut = []
for it in df_dup.index:
    if df_dup['opening_angle'].loc[it]<2.0 and df_dup['opening_angle'].loc[it]>.35:
        cut.append(it)
df_dup_sel = df_dup.loc[cut]

# Now see how many unique we have 
#########################################
df_dupcut_uni = df_dup_sel.drop_duplicates(subset=['dirnum','fnum'])
print 'size of cut dups to uni  ' , len(df_dupcut_uni)


### Now see what we have from uni
mc_roa_y_dup = df_dupcut_uni.mc_opening_angle - df_dupcut_uni.opening_angle 
roa_x_dup = df_dupcut_uni.opening_angle 
#Plot a histogram of the angular diferance
n, bins, patches = plt.hist(mc_roa_y_dup, 20, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(mc_roa_y_dup)
#plt.title(r'True opening angle-Reco opening angle : \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.title(r'SELECTED DUP True opening angle-Reco opening angle :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()


# Now for OMC
mcr_omc_dup = np.sqrt(df_dupcut_uni.mc_OMcos) - np.sqrt(df_dupcut_uni.OMcos)
#Plot a histogram of the angular diferance
n, bins, patches = plt.hist(mcr_omc_dup, 20, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(mcr_omc_dup)
#plt.title(r'True opening angle-Reco opening angle : \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.title(r'SELECTED dup True OMC - reco OMC :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()






























####################
#  Sqrt(EE) 
####################
mc_ree_y = np.sqrt(df_uni.mc_gamma_A_mom_mag* df_uni.mc_gamma_B_mom_mag)*1000 - np.sqrt(df_uni.Energy_A*df_uni.Energy_B) 
ree_x = np.sqrt(df_uni.Energy_A*df_uni.Energy_B)
mc_ree_x = np.sqrt(df_uni.mc_gamma_A_mom_mag* df_uni.mc_gamma_B_mom_mag)*1000
EA = df_uni.Energy_A
EB = df_uni.Energy_B

#Plot a histogram of the energy diferance
n, bins, patches = plt.hist(mc_ree_y, 20, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(mc_ree_y)
#plt.title(r'True opening angle-Reco opening angle : \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.title(r'True sqrt(EE)-Reco sqrt(EE) :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()


plt.scatter(ree_x,mc_ree_y)
plt.title('Difference in  sqrt(EE) vs Reco sqrt(EE)')
plt.xlabel('MeV')
plt.show()

plt.scatter(mc_ree_x,mc_ree_y)
plt.title('Difference in  sqrt(EE) vs MC sqrt(EE)')
plt.xlabel('MeV')
plt.show()


plt.scatter(EA,mc_ree_y)
plt.title('Difference in  sqrt(EE) vs Shower EnergyA')
plt.xlabel('MeV')
plt.show()

plt.scatter(EB,mc_ree_y)
plt.title('Difference in  sqrt(EE) vs Shower EnergyB')
plt.xlabel('MeV')
plt.show()

###################




####################
#  UniMass 
####################
mass_r = np.sqrt(2*df_uni.Energy_A*df_uni.Energy_B*df_uni.OMcos)
n, bins, patches = plt.hist(mass_r, 20, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(mass_r)
plt.title(r'RecoMass :$\mathrm{} \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()


###################



####################
#  UniMass  Selected
####################



###################





sel = []
for it in df_uni.index:
    if df_uni['OMcos'].loc[it]> 0.2:
	sel.append(it)

print 'SEL length ', str(len(sel))
df_sel = df_uni.loc[sel]
fig4 = plt.figure()
#mass_ars = np.sqrt(2.*df_sel.Energy_A*df_sel.Energy_B*(df_sel.mc_OMcos))
mass_ars = np.sqrt(2.*df_uni.Energy_A*df_uni.Energy_B*(df_uni.OMcos))
n, bins, patches = plt.hist(mass_ars, 20, facecolor='blue', alpha=0.75)
#n, bins, patches = plt.hist(mass_ar, 35, normed=1, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(mass_ars)
plt.title(r'$\mathrm{(True-Reco) / True:}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()




#Plot the mass WORKING HERE

plt.scatter(np.sqrt(df_uni.Energy_A*df_uni.Energy_B),np.sqrt(df_uni.mc_gamma_A_mom_mag*df_uni.mc_gamma_B_mom_mag)*1000. )
plt.title('Reconstructed vs true sqrt(EE)')
plt.xlabel('Reconstructed sqrt(EE)')
plt.ylabel('True sqrt(EE)')
plt.show()
# Make a hist of thi
sed = (np.sqrt(df_uni.mc_gamma_A_mom_mag*df_uni.mc_gamma_B_mom_mag)*1000. -np.sqrt(df_uni.Energy_A*df_uni.Energy_B*1.25))/(np.sqrt(df_uni.mc_gamma_A_mom_mag*df_uni.mc_gamma_B_mom_mag)*1000.)
n, bins, patches = plt.hist(sed, 18, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(sed)
plt.title(r'$\mathrm{(True-Reco)}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()


un_EE = sns.jointplot(np.sqrt(df_uni.Energy_A*df_uni.Energy_B), np.sqrt(df_uni.mc_gamma_A_mom_mag*df_uni.mc_gamma_B_mom_mag)*1000. )
un_EE.set_axis_labels('Reconstructed sqrt(EE)','Truth sqrt(EE)')
plt.show()

un_OMC = sns.jointplot(np.sqrt(df_uni.OMcos), np.sqrt(df_uni.mc_OMcos))
un_OMC.set_axis_labels('Reconstructed sqrt(1-cos)','Truth sqrt(1-cos)')
plt.show()

un_OMCr = sns.jointplot( df_uni.opening_angle*180./np.pi, df_uni.mc_opening_angle*180./np.pi -df_uni.opening_angle*180./np.pi )
#un_OMCr = sns.jointplot(np.sqrt(df_uni.mc_opening_angle*180./np.pi) -np.sqrt( df_uni.opening_angle*180./np.pi), np.sqrt(df_uni.opening_angle*180./np.pi))
un_OMCr.set_axis_labels('THIS ONE','Truth sqrt(1-cos)')
plt.show()

plt.scatter(np.sqrt(df_uni.OMcos), np.sqrt(df_uni.mc_OMcos))
plt.title('Reconstructed vs true sqrt(1-cos)')
plt.xlabel('Reconstructed sqrt(1-cos)')
plt.ylabel('True sqrt(1-cos)')
plt.show()


omc = np.sqrt(df_uni.mc_OMcos)-np.sqrt(df_uni.OMcos)
n, bins, patches = plt.hist(omc, 20, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(omc)
plt.title(r'$\mathrm{(True-Reco)}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()

plt.scatter(df_uni.IP,omc)
plt.show()
plt.scatter(df_uni.OMcos,omc)
plt.show()



fig3 = plt.figure()
mass_ar = np.sqrt(2.*df_uni.Energy_A*df_uni.Energy_B*1.2*(df_uni.mc_OMcos))
#mass_ar = np.sqrt(2.*df_uni.Energy_A*df_uni.Energy_B*1.2*(df_uni.OMcos))
n, bins, patches = plt.hist(mass_ar, 30, facecolor='blue', alpha=0.75)
#n, bins, patches = plt.hist(mass_ar, 35, normed=1, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(mass_ar)
y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'r--', linewidth=1)
plt.title(r'$\mathrm{(True-Reco) / True:}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()


un_mass = sns.distplot(np.sqrt(2.*df_uni.Energy_A*df_uni.Energy_B*(df_uni.mc_OMcos)),kde=False)
#un_mass = sns.distplot(np.sqrt(2.*df_uni.Energy_A*df_uni.Energy_B*(1.-math.cos(df_uni.mc_opening_angle))),kde=False)
un_mass.set_xlim(0,300)
plt.show()
#Plot the mass WORKING HERE
un_mass = sns.distplot(np.sqrt(2.*df_uni.mc_gamma_A_mom_mag*1000*1000*df_uni.mc_gamma_B_mom_mag*(df_uni.OMcos)),kde=False)
un_mass.set_xlim(0,300)
plt.show()
#Plot the mass WORKING HERE
un_mass = sns.distplot(np.sqrt(2.*df_uni.mc_gamma_A_mom_mag*1000*1000*df_uni.mc_gamma_B_mom_mag*(df_uni.mc_OMcos)),kde=False)
un_mass.set_xlim(0,300)
plt.show()

#Plot the mass
un_mass = sns.distplot(df_uni.mass*10.,kde=False)
plt.show()
###
un_angle_mass = sns.jointplot("angle", "mass", data=df_uni)
plt.show()
###
un_ip_mass = sns.jointplot("ip", "mass", data=df_uni)
plt.show()
###


ax = sns.regplot(x="opening_angle", y="mass", data=df_uni)
plt.show()

ax = sns.regplot(x="opening_angle", y="mc_opening_angle", data=df_uni)
plt.show()

ax = sns.regplot(x="IP", y="mass", data=df_uni)
plt.show()


###
un_rada = sns.distplot(df_uni.radl_A,kde=False)
un_radb = sns.distplot(df_uni.radl_B,kde=False)
plt.show()

### Plot the curser
#Plot the mass
dun_mass = sns.distplot(df_dup.mass,kde=False)
dun_mass.set_xlim(0,300)
plt.show()
###
dun_angle_mass = sns.jointplot("angle", "mass", data=df_dup)
plt.show()
###
dun_ip_mass = sns.jointplot("ip", "mass", data=df_dup)
plt.show()
###
dun_rada = sns.distplot(df_dup.radl_A,kde=False)
dun_radb = sns.distplot(df_dup.radl_B,kde=False)
plt.show()


#########################################
#########################################
#########################################


###Make a selection 

#First find the max number or processes
maxproc = df.loc[df['proc'].idxmax()]

#list iterator position of passed events
sel_iter_loc = []
unsel_search_iter_loc = []

#########################################
#################CUTS ###################
#########################################
min_angle = 0.4
min_energy = 0.001
min_energy_sum = 0.100
max_ip = 6
max_asym = 0.8

for p in xrange(0,int(maxproc[0])):
    sublist = df[df['proc'].isin([p])].index.tolist()
    print 'This is the start of p'
    print sublist
    testsub = []
    keep_large_itr = -1
    energy_sum_val = -1
    for it in sublist:
	mass = df['mass'].loc[it]
	print mass 
	if df['angle'].loc[it] <min_angle:
	    continue
	if df['EL'].loc[it] <min_energy:
	    continue
	if df['ES'].loc[it] <min_energy:
	    continue
	if df['ip'].loc[it] >max_ip:
	    continue
	if df['ES'].loc[it]+df['EL'].loc[it] <min_energy_sum:
	    continue
	if math.fabs(df['ES'].loc[it]+df['EL'].loc[it])/df['ES'].loc[it]+df['EL'].loc[it] <max_asym:
	    continue
	if df['ES'].loc[it]+df['EL'].loc[it] >energy_sum_val:
	    keep_large_itr = it
	    energy_sum_val = df['ES'].loc[it]+df['EL'].loc[it] 
	
        #testsub.append(it)
    if keep_large_itr!=-1:
	testsub.append(keep_large_itr)
    if len(testsub)==1:
	sel_iter_loc.append(testsub[0])
    if len(testsub)>1:
	for t in testsub:
	    unsel_search_iter_loc.append(t)
	

print 'entries of the selected :', str(len(sel_iter_loc))
df_sel = df.loc[sel_iter_loc]
#Plot the mass
sel_mass = sns.distplot(df_sel.mass,kde=False)
sel_mass.set_xlim(0,300)
plt.show()


fig3 = plt.figure()
mass_ar = df_sel['mass'].values
n, bins, patches = plt.hist(mass_ar, 12, facecolor='blue', alpha=0.75)
#n, bins, patches = plt.hist(mass_ar, 35, normed=1, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(mass_ar)
y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'r--', linewidth=1)
plt.title(r'$\mathrm{(True-Reco) / True:}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()

###
sel_angle_mass = sns.jointplot("angle", "mass", data=df_sel)
plt.show()
###
sel_EL_mass = sns.jointplot("EL", "mass", data=df_sel)
sel_ES_mass = sns.jointplot("ES", "mass", data=df_sel)
plt.show()
#
###
sel_ip_mass = sns.jointplot("ip", "mass", data=df_sel)
plt.show()
###
sel_rada = sns.distplot(df_sel.radl_A,kde=False)
sel_radb = sns.distplot(df_sel.radl_B,kde=False)
plt.show()

print 'entries for which sel can still be made :', str(len(unsel_search_iter_loc))
 
#### What is still remaining 

df_unsel = df.loc[unsel_search_iter_loc]
#Plot the mass
unsel_mass = sns.distplot(df_unsel.mass,kde=False)
unsel_mass.set_xlim(0,300)
plt.show()
###
unsel_angle_mass = sns.jointplot("angle", "mass", data=df_unsel)
plt.show()
###
unsel_EL_mass = sns.jointplot("EL", "mass", data=df_unsel)
unsel_ES_mass = sns.jointplot("ES", "mass", data=df_unsel)
plt.show()
###
unsel_ip_mass = sns.jointplot("ip", "mass", data=df_unsel)
plt.show()
###
unsel_rada = sns.distplot(df_unsel.radl_A,kde=False)
unsel_radb = sns.distplot(df_unsel.radl_B,kde=False)
plt.show()

print ' This many process : ', str(maxproc[0])

