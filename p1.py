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
    nodes = []
    
    def __init__(self, fn):
        self.edges, self.name = read_graph(fn)

        self.nodes = list(self.get_nodes())

        self.amatrix = [ [0 for i in range(self.num_nodes())] for j in range(self.num_nodes()) ]

        self.init_edges()
        
        
    def get_name(self):
        return self.name
    
    def print_edges(self):
        for edge in self.edges:
            print_edge(edge)
            
    def num_nodes(self):
        return len(self.nodes)
        
    def get_nodes(self):
        nodes = []
        for edge in self.edges:
            for node in edge:
                nodes.append(node)
            
        return set(nodes)

    def get_node_index(self, node_id):
        return self.nodes.index(node_id)

    def get_node_id(self, node_index):
        return self.nodes[node_index]

    def put_edge_in_matrix (self, edge):
        if (len(edge) > 1):
            self.amatrix[self.get_node_index(edge[0])][self.get_node_index(edge[1])] = 1    # do edge
            self.amatrix[self.get_node_index(edge[1])][self.get_node_index(edge[0])] = 1    # do reciprocal
            self.amatrix[self.get_node_index(edge[0])][self.get_node_index(edge[0])] = 1    # do first node
            self.amatrix[self.get_node_index(edge[1])][self.get_node_index(edge[1])] = 1    # do second node
        else:
            self.amatrix[self.get_node_index(edge[0])][self.get_node_index(edge[0])] = 1

    def init_edges(self):
        for edge in self.edges:
            self.put_edge_in_matrix(edge)
            
    
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

                #tokens = tokens.split("--")

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

def print_matrix(mat):
    for line in mat:
        print line
    
def maximum_clique(g):
    return 1

def is_clique(g):
    clique = True
    for line in g.amatrix:
        if 0 in line:
            clique = clique and False        
    return clique

def do_graph(gfn):
    g = Graph(gfn)
    print ""
    print g.get_name()
    g.print_edges()
    print "Nodes: " + str(g.num_nodes())
    # print g.get_nodes()
    print_matrix(g.amatrix)
    print "Clique: " + str(is_clique(g))

do_graph("graph.gv")
do_graph("graph2.gv")
do_graph("graphex.gv")
do_graph("graph1.gv")

