
from string import split
from graph import WeightedDigraph as WD, Digraph, WeightedEdge as WE, Edge, Node
 

def load_map(mapFname):
    #TODO
    print "Loading map from file..."
    dataFile = open(mapFname, 'r') #open mit_map.txt in read-only mode, assign it to dataFile variable
    
    travel_map = WD() #create empty weighted directed graph
    
    node_dic = {}
    edge_list = []
    
    for line in dataFile:
        if len(line) == 0 or line[0] == '#': #skip null or comment lines
            continue
        src, dest, distance, outside_distance = line.split() #pull relevant data from line
        
        if src not in node_dic:
            node_dic[src] = Node(src)
        if dest not in node_dic:
            node_dic[dest] = Node(dest)
        
        edge_list.append((src, dest, distance, outside_distance))
    
    for node in node_dic.values():
        travel_map.addNode(node)    
    for edge in edge_list:
        start = node_dic[edge[0]] 
        end = node_dic[edge[1]]
        WEdge = WE(start, end, edge[2], edge[3])
        travel_map.addEdge(WEdge)
        
    dataFile.close()
        
    return travel_map
    

#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and the constraints
#

def bruteForceSearch(map_digraph, start, end, maxTotalDist, maxDistOutdoors, visited = [], toPrint = True):    

    #TODO
    if toPrint: 
        print start, end 
    if not (map_digraph.hasNode(start) and map_digraph.hasNode(end)): 
        raise ValueError('Start or end building not in graph.') 
    path = [str(start)] 
    if start == end: 
        return path 
    shortest = None 
    for building in map_digraph.childrenOf(start):
    #here building == a tuple (child, weight, sub_weight) 
        if (str(building[0]) not in visited): 
            visited = visited + [str(building[0])] #new list
            if toPrint:
                print visited 
            newPath = shortestPath(map_graph, building[0], end, visited, toPrint) 
            if newPath == None: 
                continue 
            if (shortest == None or len(newPath) < len(shortest)): 
                shortest = newPath 
    if shortest != None: 
        path = path + shortest 
    else: 
        path = None 
    return path 

#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """ 
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDisOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO
    pass

# Uncomment below when ready to test
##if __name__ == '__main__':
##    # Test cases
##    digraph = load_map("mit_map.txt")
##
##    LARGE_DIST = 1000000
##
##    # Test case 1
##    print "---------------"
##    print "Test case 1:"
##    print "Find the shortest-path from Building 32 to 56"
##    expectedPath1 = ['32', '56']
##    brutePath1 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
##    dfsPath1 = directedDFS(digraph, '32', '56', LARGE_DIST, LARGE_DIST)
##    print "Expected: ", expectedPath1
##    print "Brute-force: ", brutePath1
##    print "DFS: ", dfsPath1
##
##    # Test case 2
##    print "---------------"
##    print "Test case 2:"
##    print "Find the shortest-path from Building 32 to 56 without going outdoors"
##    expectedPath2 = ['32', '36', '26', '16', '56']
##    brutePath2 = bruteForceSearch(digraph, '32', '56', LARGE_DIST, 0)
##    dfsPath2 = directedDFS(digraph, '32', '56', LARGE_DIST, 0)
##    print "Expected: ", expectedPath2
##    print "Brute-force: ", brutePath2
##    print "DFS: ", dfsPath2
##
##    # Test case 3
##    print "---------------"
##    print "Test case 3:"
##    print "Find the shortest-path from Building 2 to 9"
##    expectedPath3 = ['2', '3', '7', '9']
##    brutePath3 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
##    dfsPath3 = directedDFS(digraph, '2', '9', LARGE_DIST, LARGE_DIST)
##    print "Expected: ", expectedPath3
##    print "Brute-force: ", brutePath3
##    print "DFS: ", dfsPath3
##
##    # Test case 4
##    print "---------------"
##    print "Test case 4:"
##    print "Find the shortest-path from Building 2 to 9 without going outdoors"
##    expectedPath4 = ['2', '4', '10', '13', '9']
##    brutePath4 = bruteForceSearch(digraph, '2', '9', LARGE_DIST, 0)
##    dfsPath4 = directedDFS(digraph, '2', '9', LARGE_DIST, 0)
##    print "Expected: ", expectedPath4
##    print "Brute-force: ", brutePath4
##    print "DFS: ", dfsPath4
##
##    # Test case 5
##    print "---------------"
##    print "Test case 5:"
##    print "Find the shortest-path from Building 1 to 32"
##    expectedPath5 = ['1', '4', '12', '32']
##    brutePath5 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
##    dfsPath5 = directedDFS(digraph, '1', '32', LARGE_DIST, LARGE_DIST)
##    print "Expected: ", expectedPath5
##    print "Brute-force: ", brutePath5
##    print "DFS: ", dfsPath5
##
##    # Test case 6
##    print "---------------"
##    print "Test case 6:"
##    print "Find the shortest-path from Building 1 to 32 without going outdoors"
##    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
##    brutePath6 = bruteForceSearch(digraph, '1', '32', LARGE_DIST, 0)
##    dfsPath6 = directedDFS(digraph, '1', '32', LARGE_DIST, 0)
##    print "Expected: ", expectedPath6
##    print "Brute-force: ", brutePath6
##    print "DFS: ", dfsPath6
##
##    # Test case 7
##    print "---------------"
##    print "Test case 7:"
##    print "Find the shortest-path from Building 8 to 50 without going outdoors"
##    bruteRaisedErr = 'No'
##    dfsRaisedErr = 'No'
##    try:
##        bruteForceSearch(digraph, '8', '50', LARGE_DIST, 0)
##    except ValueError:
##        bruteRaisedErr = 'Yes'
##    
##    try:
##        directedDFS(digraph, '8', '50', LARGE_DIST, 0)
##    except ValueError:
##        dfsRaisedErr = 'Yes'
##    
##    print "Expected: No such path! Should throw a value error."
##    print "Did brute force search raise an error?", bruteRaisedErr
##    print "Did DFS search raise an error?", dfsRaisedErr
##
##    # Test case 8
##    print "---------------"
##    print "Test case 8:"
##    print "Find the shortest-path from Building 10 to 32 without walking"
##    print "more than 100 meters in total"
##    bruteRaisedErr = 'No'
##    dfsRaisedErr = 'No'
##    try:
##        bruteForceSearch(digraph, '10', '32', 100, LARGE_DIST)
##    except ValueError:
##        bruteRaisedErr = 'Yes'
##    
##    try:
##        directedDFS(digraph, '10', '32', 100, LARGE_DIST)
##    except ValueError:
##        dfsRaisedErr = 'Yes'
##    
##    print "Expected: No such path! Should throw a value error."
##    print "Did brute force search raise an error?", bruteRaisedErr
##    print "Did DFS search raise an error?", dfsRaisedErr
