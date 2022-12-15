import re
import math as m

# open file and read
def read_file(file):
    edges = []
    node_dict = {}
    f = open(file, 'r')
    for x in f:
        first = x[0]
        if first == '#' or first == '\n':
            continue

        line_list = re.split(' |\t|\n', x.strip())
        linelength = len(line_list)
        if linelength == 3:
            node_dict[line_list[0]] = (int(line_list[1]), int(line_list[2]))
        elif linelength == 2:
            edges.append((line_list[0], line_list[1]))
    f.close()
    return (node_dict, edges)

def print_list(llist):
    s = ""
    if llist:
        for x in llist:
            s += x + " -> "
        s = s[:-4]
    return s

def calculate_weight(n1v, n2v):
        dist = m.sqrt((n1v[0] - n2v[0])**2 + (n1v[1] - n2v[1])**2)
        return dist

def check_edge_valid(nodes, edges):
    node_list = nodes.keys()
    for u in edges:
        if u[0] not in node_list or u[1] not in node_list:
            return False
    return True

def is_node_valid(nodes, start):
    node_list = nodes.keys()
    if start not in node_list:
        return False
    return True

def is_algo_valid(algo):
    if algo.lower() == "bfs":
        return True
    elif algo.lower() == "id":
        return True
    elif algo.lower() == "a_star":
        return True
    return False


