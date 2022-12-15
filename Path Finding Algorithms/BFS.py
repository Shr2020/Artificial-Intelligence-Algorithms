import Helper

def print_bfs_path(parent_dict, s):
    path = []
    path.append(s)
    source = False
    goal = s
    while source == False:
        p = parent_dict[goal]
        if p == None:
            source = True
        else:     
            path.append(p)
            goal = p

    path.reverse()
    return Helper.print_list(path)
    
    
def breadth_first_search(g, start, goal, verbose):
    visited = {} 
    parent = {}
    bfs_q = []
    bfs_q.append(start)
    visited[start] = True
    parent[start] = None
    sol_exist = False
    
    while bfs_q:
        current = bfs_q.pop(0)
        if verbose:
            print("Visiting: " + current + ". Path: " + print_bfs_path(parent, current))
        if current == goal:
            sol_exist = True
            print("Solution: " + print_bfs_path(parent, goal))
            break
        else:
            neighbours = g.graph[current]
            for u in neighbours:
                if u not in visited.keys():
                    parent[u] = current
                    bfs_q.append(u)
                    visited[u] = True
    if not sol_exist:
        print("The queue is Empty. Unable to reach goal. ")