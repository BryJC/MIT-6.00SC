# 6.00 Problem Set 11
#
# graph.py
#
# A set of data structures to represent graphs
#

class Node(object):
   def __init__(self, name):
       self.name = str(name)
   def getName(self):
       return self.name
   def __str__(self):
       return self.name
   def __repr__(self):
      return self.name
   def __eq__(self, other):
      return self.name == other.name
   def __ne__(self, other):
      return not self.__eq__(other)
   def __hash__(self):
       return hash(self.name) 

class Edge(object):
   def __init__(self, src, dest):
       self.src = src
       self.dest = dest
   def getSource(self):
       return self.src
   def getDestination(self):
       return self.dest
   def __str__(self):
       return str(self.src) + '->' + str(self.dest)

class Digraph(object):
   """
   A directed graph
   """
   def __init__(self):
       self.nodes = []
       self.edges = {}
   def addNode(self, node):
       if node in self.nodes:
           raise ValueError ("Duplicate Node")
       else:
           self.nodes.append(node)
           self.edges[node] = []
   def addEdge(self, edge):
       src = edge.getSource()
       dest = edge.getDestination()
       if not(src in self.nodes and dest in self.nodes):
           raise ValueError('Node not in graph')
       self.edges[src].append(dest)
   def childrenOf(self, node):
       return self.edges[node]
   def hasNode(self, node):
       for i in self.nodes:
           if i == node:
               return True
       return False
   def __str__(self):
       res = ''
       for k in self.edges:
           for d in self.edges[k]:
               res = res + str(k) + '->' + str(d) + '\n'
       return res[:-1]

###___###___###___###___###       

class WeightedEdge(Edge):
    """
    creates weighted edge object
    """
    def __init__(self, src, dest, weight, subweight):
       self.src = src
       self.dest = dest
       self.weight = int(weight)
       self.subweight = int(subweight)
    def getSource(self):
        return self.src
    def getDestination(self):
        return self.dest
    def getWeight(self):
        return self.weight
    def getSubWeight(self):
        return self.subweight
    def __str__(self):
        return str(self.src) + '->' + str(self.dest) + " weight:{}".format(str(self.weight))

class WeightedDigraph(Digraph):
    """
    creates weighted digraph object
    """
    def __init__(self):
    #ensure same initialization process as digraph object
        Digraph.__init__(self)
        
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        wgt = edge.getWeight()
        swgt = edge.getSubWeight()
        if not(src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        self.edges[src].append((dest, wgt, swgt))
    def calcPathLength(self, path):
        #need to add up distance and outside distance
        length = 0.0
        outside = 0.0
        for i in xrange(len(path)-1):
            start = self.edges[path[i]]
            for j in start:
                if j[0] == path[i+1]:
                    length += j[1]
                    outside += j[2]
        return length, outside
                
        
###___###___###___###___###        
