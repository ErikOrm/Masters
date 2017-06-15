import pulp
import math


def sub_problem2(n, car, m, pi, gamma, t):
    
    
    #initialise the model
    
    T = 20
    startTime = 0
    M = 30
    
    # sets
    o_nodes = ["n%i" % (i+1) for i in range(n)]
    d_nodes = ["n%i" % (i+1) for i in range(n,2*n)]
    k_nodes = ["n%i" % (i+1) for i in range(2*n, 2*n+m)]
    z_nodes = ["n%i" % (2*n+m+1)]
    nodes =  o_nodes + d_nodes + k_nodes + z_nodes
    
    
    #t = {(i,j):1 for i in nodes for j in nodes}
    q = {i:0 for i in nodes}
    for i in o_nodes:
        q[i] = 1
    for i in d_nodes:
        q[i] = - 1
    
    
    path = [k_nodes[car], z_nodes[0]]
    cost = 0
    added = True
    free_nodes = [x for x in range(n)]
    while added:
        added = False
        for i in free_nodes:
            print("i:%i" % i)
            o = o_nodes[i]
            d = d_nodes[i]
            best_cost = 0
            best_path = path
            for j in range(1,len(path)):
                for k in range(j,len(path)):
                    print("j,k: %i%i" % (j,k))
                    tmp_cost = 0
                    tmp_path = path[:j] + [o] + path[j:k] + [d] + path[k:]
                    tmp_Q = 0
                    fail = 0
                    time = 0
                    for node in tmp_path:
                        tmp_Q = tmp_Q + q[node]
                        if tmp_Q >= 4:
                            fail = 1
                    if fail:
                        tmp_cost = 1000
                    else:
                        for l in range(len(tmp_path)-1):
                            time = time + t[(tmp_path[l],tmp_path[l+1])]
                            if tmp_path[l+1] in d_nodes:
                                tmp_cost = tmp_cost + time - pi[tmp_path[l+1]].value()
                    print(tmp_cost)
                    print(tmp_path)
                    if tmp_cost < best_cost:
                        best_cost = tmp_cost
                        best_path = tmp_path
            if best_cost < cost:
                path = best_path
                cost = best_cost
                free_nodes.remove(i)
                added = True
                break
    c = 0
    for i in range(len(path)-1):
        time = time + t[(path[i],path[i+1])]
        if tmp_path[l+1] in d_nodes:
            c = tmp_cost + time

    return(path, cost-gamma['c%i' % (car+1)].value(), c)