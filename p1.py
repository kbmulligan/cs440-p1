# p1.py - find the maximum clique in a graph
# by K. Brett Mulligan
# 27 Aug 2014
# CSU CS440
# Dr. Asa Ben-Hur
##############################################

prohibited_chars = ['{', '}', '/']

class Graph:

    name = ""
    edges = []
    amatrix = []
    
    def __init__(self, fn):
        self.edges, self.name = read_graph(fn)

    def maximum_clique(self):
        return 1
    
    def get_name(self):
        return self.name
    
    def print_edges(self):
        for edge in self.edges:
            print_edge(edge)
            
    def num_nodes(self):
        return len(self.get_nodes())
        
    def get_nodes(self):
        nodes = []
        for edge in self.edges:
            for node in edge:
                nodes.append(node)
            
        return set(nodes)
    
def read_graph (filename):

    name = ''
    edges = []

    gf = open(filename, 'r')
    if gf == None:
        print "Error: Could not open points file."
    else:
        
        title = gf.readline()                        # read title
        if title != "":
            name = title.strip("\n {")
            
        for line in gf:                              # read edges
            if line != "":
                gData = line
                #print gData
                
                gData = gData.split(";")[0]          # remove comment (everything after ";")
                #print gData
                
                tokens = gData.split()               # remove whitespace
                #print tokens

                edge = remove_non_nodes(tokens)

                if edge[0] not in prohibited_chars:
                    edges.append(edge)
                    #print edge
                
    gf.close()
    return edges, name

def remove_non_nodes (tokens):
    newList = []
    
    for x in tokens:
        if x != '--':
            newList.append(x)

    return newList

def print_edge (edge):
    print '--'.join(edge)


def put_edge_in_matrix (edge, matrix):
    pass

def maximum_clique(g):
    return 1
    
g1 = Graph("graph.gv")
print g1.get_name()
g1.print_edges()
print g1.get_nodes()
print g1.num_nodes()

g2 = Graph("graph2.gv")
print g2.get_name()
g2.print_edges()
print g2.get_nodes()
print g2.num_nodes()
