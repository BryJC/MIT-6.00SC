#US Counties example
def readCountyData(fName, numEntries = 14): #parse data from counties.txt, which contains 14 default data fields (excluding name)

    dataFile = open(fName, 'r') #open counties.txt in read-only mode, assign it to dataFile variable
    dataList = [] #create empty list 'dataList', will hold data fields of counties
    nameList = [] #create empty list 'nameList', will hold names of counties
    maxVals = np.array([0.0]*numEntries) #create empty array 'maxVals', will hold max value from each data field
    
    #Build unnormalized feature vector
    for line in dataFile:
        if len(line) == 0 or line[0] == '#': #skip null or comment lines
            continue
        dataLine = string.split(line) #split each line into individual data fields
        name = dataLine[0] + dataLine[1] #create full name for each county
        features = [] #create empty list 'features', will hold data fields of EACH individual line (i.e county)
        
        #Build vector with numEntries features
        for f in dataLine[2:]:
            try:
                f = float(f) #ensure each data point remains a float
                features.append(f) #add each data point to line's (i.e. county's) feature vector
                if f > maxVals[len(features)-1]: #checks index in maxVals corresponding to f index in feature vector. 
                    maxVals[len(features)-1] = f #if f is larger, assign f value to above index in maxVal array
            except ValueError:
                name = name + f #error that assumes f is actually a name point
        if len(features) != numEntries: #disallows only partially full lines to be added to full data/name lists
            continue #...except maxVals are kept? Seems strange
            
        dataList.append(features) #append dataList with feature vector of each county
        nameList.append(name) #append nameList with name of each county
        
    return nameList, dataList, maxVals #return list of county names, feature vector, and maximum values for each feature

    
def buildCountyPoints(fName): #take names, data, and max values from counties.txt and use it to create list of County(Point) objects
    """
    Given an input filename, reads County values from the file and returns
    them all in a list.
    """
    nameList, featureList, maxVals = readCountyData(fName) #perform readCountyData on counties.txt
    points = [] #create empty 'points' list, to be filled with County points)
    
    for i in range(len(nameList)): #for all named entries
        originalAttrs = np.array(featureList[i]) #create 'originalAttrs' array for the i'th feature vector from featureList
        normalizedAttrs = originalAttrs/np.array(maxVals) #create 'normalizedAttrs' array for the i'th feature vector from featureList\
                                                          #using originalAttrs divided by the maxValue for each data field
        points.append(County(nameList[i], originalAttrs, normalizedAttrs))#create County object using the i'th name and two attr arrays
        
    return points #return the list of all County objects created
    
################################################################################

class Point(object):
    def __init__(self, name, originalAttrs, normalizedAttrs = None):
        """normalizedAttrs and originalAttrs are both arrays"""
        self.name = name
        self.unNormalized = originalAttrs
        self.attrs = normalizedAttrs
    def dimensionality(self):
        return len(self.attrs)
    def getAttrs(self):
        return self.attrs
    def getOriginalAttrs(self):
        return self.unNormalized
    def distance(self, other):
        #Euclidean distance metric
        difference = self.attrs - other.attrs
        return sum(difference * difference) ** 0.5
    def getName(self):
        return self.name
    def toStr(self):
        return self.name + str(self.attrs)
    def __str__(self):
        return self.name

class County(Point):
    weights = np.array([1.0] * 14)
    
    # Override Point.distance to use County.weights to decide the
    # significance of each dimension
    def distance(self, other):
        difference = self.getAttrs() - other.getAttrs()
        return sum(County.weights * difference * difference) ** 0.5
        
################################################################################
            
class Cluster(object):
    def __init__(self, points, pointType):
        self.points = points
        self.pointType = pointType
        self.centroid = self.computeCentroid()
    def getCentroid(self):
        return self.centroid
        
    def computeCentroid(self):
        dim = self.points[0].dimensionality() #get the dimesionality of the points within cluster
        totVals = np.array([0.0]*dim) #create array with same dimensionality
        for p in self.points:
            totVals += p.getAttrs() #sum up each feature vector value for each point in cluster
        meanPoint = self.pointType('mean',
                                   totVals/float(len(self.points)),
                                   totVals/float(len(self.points))) 
                   #creates a centroid, or creation of point based upon feature vector value averages within current grouping of points
        return meanPoint
        
    def update(self, points):
        oldCentroid = self.centroid #assign currently computed centroid point object to oldCentroid variable
        self.points = points #assign updated points list to self.points
        if len(points) > 0:
            self.centroid = self.computeCentroid() #compute self.centroid based upon new self.points
            return oldCentroid.distance(self.centroid) 
            #determine the difference in feature value vectors between centroid point objects (old and newly assigned), \
            #return this as the 'distance' between the centroids
        else:
            return 0.0
            
    def getPoints(self):
        return self.points
    def contains(self, name):
        for p in self.points:
            if p.getName() == name:
                return True
        return False
    def toStr(self):
        result = ''
        for p in self.points:
            result = result + p.toStr() + ', '
        return result[:-2]
    def __str__(self):
        result = ''
        for p in self.points:
            result = result + str(p) + ', '
        return result[:-2]
        
################################################################################            

def kmeans(points, k, cutoff, pointType, minIters = 3, maxIters = 100, toPrint = False):
    """ Returns (Cluster list, max dist of any point to its cluster) """
    #Uses random initial centroids
    initialCentroids = random.sample(points,k) #picks k (county) point objects from all objects in points list
    clusters = [] #initialize empty clusters list
    
    for p in initialCentroids:
        clusters.append(Cluster([p], pointType)) #create Cluster objects using each point from initialCentroids, put into clusters list
        
    numIters = 0 #start iterations count
    biggestChange = cutoff #assign biggest change to cutoff value (will be updated by performing distance function from clusters)
    while (biggestChange >= cutoff and numIters < maxIters) or numIters < minIters:
    #while biggestChange continues to be larger than the cutoff (meaning distance change between centroid update is still large enough\
    #AND num_iters is less than the max num_iters, OR num_iters continues to be less than the max num_iters,
    #continue to try and find optimal clustering
    
        print "Starting iteration " + str(numIters)
        #starting iteration number: numIters
        newClusters = [] #create new clusters list
        for c in clusters:
            newClusters.append([]) #add number of empty buckets to newClusters equivalent to num_clusters in clusters
        for p in points:
            smallestDistance = p.distance(clusters[0].getCentroid()) 
            #for each point, find difference between first cluster centroid point and point p feature vector, set to smallestDist.
            index = 0
            for i in range(len(clusters)):
                distance = p.distance(clusters[i].getCentroid())
                #for each point, find difference between i'th cluster centroid point and point p feature vector, set to distance.
                if distance < smallestDistance: #if distance is smaller than the previously established smallestDistance:
                    smallestDistance = distance #distance is now assigned to smallestDistance
                    index = i #index of smallestDistance is set to i
            newClusters[index].append(p)
            #append the i'th bucket (set by smallestDistance) in newClusters with the point p
            #allows for points to be concentrated around centroid point object (i.e. the smallestDistance) when creating new clusters
                    
        biggestChange = 0.0 #set initial value to 0 for changes in centroid value
        for i in range(len(clusters)):
            change = clusters[i].update(newClusters[i]) #updates each cluster i in cluster with the new set of points from \
                                                        #i in newClusters, returns the difference between old and new centroid \ 
                                                        #feature vectors.
            #print "Cluster " + str(i) + ": " + str(len(clusters[i].points))
            biggestChange = max(biggestChange, change) #set biggestChange in centroid value to either current biggestChange or \
                                                       #the centroid difference between old and new centroid calculations
        numIters += 1 #add a count to iterations
        if toPrint:
            print 'Iteration count =', numIters
            
    maxDist = 0.0 #set initial value to 0 for changes in centroid value
    for c in clusters:
        for p in c.getPoints():
        #iterate through each point within each cluster within the final cluster list
            if p.distance(c.getCentroid()) > maxDist:
                maxDist = p.distance(c.getCentroid())
                #if the point object p distance(difference) to it's cluster's centroid is > current maxDistance,
                #set maxDist to p's distance calculation
                
    print 'Total Number of iterations =', numIters, 'Max Diameter =', maxDist
    print biggestChange
    return clusters, maxDist #return the list of final clusters containing clusters that have minimized distance(difference) between their points and their average point (the computed centroid), as well as the maximum distance remaining between any of the points in any of the clusters relative to it's cluster's centroid.
    
################################################################################

def getAveIncome(cluster):
    """
    Given a Cluster object, finds the average income field over the members
    of that cluster.
    
    cluster: the Cluster object to check
    
    Returns: a float representing the computed average income value
    """
    tot = 0.0
    numElems = 0
    for c in cluster.getPoints():
        tot += c.getOriginalAttrs()[1]

    return float(tot) / len(cluster.getPoints())
    #use to determine the average income of county point objects within each cluster created by the kmeans function
    #return the avergae income (from original, non-normalized attributes)
    
################################################################################

        
