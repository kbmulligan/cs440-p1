# p1.py - find the maximum clique in a graph
# by K. Brett Mulligan
# 27 Aug 2014
# CSU CS440
# Dr. Asa Ben-Hur
##############################################

import itertools, copy

DO_TESTING = True
DO_VERBOSE_PARSING = False

prohibited_chars = ['{', '}', '/']

class Graph:

    name = ""               # id of graph
    edges = []              # list of edges
    amatrix = []            # adjacency matrix
    nodes = []              # list of node ids
    cliques = []            # list of Graph objects which are cliques for this graph
    
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
                    if DO_VERBOSE_PARSING:
                        print "\nRaw               :   ", gData.rstrip('\n')
                    
                    gData = gData.split(";")[0]                 # remove comment (everything after ";")
                    if DO_VERBOSE_PARSING:
                        print "Comment removed   :   ", gData

                    tokens = gData.split("--")                  # split on --
                    if DO_VERBOSE_PARSING:
                        print "Split along '--'' :     ", tokens

                    clean_tokens = [t.strip() for t in tokens]  # remove whitespace
                    if DO_VERBOSE_PARSING:
                        print "Whitespace removed:     ", clean_tokens        
                    
                    edge = remove_non_nodes(clean_tokens)       # remove prohibited chars
                    if DO_VERBOSE_PARSING:
                        print "Non-nodes removed :     ", edge

                    if edge and edge not in edges:
                        edges.append(edge)
                    
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
                if (node not in nodes):
                    nodes.append(node)
            
        return nodes # make this set(nodes) if the above code does not remove duplicates

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
        for edge in self.edges:                     # add each edge to the matrix
            self.put_edge_in_matrix(edge)

        for node in self.nodes:                     # add all nodes that didn't have an explicit edge for themselves
                if list(node) not in self.edges:
                    self.edges.append(list(node))

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
        to_remove = []
        for edge in self.edges:
            if node in edge:
                to_remove.append(edge)
        for edge in to_remove:
            self.edges.remove(edge)
        return

    def print_matrix(self):
        print '   ' + '  '.join(self.nodes)
        for x in range(self.get_size()):
            print self.nodes[x], self.amatrix[x]

    def is_clique(self):
        clique = True
        for y in self.get_matrix():
            for x in y:
                if (x == 0):
                    clique = clique and False        
        return clique

    def add_clique(self, cg):
        self.cliques.append(cg)
        return

    def get_cliques(self):
        return self.cliques

            
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

def remove_non_nodes (tokens):
    new_list = [x for x in tokens if x if x not in prohibited_chars]

    return new_list

def print_matrix(mat):
    for line in mat:
        print line

def print_edge (edge):
    print '--'.join(edge)
    
def maximum_clique(g):
    cliq = find_clique(g)

    # print "Found ", len(cliq.get_cliques()), " cliques!!!"
    sizes = []
    for graph in cliq.get_cliques():
        sizes.append(graph.get_size())
        # do_graph(graph)

    # print "Maximum cliques size was ", max(sizes)
    return max(sizes)


def remove_node(old_mat, index):
    mat = list(old_mat)
    if (len(mat) > 1):
        for y in range(len(mat)):
            mat[y].pop(index)           # remove index in each row
        mat.pop(index)                  # remove index row
    return mat

# returns graph g of clique it finds
def find_clique(gx):
    if gx.is_clique():
        # print "\nFound clique! SIZE: ", gx.get_size(), " See below..."
        # print "If branch"
        # do_graph(gx)
        
        # print "Find_clique complete...showing AND adding graph..."
        gx.add_clique(gx)

    else:
        # print "Not clique, still looking...", gx.num_nodes(), " nodes"
        # gx.print_matrix()

        for x in range(gx.num_nodes()):
            gn = copy.deepcopy(gx)
            gn.remove_node(x)
            # print "Removed node ", x, " ... finding clique again..."
            find_clique(gn)
        
        # print "End  else branch"
        #do_graph(gx)

    return copy.deepcopy(gx)
            

def do_graph(g):
    print "---------------\\\\"
    print g.get_name()
    g.print_edges()
    # print g.edges
    print "Nodes: " + str(g.num_nodes())
    print "Clique: " + str(g.is_clique())
    # print g.get_nodes()
    g.print_matrix()
    print "---------------//"

# g0 = Graph("graph.gv")
# g1 = Graph("graph1.gv")
# g2 = Graph("graph2.gv")
# g3 = Graph("graphex.gv")
# t0 = Graph("test1.gv")

# do_graph(g0)
# do_graph(g1)
# do_graph(g2)
# do_graph(g3)

# print "Start find clique ----------"
# cliq = find_clique(g0)
# do_graph(g0)

test_files = [   "graphex.gv",
                 "graph.gv", 
                 "graph1.gv", 
                 "graph2.gv",
                 "graph3.gv",
                 "graph4.gv",
                 ]

# if DO_TESTING:
#     for test in test_files:
#         print test, " -> ", maximum_clique(Graph(test))
test1 = "graph2.gv"
print test1, " -> ", maximum_clique(Graph(test1))

test = "graph1.gv"
print test, " -> ", maximum_clique(Graph(test))

