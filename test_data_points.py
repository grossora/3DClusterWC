import sys, os
import numpy as np
import Utils.datahandle as dh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import style
style.use("ggplot")
colors = 10*['r','g','b','c','k','y','m']

## Find Event number
evtpath = str(sys.argv[1])
evt = evtpath.split('result_')[1].split('.')[0]

# Open up the text file for looking up the ROI 
# Find the line that had the evt and then read off the rest of the params 
lookup = open('ROI_Visual.txt','r')

fid_v =[]
for line in lookup:
    #print line
    # split up the line
    line_v = line.split()
    if line_v[0] == evt:
        fid_v = line_v[1:]
if len(fid_v) ==0:
    print 'We did not find an ROI for this event'
    print ' If you like you may put them in manually... don\'t mess it up '
    xlo = raw_input('Value for xlo:')
    xhi = raw_input('Value for xhi:')
    ylo = raw_input('Value for ylo:')
    yhi = raw_input('Value for yhi:')
    zlo = raw_input('Value for zlo:')
    zhi = raw_input('Value for zhi:')
    fid_v = [xlo,xhi,ylo,yhi,zlo,zhi]
print 'These are the params you are using ', fid_v
#bring in the data
predataset = dh.ConvertWC_InRange('{}'.format(sys.argv[1]),float(fid_v[0]),float(fid_v[1]),float(fid_v[2]),float(fid_v[3]),float(fid_v[4]),float(fid_v[5]))
print 'predataset size ', len(predataset)
dataset = dh.Unique(predataset)
print 'dataset size ', len(dataset)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#for i in dataset:
for i in range(len(dataset)):
    ax.scatter(dataset[i][0], dataset[i][1], dataset[i][2], marker='o')
ax.set_xlabel('X ')
ax.set_ylabel('Y ')
ax.set_zlabel('Z ')

plt.show()

