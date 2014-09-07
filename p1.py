# p1.py - find the maximum clique in a graph
# by K. Brett Mulligan
# 27 Aug 2014
# CSU CS440
# Dr. Asa Ben-Hur
##############################################

import itertools

prohibited_chars = ['{', '}', '/']

class Graph:

    name = ""
    edges = []
    amatrix = []
    nodes = []
    
    def __init__(self, fn):
        if (fn != ''):
            self.edges, self.name = self.read_graph(fn)
            self.nodes = list(self.get_nodes())
            self.amatrix = [ [0 for i in range(self.num_nodes())] for j in range(self.num_nodes()) ]
            self.init_edges()
            
        else:
            self.name = ''

    def read_graph (self, filename):

        name = ''
        edges = []

        gf = open(filename, 'r')
        if gf == None:
            print "Error: Could not open file."
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
        
    def get_name(self):
        return self.name

    def get_matrix(self):
        return list(self.amatrix)
        
    def get_edges(self):
        return list(self.edges)
    
    def print_edges(self):
        for edge in self.edges:
            print_edge(edge)
            
    def num_nodes(self):
        return len(self.nodes)

    def get_size(self):
        return self.num_nodes()
        
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

    def remove_node(self, index):
        to_remove = self.get_node_id(index)         # get id first
        self.remove_edges_with_node(to_remove)      # remove edges
        self.nodes.remove(to_remove)                # remove node

        if (len(self.amatrix) > 1):                 # adjust matrix
            for y in range(len(self.amatrix)):
                self.amatrix[y].pop(index)          # remove index in each row
            self.amatrix.pop(index)                 # remove index row
        return

    def remove_edges_with_node(self, node):
        return

    def print_matrix(self):
        print '   ' + '  '.join(self.nodes)
        for x in range(self.get_size()):
            print self.nodes[x], self.amatrix[x]

            
def graph_from_edges(new_edges):
    g = Graph('')
    g.edges = list(new_edges)
    g.nodes = list(self.get_nodes())
    g.amatrix = [ [0 for i in range(self.num_nodes())] for j in range(self.num_nodes()) ]
    g.init_edges()
    return g

def graph_from_matrix(new_matrix):
    g = Graph('')
    g.name = "_dyn"
    g.amatrix = list(new_matrix)
    g.nodes = list(range(len(g.amatrix)))
    return g
    
def graph_from_graph(parent):
    g = Graph('')
    g.name = parent.name
    g.amatrix = list(parent.get_matrix())
    g.nodes = list(range(len(g.amatrix)))
    g.edges = list(parent.get_edges())
    return g
    
def read_graph (filename):

    name = ''
    edges = []

    gf = open(filename, 'r')
    if gf == None:
        print "Error: Could not open file."
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

def print_matrix(mat):
    for line in mat:
        print line

def print_edge (edge):
    print '--'.join(edge)
    
def maximum_clique(g):
    return 1

def is_clique(g):
    clique = True
    for y in g.get_matrix():
        for x in y:
            if (x == 0):
                clique = clique and False        
    return clique

def remove_node(old_mat, index):
    mat = list(old_mat)
    if (len(mat) > 1):
        for y in range(len(mat)):
            mat[y].pop(index)           # remove index in each row
        mat.pop(index)                  # remove index row
    return mat

# returns graph g of clique it finds
def find_clique(gx):
    if is_clique(gx):
        print "\nFound clique! See below..."
        print "If branch"
        do_graph(gx)
        print "Find_clique complete...showing graph..."
    else:
        print "Not clique, still looking...", gx.num_nodes(), " nodes"
        print_matrix(gx.get_matrix())
        gx.remove_node(gx.num_nodes()-1)
        find_clique(gx)
        print "Else branch"
        do_graph(gx)

    return graph_from_graph(gx)
            

def do_graph(g):
    print "...Doing graph"
    print g.get_name()
    g.print_edges()
    print "Nodes: " + str(g.num_nodes())
    # print g.get_nodes()
    g.print_matrix()
    print "Clique: " + str(is_clique(g))

g0 = Graph("graph.gv")
g1 = Graph("graph1.gv")
g2 = Graph("graph2.gv")
g3 = Graph("graphex.gv")

do_graph(g0)
do_graph(g1)
do_graph(g2)
do_graph(g3)

# print "Start find clique ----------"
# cliq = find_clique(g0)
# do_graph(g0)

cliq = find_clique(g0)
