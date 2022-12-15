import re
import math as m

# open file and read
def read_file(file):
    nodes_list = []
    node_dict = {}
    decision_node_dict = {}
    chance_node_dict = {}
    reward_dict = {}
    f = open(file, 'r')
    for x in f:
        first = x[0]
        if first == '#' or first == '\n':
            continue
        if "=" in x:
            reward_dict = handle_rewards(x, reward_dict)
        elif "%" in x:
            chance_node_dict, decision_node_dict = handle_chance_and_decision_nodes(x, chance_node_dict, decision_node_dict)
        elif ":" in x:
            nodes_list, node_dict = handle_nodes(x, nodes_list, node_dict)
    f.close()

    return (nodes_list, node_dict, decision_node_dict, chance_node_dict, reward_dict)

def handle_rewards(line, reward_dict):
    llist = re.split('\s+|\t+|\n', line.replace("="," ").strip())
    reward_dict[llist[0]] = float(llist[1])
    return reward_dict

def handle_chance_and_decision_nodes(line, chance_node_dict, decision_node_dict):
    llist = re.split('\s+|\t|\n', line.replace("%"," ").strip())
    if len(llist) == 2:
        # decision node
        decision_node_dict[llist[0]] = float(llist[1])
    else:
        # chance node
        l = []
        for i in range(1, len(llist)):
            l.append(float(llist[i]))
        chance_node_dict[llist[0]] = l
    
    return (chance_node_dict, decision_node_dict)

def handle_nodes(line, node_list, node_dict):
    llist = re.split('\s+|\t|\n|\s*,\s*', line.replace(":"," ").replace("["," ").replace("]"," ").strip())
    
    if llist[0] not in node_list:
        node_list.append(llist[0])
    
    l = []
    for i in range(1, len(llist)):
        if llist[i] not in node_list:
            node_list.append(llist[i])
        l.append(llist[i])
    
    node_dict[llist[0]] = l

    return(node_list, node_dict)

def check_terminal_nodes(node_dict, nodes_list, decision_node_dict, chance_node_dict):
    for node in nodes_list:
        if node not in node_dict:
            if node in decision_node_dict or node in chance_node_dict:
                print("Terminal node:", node, "has probability entry. Invalid Input File.")
                return False
    return True

def check_nodes(nodes_list):
    for node in nodes_list:
        if not node.isalnum():
            print("State", node, "is not alphanumeric. Nodes/States should be alphanumeric.")
            return False
    return True



