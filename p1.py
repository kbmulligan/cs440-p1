# p1.py - find the maximum clique in a graph
# by K. Brett Mulligan
# 27 Aug 2014
# CSU CS440
# Dr. Asa Ben-Hur
##############################################

import itertools, copy, re

DO_TESTING = False
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
                        print "\nRaw                 :   ", gData.rstrip('\n')
                    
                    if gData[0:2] == '/*':
                        gData = ''
                        if DO_VERBOSE_PARSING:
                            print "There's a comment only line!!!"


                    gData = gData.split(";")[0]                 # remove everything after ";")
                    if DO_VERBOSE_PARSING:
                        print "All after ; removed :   ", gData

                    tokens = gData.split("--")                  # split on --
                    if DO_VERBOSE_PARSING:
                        print "Split along '--''   :     ", tokens

                    clean_tokens = [t.strip() for t in tokens]  # remove whitespace
                    if DO_VERBOSE_PARSING:
                        print "Whitespace removed  :     ", clean_tokens        
                    
                    edge = [x for x in clean_tokens if x if x not in prohibited_chars]       # remove prohibited chars
                    if DO_VERBOSE_PARSING:
                        print "Non-nodes removed   :     ", edge

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
            self.print_edge(edge)

    def print_edge (self, edge):
        print '--'.join(edge)
            
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
            
        return nodes

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

        # for node in self.nodes:                     # add all nodes that didn't have an explicit edge for themselves
        #         if list(node) not in self.edges:
        #             self.edges.append(list(node))

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
        if cg not in self.cliques:
            self.cliques.append(cg)
        return

    def get_cliques(self):
        return self.cliques

    # given 2 node indices, returns true if they are connected
    def nodes_connected(self, n1, n2):
        adjacent = False
        if (self.amatrix[n1][n2] == 1):
            adjacent = True
        else:
            pass
        return adjacent

    # given 2 node id's, returns true if they are connected
    def nodes_connected_id(self, id1, id2):
        return self.nodes_connected(self.get_node_index(id1), self.get_node_index(id2))

    # given a node and a list of nodes, return true if that node is connected to all nodes in list
    def node_connected_to_list(self, node_a, nodes_list):
        connected = True

        for node in nodes_list:
            if self.nodes_connected_id(node_a, node):
                connected = connected and True
            else:
                connected = connected and False
        
        return connected


    # returns combination object of all node combinations with 1 node removed
    def node_combinations(self):
        return itertools.combinations(self.get_nodes(), self.get_size()-1)

    def generate_all_node_combinations(self):
        all_combinations = []

        for x in range(1, self.get_size()+1):
            combos_length_x = itertools.combinations(self.get_nodes(), x)
            all_combinations.extend(combos_length_x)

        return all_combinations


    def find_cliques(self):
        cliques = []

        all_combos = self.generate_all_node_combinations()

        for combo in all_combos:
            if (self.is_combo_clique(combo)) and (combo not in cliques):
                cliques.append(combo)

        self.cliques = cliques

        return cliques

    def is_combo_clique(self, combo):
        connected = False
        if (len(combo) == 1):
            connected = True
        elif (len(combo) == 2):
            connected = self.nodes_connected_id(combo[0], combo[1])
        else:
            connected = self.node_connected_to_list(combo[0], combo[:]) and self.is_combo_clique(combo[1:])
        return connected



    def get_max_clique(self):

        self.find_cliques()

        max_cliq = ''
        max_size = 0

        sizes = [len(cliq) for cliq in self.get_cliques()]

        for cliq in self.get_cliques():
            if (len(cliq) > max_size):
                max_size = len(cliq)
                max_cliq = cliq

        # print "Cliques: ", self.get_cliques()
        # print "Clique sizes: ", sizes
        # print "Maximum cliques size was ", max_size

        return max_cliq

################ END CLASS GRAPH ################################

# GRAPH CREATORS            
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

    
def maximum_clique(g):                          # standalone function that returns max clique of graph
    return len(g.get_max_clique())


def do_graph(g):
    print "---------------\\\\"
    print g.get_name()
    g.print_edges()
    print "Nodes: " + str(g.num_nodes())
    print "Clique: " + str(g.is_clique())
    g.print_matrix()
    print "---------------//"


################ TESTING ###############################

test_files = [   "graph.gv", 
                 "graph0.gv",
                 "graph1.gv", 
                 "graph2.gv",
                 "graph3.gv",
                 "graph4.gv",
                 "graph5.gv",
                 "graphex.gv",
                 "file3.gv",
                 "file4.dot",
                 "file5.dot",
                 "file6.dot"
                 ]

if DO_TESTING:
    for test in test_files:
        print test , " -> ", maximum_clique(Graph(test))

