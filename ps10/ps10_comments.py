# Problem Set 10
# Name:
# Collaborators:
# Time:

#Code shared across examples
import numpy as np, random, string, copy, math
import matplotlib.pyplot as plt 
  
    



#def randomPartition(l, p):
#    """
#    Splits the input list into two partitions, where each element of l is
#    in the first partition with probability p and the second one with
#    probability (1.0 - p).
#    
#    l: The list to split
#    p: The probability that an element of l will be in the first partition
#    
#    Returns: a tuple of lists, containing the elements of the first and
#    second partitions.
#    """
#    l1 = []
#    l2 = []
#    for x in l:
#        if random.random() < p:
#            l1.append(x)
#        else:
#            l2.append(x)
#    return (l1,l2)


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
random.seed(123)
testPoints = random.sample(points, len(points)/10)

##########
    
    
def graphRemovedErr(points, kvals = [25, 50, 75, 100, 125, 150], cutoff = 0.1):
    """
    Should produce graphs of the error in training and holdout point sets, and
    the ratio of the error of the points, after clustering for the given values of k.
    For details see Problem 1.
    """

    # Your Code Here


def graphPredictionErr(points, dimension, kvals = [25, 50, 75, 100, 125, 150], cutoff = 0.1):
    """
    Given input points and a dimension to predict, should cluster on the
    appropriate values of k and graph the error in the resulting predictions,
    as described in Problem 3.
    """

	# Your Code Here
    
