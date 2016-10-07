import sys,os 
import collections as col

#incoming file 
lines = open('{}'.format(sys.argv[1])).readlines()
newfile = open('PiZero_Selection_Params_Cleaned.txt', 'w')

for l in lines: 
    #split up the line
    lsp = l.split(' ')
    # Ask if index 4,5,6,7,8 are the same 
    aa = [ float(lsp[x]) for x in xrange(4,11)]
    a = col.Counter(aa).items()[0][1]
    if a == 7:
	#This is a dud line
	continue
    newfile.write(l)

newfile.close()
    
    
	
    




