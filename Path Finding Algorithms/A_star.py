import Helper

# calculates the distance of nodes from goal
def calculate_h(node_dict, goal):
    heuristics = {} 
    n2v = node_dict[goal]
    for n in node_dict:
        n1v = node_dict[n]
        dist = Helper.calculate_weight(n1v, n2v)
        heuristics[n] = round(dist, 2)
    return heuristics

def A_star(gr, node_dict, start, goal, verbose):
    
    # heuristics
    h = calculate_h(node_dict, goal)
    
    # sets containing nodes that could be expanded and not.
    openList = []
    
    visited = {}
    
    # f and g functions. f = g + h
    g = {} 
    f = {}
    
    # set all values to infinity
    for n in node_dict:
        g[n] = float('inf')
        f[n] = float('inf')
    
    # set start values.
    g[start] = 0
    f[start] = h[start]
    
    openList.append(([start],f[start]))
    
    while openList:
        current_path, current_node_f = min(openList,key=lambda x:x[1])
        if verbose:
            print("adding", Helper.print_list(current_path))
        openList.remove((current_path, current_node_f))
        current_node = current_path[-1]
        visited.setdefault(current_node, f[current_node])
        neighbours = gr.graph[current_node]

        for neighbour in neighbours:
            if neighbour in current_path:
                continue
            path_to_neighbour = current_path + [neighbour]
            current_lowest_f_to_neighbour = visited.get(neighbour, f[neighbour])
            g_tent = sum([Helper.calculate_weight(node_dict[path_to_neighbour[i]], node_dict[path_to_neighbour[i+1]]) for i in range(len(path_to_neighbour)-1)])
            f_tent = round(g_tent + h[neighbour],2)

            if verbose:
                print("{0} g={1:0.2f}, h={2:0.2f}, f={3:0.2f}".format(Helper.print_list(path_to_neighbour), g_tent,h[neighbour], f_tent))
            
            if neighbour == current_node:
                continue
            
            openList.append((path_to_neighbour, f_tent))
            
            if f_tent < current_lowest_f_to_neighbour:
                # We found a better path
                f[neighbour] = f_tent
            
            if neighbour == goal:
                openList.clear()
                visited[goal] = (path_to_neighbour, f[neighbour])
                break
        
        if not openList:
            break
    
    if goal not in visited:
        print("No Path found.")
    
    else:
        print("Solution: ", Helper.print_list(visited[goal][0]))