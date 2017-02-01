import numpy as np
from sklearn.decomposition import PCA

def clusterspread(dataset,datasetidx_holder, first, clustersize):

    print 'start of clusterspread'
    track_holder = []
    shower_holder = []
    for a in datasetidx_holder:
        points = []
        for p in a:
            pt = [ dataset[p][0],dataset[p][1],dataset[p][2] ]
            points.append(pt)

        if len(points)<clustersize:
            # Push this to the showers holder
            shower_holder.append(a)
            continue

	par = -999
        try:
            pca = PCA(n_components=3)
            pca.fit(points)
            par = pca.explained_variance_ratio_
	except:
	    print ' could not make a PCA'
            shower_holder.append(a)

        if par[0] > first:
            print len(points)
            print par[0]
            track_holder.append(a)
            continue
        else:
            shower_holder.append(a)

    return shower_holder, track_holder
