import numpy as np 
from sklearn.decomposition import PCA
from scipy.spatial import ConvexHull






def locallin_clean(dataset, datasetidx_holder, min_clustersize, max_cluster_length,k_radius, rep_level, min_mean_err  ):
    # A few things to start
    k_radius_sq = k_radius*k_radius
    track_holder = []
    shower_holder = []

    #bring in the object 
    for a in datasetidx_holder:
        points = []
        for p in a:
            pt = [ dataset[p][0],dataset[p][1],dataset[p][2] ]
            points.append(pt)
	#check to see if tghe cluster is large engouh
        if len(points)<min_clustersize:
            # Push this to the showers holder
            shower_holder.append(a)
            continue


        #now we are going to loop over all the points and get the local region fit
        region_fit = []
	hull_points = []
        for pt_a in range(0,len(points)):
            # Get the first point
            pa = points[pt_a]
            region_pts = [pa]
            hull_points.append(pa)
	    # loop over all the other points
            for pt_b in xrange(0,len(points)):
		if pt_b==pt_a:
		    continue
                pb = points[pt_b]
                test_dist_sq = (pa[0]-pb[0])*(pa[0]-pb[0])+(pa[1]-pb[1])*(pa[1]-pb[1])+(pa[2]-pb[2])*(pa[2]-pb[2])
		# Check if the point is inside the sphere
                if test_dist_sq<k_radius:
                    # Keep this point to fit to
                    region_pts.append(pb)

            # Once we have made it here we need to fit the line 
            # This needs to be a try catch... if its fails just put it as a shower
            pca_var = -999
            try:
                # perfrom the PCA 
                pca = PCA(n_components=1)
                pca.fit(region_pts)
                # Now we need to store this fit spread
                pca_var = pca.explained_variance_ratio_[0]
            except:
                print 'Opps we dont have a pca'

            if not pca_var== -999 and not np.isnan(pca_var):
                region_fit.append(pca_var)

	##### Now Make the hull to get the length 
	cluster_length = -999
        try :
	    hull = ConvexHull(hull_points)
            min_bd = hull.min_bound
            max_bd = hull.max_bound
            cluster_length = np.linalg.norm(min_bd-max_bd)
	    
	except:
	    print ' hull is too small or something '

        # Check if it is past the min_length
        if cluster_length>max_cluster_length:
            print ' look how long a cluster ' , str(cluster_length)
            track_holder.append(a)
            continue
        
        represetation_conf = 1.0*len(region_fit)/len(points)
        if represetation_conf ==0.0:
            shower_holder.append(a)
            continue

	
        #outlier level
	# Remove the outliers... shower we be doing this? 
        #region_fit_no_outlier = region_fit[abs(region_fit - np.mean(region_fit)) < m * np.std(region_fit)]
        m = 2
        region_fit_no_outlier = []
        for i in range(len(region_fit)):
            if abs(region_fit[i] - np.mean(region_fit)) < m * np.std(region_fit):
                region_fit_no_outlier.append(region_fit[i])

        ################################################
        ################################################
        # make some decisions about tracklike or shower
        ################################################
        ################################################
        if np.mean(region_fit) > min_mean_err and represetation_conf>rep_level :
            print '\033[1;34m ####### Print out some info #############################'
            print 'This is the len of points ', str(len(points))
            print 'This is the represetnation _conf ', str(represetation_conf)
            print 'This is the mean of the region', str(np.mean(region_fit))
            print 'This is the len of region_fit ', str(len(region_fit))
            print 'This is the len of no outlier ', str(len(region_fit_no_outlier))
            print 'This is the mean of the nooutlier region', str(np.mean(region_fit_no_outlier))
            print 'This is the Product_Param  ', str(np.mean(region_fit)*represetation_conf)
            print 'This is the avg_Param  ', str((np.mean(region_fit)+represetation_conf)/2)
            print 'This is the FullProduct_Param  ', str(len(points)*np.mean(region_fit)*represetation_conf)
            print 'This is the meanProductpoints_Param  ', str(len(points)*np.mean(region_fit))
            print 'This is the length  ', str(cluster_length)
            print 'This is the length_avggerion  ', str(cluster_length*np.mean(region_fit))
            print 'This is the pow(length,avg)  ', str(pow(cluster_length,np.mean(region_fit)))
            print 'This is the pow(length,avgnoout)  ', str(pow(cluster_length,np.mean(region_fit_no_outlier)))
	

            print '###################################################### \n '
	    print '\033[0;0m'



            # ^^^ This is just a guess 
            track_holder.append(a)
        else:
            print '\033[1;31m ####### Print out some info #############################'
            print 'This is the len of points ', str(len(points))
            print 'This is the represetnation _conf ', str(represetation_conf)
            print 'This is the mean of the region', str(np.mean(region_fit))
            print 'This is the len of region_fit ', str(len(region_fit))
            print 'This is the len of no outlier ', str(len(region_fit_no_outlier))
            print 'This is the mean of the nooutlier region', str(np.mean(region_fit_no_outlier))
            print 'This is the Product_Param  ', str(np.mean(region_fit)*represetation_conf)
            print 'This is the avg_Param  ', str((np.mean(region_fit)+represetation_conf)/2)
            print 'This is the FullProduct_Param  ', str(len(points)*np.mean(region_fit)*represetation_conf)
            print 'This is the meanProductpoints_Param  ', str(len(points)*np.mean(region_fit))
            print 'This is the length  ', str(cluster_length)
            print 'This is the length_avggerion  ', str(cluster_length*np.mean(region_fit))
            print 'This is the pow(length,avg)  ', str(pow(cluster_length,np.mean(region_fit)))
            print 'This is the pow(length,avgnoout)  ', str(pow(cluster_length,np.mean(region_fit_no_outlier)))
	

            print '###################################################### \n '
	    print '\033[0;0m'


            '''     
            print '\n ######################################################'
            print '####### Print out some info #############################'
            print 'This is the len of points ', str(len(points))
            print 'This is the represetnation _conf ', str(represetation_conf)
            print 'This is the len of no outlier ', str(len(region_fit_no_outlier))
            print 'This is the mean of the region', str(np.mean(region_fit))
            print 'This is the len of region_fit ', str(len(region_fit))
            print '###################################################### \n '
            '''
            shower_holder.append(a)

    return shower_holder, track_holder


	















def locallin(dataset, datasetidx_holder, min_clustersize, k_radius, rep_level, min_mean_err  ):
#def locallin(dataset, datasetidx_holder, min_clustersize, k_radius  ):
#    print 'start of local lin'
    k_radius_sq = k_radius*k_radius
    track_holder = []
    shower_holder = []
    #bring in the object 
    for a in datasetidx_holder:
        points = []
        for p in a:
            pt = [ dataset[p][0],dataset[p][1],dataset[p][2] ]
            points.append(pt)
        #check to see if tghe cluster is large engouh
        if len(points)<min_clustersize:
            # Push this to the showers holder
            shower_holder.append(a)
#            print 'bailing because of min cluster size'
            continue

        region_fit = []
        for pt_a in range(0,len(points)):
            # Get the first point
            pa = points[pt_a]
            region_pts = [pa]
            for pt_b in xrange(pt_a,len(points)):
                pb = points[pt_b]
                #pa = [ points[pt_a][0],points[pt_a][1],points[pt_a][2]]
                #pb = [ points[pt_b][0],points[pt_b][1],points[pt_b][2]]
                test_dist_sq = (pa[0]-pb[0])*(pa[0]-pb[0])+(pa[1]-pb[1])*(pa[1]-pb[1])+(pa[2]-pb[2])*(pa[2]-pb[2])
                #test_dist = distance.euclidean(pa,pb)
                if test_dist_sq<k_radius:
                    # Keep this point to fit to
                    region_pts.append(pb)

            # Once we have made it here we need to fit the line 
            # This needs to be a try catch... if its fails just put it as a shower
            # IDEA: Use hul to get length and volume to also cut on 
            pca_var = -999
            try:
                # perfrom the PCA 
                pca = PCA(n_components=1)
                pca.fit(region_pts)
                # Now we need to store this fit spread
                pca_var = pca.explained_variance_ratio_[0]
            except:
                print 'Opps we dont have a pca'


            #if not pca_var== -999:
            if not pca_var== -999 and not np.isnan(pca_var):
                #print 'filling region fit'
                #print pca_var
                region_fit.append(pca_var)

        # Now we have the fit values for all points in the cluster

        # this can act as pseudo confidence of representation
        # take the len(region_pts)/total number of points
        # This represents how many points actually got fit... if this value is low it means that is not doing a good representation of points
        # Shower are difuse so there stray points will not have neighbors around them and will not get put into the fit

        represetation_conf = 1.0*len(region_fit)/len(points)
	if represetation_conf ==0.0:	
	    continue

        # Need to figure out a few ways to decided if it's track like 

        #First take the average? Maybe Remove outliers first? 

        #outlier level
        #region_fit_no_outlier = region_fit[abs(region_fit - np.mean(region_fit)) < m * np.std(region_fit)]
        m = 2
        region_fit_no_outlier = []
        for i in range(len(region_fit)):
            if abs(region_fit[i] - np.mean(region_fit)) < m * np.std(region_fit):
                region_fit_no_outlier.append(region_fit[i])

        # with respect to  points # if this is close to 1 that means not a lot removed ... which means a tight distribution
        represetation_noout_conf = 1.0*len(region_fit_no_outlier)/len(region_fit)
        # with respect to all points
        represetation_all_noout_conf = 1.0*len(region_fit_no_outlier)/len(points)

        ##### Print out some things just to see what is going on 
#        print '\n ######################################################'
#        print '####### Print out some info #############################'
#        print 'This is the len of points ', str(len(points))
#        print 'This is the represetnation _conf ', str(represetation_conf)
#        print 'This is the len of no outlier ', str(len(region_fit_no_outlier))
#        print 'This is the mean of the region', str(np.mean(region_fit))
#        print 'This is the len of region_fit ', str(len(region_fit))
#        print '###################################################### \n '


        ################################################
        ################################################
        # make some decisions about tracklike or shower
        ################################################
        ################################################
        if np.mean(region_fit) > min_mean_err and represetation_conf>rep_level :
            # ^^^ This is just a guess 
            print '\n ######################################################'
            print '####### Print out some info #############################'
            print 'This is the len of points ', str(len(points))
            print 'This is the represetnation _conf ', str(represetation_conf)
            print 'This is the len of no outlier ', str(len(region_fit_no_outlier))
            print 'This is the mean of the region', str(np.mean(region_fit))
            print 'This is the len of region_fit ', str(len(region_fit))
            print 'This is the Product_Param  ', str(np.mean(region_fit)*represetation_conf)
            print 'This is the avg_Param  ', str((np.mean(region_fit)+represetation_conf)/2)
            print 'This is the FullProduct_Param  ', str(len(points)*np.mean(region_fit)*represetation_conf)
            print 'This is the meanProductpoints_Param  ', str(len(points)*np.mean(region_fit))

	    print '###################################################### \n '
            
            track_holder.append(a)
        else:
	    '''	    
            print '\n ######################################################'
            print '####### Print out some info #############################'
            print 'This is the len of points ', str(len(points))
            print 'This is the represetnation _conf ', str(represetation_conf)
            print 'This is the len of no outlier ', str(len(region_fit_no_outlier))
            print 'This is the mean of the region', str(np.mean(region_fit))
            print 'This is the len of region_fit ', str(len(region_fit))
	    print '###################################################### \n '
	    '''	    
            shower_holder.append(a)

    return shower_holder, track_holder






def Cosmic_TrackRemover(dataset, datasetidx_holder, min_clustersize,clusterlength, k_radius, rep_level, min_mean_err  ):
#def locallin_length(dataset, datasetidx_holder, min_clustersize,clusterlength, k_radius, rep_level, min_mean_err  ):
#    print 'start of local lin'
    k_radius_sq = k_radius*k_radius
    track_holder = []
    shower_holder = []
    #bring in the object 
    for a in datasetidx_holder:
        points = []
        for p in a:
            pt = [ dataset[p][0],dataset[p][1],dataset[p][2] ]
            points.append(pt)
        #check to see if tghe cluster is large engouh
        if len(points)<min_clustersize:
            # Push this to the showers holder
            shower_holder.append(a)
#            print 'bailing because of min cluster size'
            continue


        # Now get the object length
	#Throughout the whole loop
	hull_points = []
        region_fit = []
        for pt_a in range(0,len(points)):
            # Get the first point
            pa = points[pt_a]
	    hull_points.append(pt_a)
	    #Log this in the whole points vector
            region_pts = [pa]
            for pt_b in xrange(pt_a,len(points)):
                pb = points[pt_b]
                #pb = [ points[pt_b][0],points[pt_b][1],points[pt_b][2]]
                test_dist_sq = (pa[0]-pb[0])*(pa[0]-pb[0])+(pa[1]-pb[1])*(pa[1]-pb[1])+(pa[2]-pb[2])*(pa[2]-pb[2])
                #test_dist = distance.euclidean(pa,pb)
                if test_dist_sq<k_radius:
                    # Keep this point to fit to
                    region_pts.append(pb)

            # Once we have made it here we need to fit the line 
            # This needs to be a try catch... if its fails just put it as a shower
            # IDEA: Use hul to get length and volume to also cut on 
            pca_var = -999
            try:
                # perfrom the PCA 
                pca = PCA(n_components=1)
                pca.fit(region_pts)
                # Now we need to store this fit spread
                pca_var = pca.explained_variance_ratio_[0]
	        #make a hull of the region points
	        hull = ConvexHull(region_pts)

	        
            except:
                print 'Opps we dont have a pca'


            #if not pca_var== -999:
            if not pca_var== -999 and not np.isnan(pca_var):
                #print 'filling region fit'
                #print pca_var
                region_fit.append(pca_var)

        # Now we have the fit values for all points in the cluster

        # this can act as pseudo confidence of representation
        # take the len(region_pts)/total number of points
        # This represents how many points actually got fit... if this value is low it means that is not doing a good representation of points
        # Shower are difuse so there stray points will not have neighbors around them and will not get put into the fit

        represetation_conf = 1.0*len(region_fit)/len(points)
	if represetation_conf ==0.0:	
	    continue

        # Need to figure out a few ways to decided if it's track like 

        #First take the average? Maybe Remove outliers first? 

        #outlier level
        #region_fit_no_outlier = region_fit[abs(region_fit - np.mean(region_fit)) < m * np.std(region_fit)]
        m = 2
        region_fit_no_outlier = []
        for i in range(len(region_fit)):
            if abs(region_fit[i] - np.mean(region_fit)) < m * np.std(region_fit):
                region_fit_no_outlier.append(region_fit[i])

        # with respect to  points # if this is close to 1 that means not a lot removed ... which means a tight distribution
        represetation_noout_conf = 1.0*len(region_fit_no_outlier)/len(region_fit)
        # with respect to all points
        represetation_all_noout_conf = 1.0*len(region_fit_no_outlier)/len(points)

        ##### Print out some things just to see what is going on 
#        print '\n ######################################################'
#        print '####### Print out some info #############################'
#        print 'This is the len of points ', str(len(points))
#        print 'This is the represetnation _conf ', str(represetation_conf)
#        print 'This is the len of no outlier ', str(len(region_fit_no_outlier))
#        print 'This is the mean of the region', str(np.mean(region_fit))
#        print 'This is the len of region_fit ', str(len(region_fit))
#        print '###################################################### \n '


        ################################################
        ################################################
        # make some decisions about tracklike or shower
        ################################################
        ################################################
        if np.mean(region_fit) > min_mean_err and represetation_conf>rep_level :
            # ^^^ This is just a guess 
            print '\n ######################################################'
            print '####### Print out some info #############################'
            print 'This is the len of points ', str(len(points))
            print 'This is the represetnation _conf ', str(represetation_conf)
            print 'This is the len of no outlier ', str(len(region_fit_no_outlier))
            print 'This is the mean of the region', str(np.mean(region_fit))
            print 'This is the len of region_fit ', str(len(region_fit))
            print 'This is the Product_Param  ', str(np.mean(region_fit)*represetation_conf)
            print 'This is the avg_Param  ', str((np.mean(region_fit)+represetation_conf)/2)
            print 'This is the FullProduct_Param  ', str(len(points)*np.mean(region_fit)*represetation_conf)
            print 'This is the meanProductpoints_Param  ', str(len(points)*np.mean(region_fit))

	    print '###################################################### \n '
            
            track_holder.append(a)
        else:
	    '''	    
            print '\n ######################################################'
            print '####### Print out some info #############################'
            print 'This is the len of points ', str(len(points))
            print 'This is the represetnation _conf ', str(represetation_conf)
            print 'This is the len of no outlier ', str(len(region_fit_no_outlier))
            print 'This is the mean of the region', str(np.mean(region_fit))
            print 'This is the len of region_fit ', str(len(region_fit))
	    print '###################################################### \n '
	    '''	    
            shower_holder.append(a)

    return shower_holder, track_holder

