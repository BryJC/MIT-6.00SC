# Problem Set 10
# Name:
# Collaborators:
# Time:

#Code shared across examples
import numpy as np, random, string, copy, math
import matplotlib.pyplot as plt 

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
    weights = np.array([1.0, 1.0, 0.0, 0.4, 0.1, 0.0, 0.0, 0.4, 0.3, 0.8, 1.0, 0.2, 0.5, 0.0])
    #turn off poverty weight, will be looking to see if we can find predictive power for this category 
    
    # Override Point.distance to use County.weights to decide the
    # significance of each dimension
    def distance(self, other):
        difference = self.getAttrs() - other.getAttrs()
        return sum(County.weights * difference * difference) ** 0.5
    
class Cluster(object):
    def __init__(self, points, pointType):
        self.points = points
        self.pointType = pointType
        self.centroid = self.computeCentroid()
    def getCentroid(self):
        return self.centroid
    def computeCentroid(self):
        dim = self.points[0].dimensionality()
        totVals = np.array([0.0]*dim)
        for p in self.points:
            totVals += p.getAttrs()
        meanPoint = self.pointType('mean',
                                   totVals/float(len(self.points)),
                                   totVals/float(len(self.points)))
        return meanPoint
    def update(self, points):
        oldCentroid = self.centroid
        self.points = points
        if len(points) > 0:
            self.centroid = self.computeCentroid()
            return oldCentroid.distance(self.centroid)
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
        

    
def kmeans(points, k, cutoff, pointType, minIters = 3, maxIters = 100, toPrint = False):
    """ Returns (Cluster list, max dist of any point to its cluster) """
    #Uses random initial centroids
    initialCentroids = random.sample(points,k)
    clusters = []
    for p in initialCentroids:
        clusters.append(Cluster([p], pointType))
    numIters = 0
    biggestChange = cutoff
    while (biggestChange >= cutoff and numIters < maxIters) or numIters < minIters:
        print "Starting iteration " + str(numIters)
        newClusters = []
        for c in clusters:
            newClusters.append([])
        for p in points:
            smallestDistance = p.distance(clusters[0].getCentroid())
            index = 0
            for i in range(len(clusters)):
                distance = p.distance(clusters[i].getCentroid())
                if distance < smallestDistance:
                    smallestDistance = distance
                    index = i
            newClusters[index].append(p)
        biggestChange = 0.0
        for i in range(len(clusters)):
            change = clusters[i].update(newClusters[i])
            #print "Cluster " + str(i) + ": " + str(len(clusters[i].points))
            biggestChange = max(biggestChange, change)
        numIters += 1
        if toPrint:
            print 'Iteration count =', numIters
    maxDist = 0.0
    for c in clusters:
        for p in c.getPoints():
            if p.distance(c.getCentroid()) > maxDist:
                maxDist = p.distance(c.getCentroid())
    print 'Total Number of iterations =', numIters, 'Max Diameter =', maxDist
    print biggestChange
    return clusters, maxDist

#US Counties example
def readCountyData(fName, numEntries = 14):
    dataFile = open(fName, 'r')
    dataList = []
    nameList = []
    maxVals = np.array([0.0]*numEntries)
    #Build unnormalized feature vector
    for line in dataFile:
        if len(line) == 0 or line[0] == '#':
            continue
        dataLine = string.split(line)
        name = dataLine[0] + dataLine[1]
        features = []
        #Build vector with numEntries features
        for f in dataLine[2:]:
            try:
                f = float(f)
                features.append(f)
                if f > maxVals[len(features)-1]:
                    maxVals[len(features)-1] = f
            except ValueError:
                name = name + f
        if len(features) != numEntries:
            continue
        dataList.append(features)
        nameList.append(name)
    return nameList, dataList, maxVals
    
def buildCountyPoints(fName):
    """
    Given an input filename, reads County values from the file and returns
    them all in a list.
    """
    nameList, featureList, maxVals = readCountyData(fName)
    points = []
    for i in range(len(nameList)):
        originalAttrs = np.array(featureList[i])
        normalizedAttrs = originalAttrs/np.array(maxVals)
        points.append(County(nameList[i], originalAttrs, normalizedAttrs))
    return points

def randomPartition(l, p):
    """
    Splits the input list into two partitions, where each element of l is
    in the first partition with probability p and the second one with
    probability (1.0 - p).
    
    l: The list to split
    p: The probability that an element of l will be in the first partition
    
    Returns: a tuple of lists, containing the elements of the first and
    second partitions.
    """
    l1 = []
    l2 = []
    for x in l:
        if random.random() < p:
            l1.append(x)
        else:
            l2.append(x)
    return (l1,l2)

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


def test(points, k = 200, cutoff = 0.1):
    """
    A sample function to show you how to do a simple kmeans run and graph
    the results.
    """
    incomes = []
    print ''
    clusters, maxSmallest = kmeans(points, k, cutoff, County)

    for i in range(len(clusters)):
        if len(clusters[i].points) == 0: continue
        incomes.append(getAveIncome(clusters[i]))

    plt.hist(incomes)
    plt.xlabel('Ave. Income')
    plt.ylabel('Number of Clusters')
    plt.show()

        
points = buildCountyPoints('counties.txt')
#random.seed(123)
testPoints = random.sample(points, len(points)/10)

#########
#########    
    
def graphRemovedErr(points, kvals = [25, 50, 75, 100, 125, 150], cutoff = 0.1, plot = True, giveVals = False):
    """
    Should produce graphs of the error in training and holdout point sets, and
    the ratio of the error of the points, after clustering for the given values of k.
    For details see Problem 1.
    """
    # Your Code Here
    k_train_errors = []
    k_hold_errors = []
    
    for k in kvals:
        holdout, testing = randomPartition(points, 0.2)
        
        print ''
        clusters, maxSmallest = kmeans(testing, k, cutoff, County)
        
        train_error = 0.0
        for c in clusters:
            for p in c.getPoints():
                train_error += (p.distance(c.getCentroid()))**2
        
        hold_error = 0.0
        for p in holdout:
            smallestDist = p.distance(clusters[0].getCentroid())
            for c in clusters:
                if p.distance(c.getCentroid()) < smallestDist:
                    smallestDist = p.distance(c.getCentroid())
            hold_error += smallestDist**2
            
        k_train_errors.append(train_error)
        k_hold_errors.append(hold_error)
        
    k_train_errors = np.array(k_train_errors)
    k_hold_errors = np.array(k_hold_errors)
        
    ###
    if plot:
        plt.subplot(2, 1, 1)
        plt.plot(kvals, k_train_errors, "r-")
        plt.plot(kvals, k_hold_errors, "g-")
        plt.title("Total Errors for k-means clustering: US County classification")
        plt.xlabel("k-values")
        plt.ylabel("Total Error:\nTotal distance of points from center of cluster")
        plt.legend(["Total Error for training set", "Total Error for holdout set"])
        
        plt.subplot(2, 1, 2)
        plt.plot(kvals, k_hold_errors / k_train_errors, "b-")
        plt.xlabel("k-values")
        plt.ylabel("Total Error Ratio")
        plt.legend(["Ratio of total errors:\nHoldout set error / Training set error"])
        
        plt.show()
    
    if giveVals:
        return k_train_errors, k_hold_errors
    #graph shows drop in error for training and holdout as k increases, though training drops quicker (training becomes more precise)
    
def trackCounty(name, points, k=50, cutoff=0.1, pointType=County):
    
    clusters_w_county = {}
    for i in xrange(3):
        clusters, maxSmallest = kmeans(points, k, cutoff, County)
        
        for c in clusters:
            if c.contains(name) == True:
                clusters_w_county["Cluster {}".format(i)] = c.__str__()
    return clusters_w_county
    #county is clustering with similar counties every time, seem to match on income education level, etc.

def getAveragePoverty(cluster):
    """
    Given a Cluster object, finds the average poverty field over the members
    of that cluster.
    
    cluster: the Cluster object to check
    
    Returns: a float representing the computed average income value
    """
    tot = 0.0
    numElems = 0
    for c in cluster.getPoints():
        tot += c.getOriginalAttrs()[2]

    return float(tot) / len(cluster.getPoints())

def graphPredictionErr(points, dimension=14, kvals = [25, 50, 75, 100, 125, 150], cutoff = 0.1, plot=True, giveVals=False):
    """
    Given input points and a dimension to predict, should cluster on the
    appropriate values of k and graph the error in the resulting predictions,
    as described in Problem 3.
    """

	# Your Code Here
    k_poverty_errors = []
    
    for k in kvals:
        holdout, testing = randomPartition(points, 0.2)
        
        print ''
        clusters, maxSmallest = kmeans(testing, k, cutoff, County)
        
        poverty_error = 0.0
        for p in holdout:
            smallestDist = p.distance(clusters[0].getCentroid())
            closestCluster = clusters[0]
            for c in clusters:
                if p.distance(c.getCentroid()) < smallestDist:
                    smallestDist = p.distance(c.getCentroid())
                    closestCluster = c
            clusterAvgPov = getAveragePoverty(closestCluster)
            poverty_error += (p.getOriginalAttrs()[2] - clusterAvgPov)**2
            
        k_poverty_errors.append(poverty_error)
        
    k_poverty_errors = np.array(k_poverty_errors)
        
    ###
    if plot:
        plt.plot(kvals, k_poverty_errors, "r-")
        plt.title("Poverty error for k-means clustering: US County classification")
        plt.xlabel("k-values")
        plt.ylabel("Poverty Error:\nDistance of points from center of cluster")
        plt.legend(["Poverty Error for holdout points\ncompared to training set\
                        \nweights=[1.0, 1.0, 0.0, 0.1, 0.0, 0.2, 0.2, 0.4, 0.5, 0.8, 1.0, 0.2, 0.6, 0.0]"])
       
        plt.show()
    
    if giveVals:
        return k_poverty_errors
    #increase k, and error decreases (~ predictive power is increasing for holdout cases)
    #increasing number of clusters, more rep of differences in poverty levels
    
    #changing weight values can reduce errors of predictive models, diffiuclt in practice to know how to weigh multiple categories
    #with poverty, factors directly influencing finances such as income, home value, degree status will have more of an effect.
