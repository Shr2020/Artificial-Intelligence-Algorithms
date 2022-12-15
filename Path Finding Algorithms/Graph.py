import math as m
from collections import defaultdict

# class representing graph
class Graph:

    def __init__(self):
        self.graph = defaultdict(list)
        self.weight_map = {}
    
    def addEdge(self, node_dict, n1, n2):
        self.graph[n1].append(n2)
        self.graph[n2].append(n1)
        wt = self.calculate_weight(node_dict, n1, n2)
        self.weight_map[(n1,n2)] = wt
        self.weight_map[(n2,n1)] = wt
        
    def calculate_weight(self, node_dict, n1, n2):
        n1v = node_dict.get(n1)
        n2v = node_dict.get(n2)
        dist = m.sqrt((n1v[0] - n2v[0])**2 + (n1v[1] - n2v[1])**2)
        return round(dist,2)
        
    def add_edges(self, node_dict, node_list):
        for nodes in node_list:
            self.addEdge(node_dict, nodes[0], nodes[1])
            
    def sort_edges(self):
        for n in self.graph:
            self.graph[n] = list(set(self.graph[n]))
            self.graph[n].sort()
