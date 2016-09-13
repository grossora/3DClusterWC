import sys, os
import ROOT
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
from scipy import stats
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import datahandle as dh
import protocluster as pc
import collections as col 

#Cheating on a few graphical things
from pylab import MaxNLocator

###############
####Define some lists and things 
tlist =[]
rlist =[]
sellist =[]
dlist =[]
dlistfrac =[]
energylist = []
nclist = []
selrecolist = []

mincluster = 10
maxdatasetsize = 10000
###############
###############


for f in sys.argv[1:]:
    fi = ROOT.TFile("{}".format(f))
    reco = fi.Get("T_rec_charge")
    true = fi.Get("T_true")
    mc = fi.Get("TMC")

    tot_mc_charge = 0.
    for ch in true:
        tot_mc_charge+=ch.q

    tot_r_charge = 0.
    for ch in reco:
        tot_r_charge+=ch.q

    
    # Bring in the data as an numpy array for clustering 
    predataset = dh.ConvertWC_InTPC('{}'.format(f))
    #predataset = dh.ConvertWC_InTPC('{}'.format(sys.argv[1]))
    #print 'predataset size ', len(predataset)
    dataset = dh.Unique(predataset)
    print 'dataset size ', len(dataset)

    # Do the clustering and pick off the info
####
#if this is taking too long skip the event
# We will not count this event and move forward
####
    if len(dataset)>maxdatasetsize:
	continue
    labels = pc.crawler(dataset,8.,10)
####
####
####
    countedlist = col.Counter(labels)
    largest_cluster_label =  countedlist.most_common(1)[0][0] 
    

    selectedcharge = 0.0
    for pt in dh.DuplicateIDX(labels,largest_cluster_label):
	# apply fit that is hardcode... ugh
	FitData  =dataset[pt][3]
	#FitData  =dataset[pt][3] - 0.472670977155*dataset[pt][3]+  105245.981838
	selectedcharge +=FitData 
	

    #add the total selected charge to the list
    sellist.append(selectedcharge)
    selrecolist.append(selectedcharge/tot_r_charge)

    #Number of clusters
    nclusters = [ x for x in countedlist.items() if x[1]>mincluster]
    #print ' n clusters ' , nclusters
    nclist.append(len(nclusters))

#################### 
# If we make it here fill out all the info!
    #get the energy of the particle 
    for m in mc:
        startmom = pow( pow(m.mc_startMomentum[0],2),0.5)# Not sure if this is correct
        energylist.append(startmom)

    tlist.append(tot_mc_charge)
    rlist.append(tot_r_charge)
    dlistfrac.append((tot_mc_charge-tot_r_charge)/tot_mc_charge)
    dlist.append(tot_mc_charge-tot_r_charge)

    print ' HOW HOW HOW TOT Charge R  ' , tot_r_charge
    print ' HOW HOW HOW TOT FRom Sel ' , selectedcharge 
    print ' HOW HOW HOW TOT FRAC ' , selectedcharge/tot_r_charge
   
#################### 



############ MC For the entire set from truth to reco... no clustering ###########
#Fit the ofset in charge 
#This is here but may not be needed
slope, intercept, r_value, p_value, std_err = stats.linregress(rlist,dlist)
# Refit the reco 
rfitlist= [ x + slope*x+intercept for x in rlist]
print slope,'  intercept ',intercept

# Calcuate the difference between the fit reco and truth 
dfitlist =[]
tfitlist =[]
energyfitlist =[]
for s in range(0,len(rfitlist)):
    if (tlist[s] - rfitlist[s])/tlist[s] <-0.2:
        continue # This is a shit hack  for plotting for now
    dfitlist.append((tlist[s] - rfitlist[s])/tlist[s])
    tfitlist.append(tlist[s])
    energyfitlist.append(energylist[s])

###############################
### Reco list v True List #####
###############################
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter( rlist, tlist, marker='o', c ='red' )
ax.grid(True)
ax.set_title('True vs. Reco Charge')
ax.set_xlabel('Reco Charge')
ax.set_ylabel('True Charge')
plt.show()

###############################
### Reco list v dif List #####
###############################
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.scatter( rlist,dlist,  marker='o', c ='red' )
ax2.grid(True)
ax2.set_title('Diff vs. chargereco')
ax2.set_xlabel('Particle charge reco')
ax2.set_ylabel('Diff Charge')
plt.show()

###############################
### Reco list v dif List #####
###############################
fig3 = plt.figure()
n, bins, patches = plt.hist(dfitlist, 35, normed=1, facecolor='blue', alpha=0.75)
(mu, sigma) = norm.fit(dfitlist)
y = mlab.normpdf( bins, mu, sigma)
l = plt.plot(bins, y, 'r--', linewidth=1)
plt.title(r'$\mathrm{(True-Reco) / True:}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
plt.show()

##################################
### energylist v diffit List #####
##################################
fig4 = plt.figure()
ax4 = fig4.add_subplot(111)
ax4.scatter( energyfitlist,dfitlist, s=70,  marker='o', c ='red' )
ax4.grid(True)
ax4.set_title('fit Charge res Difference vs energy')
ax4.set_xlabel('Particle charge energy')
ax4.set_ylabel('(true-fitreco)/true Charge Difference')
ax4.set_ylim([-0.5,0.2])
plt.show()

##################################
### energylist v diffit List #####
##################################
fig5 = plt.figure()
ax5 = fig5.add_subplot(111)
ax5.scatter( tfitlist,dfitlist, s=70,  marker='o', c ='red' )
ax5.grid(True)
ax5.set_title('true-reco Charge res Difference vs true charge')
#ax4.set_xlabel(' true charge')
ax5.set_xlabel('Particle charge ')
ax5.set_ylabel('(true-reco)/true Charge Difference')
ax5.set_ylim([-0.5,0.2])
plt.show()

####################################################################
####################################################################
####################################################################






####################################################################
###### Start to look at clustering effects #################
####################################################################

#sellist[0]/rlist[0]
##################################
### sellist v rlist ##############
##################################
fig6 = plt.figure()
ax6 = fig6.add_subplot(111)
ax6.scatter( sellist,rlist, s=70,  marker='o', c ='red' )
ax6.grid(True)
ax6.set_title('Clustered Charge vs Recocharge')
ax6.set_xlabel('Selected Charge ')
ax6.set_ylabel('Total Reco Charge')
plt.show()


##################################
### sellist v tlist ##############
##################################
fig7 = plt.figure()
ax7 = fig7.add_subplot(111)
ax7.scatter( sellist,tlist, s=70,  marker='o', c ='red' )
ax7.grid(True)
ax7.set_title('Clustered Charge vs truecharge')
ax7.set_xlabel('Selected Charge ')
ax7.set_ylabel('Total True Charge')
plt.show()


##################################
### nclusters v recocharge #######
##################################
fig8 = plt.figure()
ax8 = fig8.add_subplot(111)
ax8.hist(nclist, [x for x in range(np.max(nclist)+1)], facecolor='blue', alpha=0.75)
ax8.grid(True)
ax8.set_title('nclusters hist')
ax8.set_xlabel('Selected Charge ')
ax8.set_ylabel('Total True Charge')
xa = ax8.get_xaxis()
xa.set_major_locator(MaxNLocator(integer=True))
plt.show()


#sellist[0]/rlist[0]
##################################
### sellist v rlist ##############
##################################
fig6 = plt.figure()
ax6 = fig6.add_subplot(111)
ax6.scatter( rlist,selrecolist, s=70,  marker='o', c ='red' )
ax6.grid(True)
ax6.set_title('fraction of clustered charge vs Recocharge')
ax6.set_xlabel('Selected Charge ')
ax6.set_ylabel('Total Reco Charge')
ax6.set_ylim([0.,1.1])
ax6.set_xlim([0.,int(max(rlist))+10000000.])
fig6.savefig('Frac_clustered.png')
plt.show()




#################
######SUMMARY
#################


print 'Summary: ' , len(tlist), ' out of ', len(sys.argv[1:]),' total files were processed '  
