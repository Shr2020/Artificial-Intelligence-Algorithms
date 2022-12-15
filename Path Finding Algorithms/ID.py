import Helper

def ID_Helper(g, src, target, i, maxDepth, path, final_path, visited):
    
    if maxDepth < i : 
        return False
    
    if src == target:
        return True
    
    if (i == maxDepth):
        path.append("hit depth=" + str(maxDepth) + ": " + src)
    else: 
        path.append("Expand: " + src)

    visited[src] = True

    for s in g.graph[src]:
        j = i
        if s in visited.keys():
            continue
        if(ID_Helper(g, s,  target, j+1, maxDepth, path, final_path, visited)):
            final_path.append(s)
            return True
    return False

def iterative_deepening(g, src, target, depth, verbose):
    sol_exist = False
    max_depth = depth
    final_path = []
    if verbose:
        print("Initial depth set to " + str(depth) + ". max depth: " + str(depth))
    while sol_exist == False:
        path = []
        visited = {}
        if (ID_Helper(g, src, target, 0, max_depth, path, final_path, visited)):
            final_path.append(src)
            sol_exist = True
            if verbose:
                for p in path:
                    print(p)
        else:
            if verbose:
                for p in path:
                    print(p)
                print("Increasing Depth by 1. max depth: " + str(max_depth+1))
            max_depth += 1
    if (sol_exist):
        final_path.reverse()
        print("Soultion: " + Helper.print_list(final_path))