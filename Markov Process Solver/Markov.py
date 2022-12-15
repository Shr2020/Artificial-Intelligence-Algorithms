import numpy as np

nodes_list = []
node_dict = {}
decision_node_dict = {}
chance_node_dict = {}
reward_dict = {}

def driver(nl, nd, dnd, cnd, rd, iter, df, tol, min):
    global nodes_list, node_dict, decision_node_dict, chance_node_dict, reward_dict
    nodes_list = nl
    node_dict = nd
    decision_node_dict = complete_decision_dict_node(nl, nd, cnd, dnd)
    chance_node_dict = complete_chance_node_dict(nl, nd, cnd)
    reward_dict = complete_reward_dict(rd, nl)
    policy = create_policy(node_dict)
    if decision_node_dict:
        mdp_solve(nodes_list, node_dict, decision_node_dict, chance_node_dict, reward_dict, policy, iter, df, tol, min)
    else:
        mrp(nodes_list, node_dict, chance_node_dict, reward_dict, iter, df, tol)
        
def print_policy(pol, decision_node_dict):
    for key in sorted(pol):
        if key in decision_node_dict:
            print(key, "->", pol[key])

def print_v_values(v):
    for key in sorted(v):
        print(key, "=", round(v[key], 5))

def complete_chance_node_dict(nlist, ndict, cnd):
    chance_ndict = cnd.copy()
    for node in nlist:
        if node in ndict and len(ndict[node]) == 1:
            chance_ndict[node] = [1.0]
    return chance_ndict

def complete_decision_dict_node(nlist, ndict, cnd, dnd):
    decision_ndict = dnd.copy()
    for node in nlist:
        if node in ndict and (node not in cnd and node not in dnd):
            decision_ndict[node] = 1
    
    for node in nlist:
        if node in ndict and len(ndict[node]) == 1:
            decision_ndict.pop(node)

    return decision_ndict

def complete_reward_dict(rd, nl):
    rewards = rd.copy()
    for node in nl:
        if node not in rd:
            rewards[node] = 0.0
    return rewards

def create_policy(node_dict):
    policy = {}
    for key, edges in node_dict.items():
        policy[key] = edges[0]
    return policy

def get_cnp(chance_node_dict, edge_from, edge_to):
    lnodes = node_dict[edge_from]
    cnps = chance_node_dict[edge_from]
    for ind, n in enumerate(lnodes):
        if n == edge_to :
            return cnps[ind] * lnodes.count(n)

def get_dnp(decision_node_dict, edge_from, edge_to, policy):
    # list of edges
    lnodes = node_dict[edge_from]
    # decision node according to policy
    decision_to = policy[edge_from]
    # success prob to decision node
    success = decision_node_dict[edge_from]
    # occurence of edge_to in lnodes
    count_edge_to = lnodes.count(edge_to)
    # occurence of edge_to in lnodes
    count_decision_n = lnodes.count(decision_to)
    if edge_to == decision_to:
        return success
    else:
        num_nodes_fail = len(lnodes) - count_decision_n
        val = count_edge_to * ((1.0 - success)/num_nodes_fail)
        return val


def get_rew(reward_dict, edge):
    return reward_dict[edge]

def create_vdict(node_list):
    v = {}
    for n in node_list:
        v[n] = 0
    return v


def calc_max_diff(v1, v2, nl):
    max_diff =  -1
    for n in nl:
        if abs(v1[n] - v2[n]) > max_diff:
            max_diff = abs(v1[n] - v2[n])
    return max_diff

def mrp(nodes_list, node_dict, chance_node_dict, reward_dict, iter, df, tol):
    #{A:0, B:0, C:0}
    vnew = create_vdict(nodes_list).copy()

    #{A:0, B:0, C:0} 
    v = create_vdict(nodes_list).copy()

    for x in range(iter):
        # nodes_list: [E, A, B, C, D]. node_dict: {E : [A, B, D], A : [B, E]}
        for edge_from in nodes_list:
            rew = get_rew(reward_dict, edge_from)

            if edge_from not in node_dict:
                # terminal node
                v[edge_from] = rew
                continue
            
            # array: [A, B, D]
            possible_states = list(set(node_dict[edge_from]))

            if edge_from in chance_node_dict:
                #chance_node
                temp = [(df * get_cnp(chance_node_dict, edge_from, edge_to) * vnew[edge_to]) for edge_to in possible_states]
                v[edge_from] = rew + np.sum(temp)
    
        if calc_max_diff(v, vnew, nodes_list) < tol:
            break
        vnew = v.copy()
    print()
    print_v_values(v)

def mdp_solve(nodes_list, node_dict, decision_node_dict, chance_node_dict, reward_dict, pol, iter, df, tol, min):
    policy = pol.copy()
    new_policy = {}

    #{A:0, B:0, C:0}
    vnew = create_vdict(nodes_list).copy()

    #{A:0, B:0, C:0} 
    v = create_vdict(nodes_list).copy()

    it = True
    while(it):
        for x in range(iter):
            # nodes_list: [E, A, B, C, D]. node_dict: {E : [A, B, D], A : [B, E]}
            for edge_from in nodes_list:
                rew = get_rew(reward_dict, edge_from)

                if edge_from not in node_dict:
                    # terminal node
                    v[edge_from] = rew
                    continue
                
                # array: [A, B, D] TODO: make it so that entrirs are unique
                possible_states = list(set(node_dict[edge_from]))

                if edge_from in chance_node_dict:
                    #chance_node
                    temp = [(df * get_cnp(chance_node_dict, edge_from, edge_to) * vnew[edge_to]) for edge_to in possible_states]
                    v[edge_from] = rew + np.sum(temp)
                    continue    

                # decision node
                temp = [(df * get_dnp(decision_node_dict, edge_from, edge_to, policy) * vnew[edge_to]) for edge_to in possible_states]
                v[edge_from] = rew + np.sum(temp)
        
            if calc_max_diff(v, vnew, nodes_list) < tol:
                break
            vnew = v.copy()
    
        if min:
            new_policy = {i:node_dict[i][np.argmin([vnew[x] for x in node_dict[i]])] for i in policy}
        else:
            new_policy = {i:node_dict[i][np.argmax([vnew[x] for x in node_dict[i]])] for i in policy}

        if policy == new_policy:
            it = False
        else:
            policy = new_policy.copy()
    print()
    print_policy(policy, decision_node_dict)
    print()
    print_v_values(v)




