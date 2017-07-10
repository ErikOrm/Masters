import pulp
import math


def sub_problem2(n, car, m, l, passengers, arr_time, starting_times, pi, gamma, t, T, Qmax, err_penalty):
    
    
    #initialise the model

    # sets
    o_nodes = ["n%i" % (i+1) for i in range(n)]
    d_nodes = ["n%i" % (i+1) for i in range(n,2*n)]
    k_nodes = ["n%i" % (i+1) for i in range(2*n, 2*n+m)]
    l_nodes = ["n%i" % (i+1) for i in range(2*n+m, 2*n+m+l)]
    z_nodes = ["n%i" % (2*n+m+l+1)]
    nodes =  o_nodes + d_nodes + k_nodes + l_nodes + z_nodes
    
    
    #t = {(i,j):1 for i in nodes for j in nodes}
    q = {i:0 for i in nodes}
    for i in o_nodes:
        q[i] = 1
    for i in d_nodes:
        q[i] = - 1
    for i in l_nodes:
        q[i] = - 1
    
    
    path = [k_nodes[car], z_nodes[0]]
    cost = 0
    added = True
    free_nodes = [x for x in range(n)]        # List indices
    free_extra_nodes = [x for x in passengers]  # List indices  
              
    while added:
        added = False
        best_path = path
        best_cost = cost
        for i in free_nodes:
            o = o_nodes[i]
            d = d_nodes[i]
            node_cost = 0
            node_path = path
            for j in range(1,len(path)):
                for k in range(j,len(path)):
                    order_cost = 0
                    order_path = path[:j] + [o] + path[j:k] + [d] + path[k:]
                    tmp_Q = len(passengers)
                    fail = 0
                    time = arr_time
                    for node in order_path:
                        tmp_Q = tmp_Q + q[node]
                        if tmp_Q > Qmax:
                            fail = 1
                    if fail:
                        order_cost = err_penalty
                    else:
                        for ll in range(len(order_path)-1):
                            time = time + t[(order_path[ll],order_path[ll+1])]
                            if order_path[ll+1] in o_nodes and time < starting_times[order_path[ll+1]]:
                                time = starting_times[order_path[ll+1]]
                            if order_path[ll+1] in d_nodes:
                                order_cost = order_cost + time - starting_times[o_nodes[d_nodes.index(order_path[ll+1])]] - pi[order_path[ll+1]].value()
                            if order_path[ll+1] in l_nodes:
                                order_cost = order_cost + time - pi[order_path[ll+1]].value()
                        if time > T:
                            order_cost = err_penalty
                    if order_cost < node_cost:
                        node_cost = order_cost
                        node_path = order_path
            if node_cost < best_cost:
                best_path = node_path
                best_cost = node_cost
                best_index = i
        

        for i in free_extra_nodes:
            d = l_nodes[i]
            node_cost = 0
            node_path = path
            for j in range(1,len(path)):
                order_cost = 0
                order_path = path[:j] + [d] + path[j:]
                tmp_Q = len(passengers)
                fail = 0
                time = arr_time
                for node in order_path:
                    tmp_Q = tmp_Q + q[node]
                    if tmp_Q > Qmax:
                        fail = 1
                if fail:
                    order_cost = err_penalty
                else:
                    for ll in range(len(order_path)-1):
                        time = time + t[(order_path[ll],order_path[ll+1])]
                        if order_path[ll+1] in o_nodes and time < starting_times[order_path[ll+1]]:
                            time = starting_times[order_path[ll+1]]
                        if order_path[ll+1] in d_nodes:
                            order_cost = order_cost + time - starting_times[o_nodes[d_nodes.index(order_path[ll+1])]]- pi[order_path[ll+1]].value()
                        if order_path[ll+1] in l_nodes:
                            order_cost = order_cost + time - pi[order_path[ll+1]].value()
                    if time > T:
                        order_cost = err_penalty
                if order_cost < node_cost:
                    node_cost = order_cost
                    node_path = order_path
            if node_cost < best_cost:
                best_path = node_path
                best_cost = node_cost
                best_index = -i-1
###                
                
        if best_cost < cost:
            cost = best_cost
            path = best_path
            if best_index >= 0:
                free_nodes.remove(best_index)
            else:
                free_extra_nodes.remove(-best_index-1)
            added = True
            
            
    inc_nodes = [node for node in path if node in o_nodes]
    for node1 in inc_nodes:
        path_copy = path.copy()
        node2 = d_nodes[o_nodes.index(node1)]
        path_copy.remove(node1)
        path_copy.remove(node2)
        best_cost = 0
        best_path = path_copy
        for j in range(1,len(path_copy)):
            for k in range(j,len(path_copy)):
                tmp_cost = 0
                tmp_path = path_copy[:j] + [node1] + path_copy[j:k] + [node2] + path_copy[k:]
                tmp_Q = len(passengers)
                fail = 0
                time = arr_time
                for node in tmp_path:
                    tmp_Q = tmp_Q + q[node]
                    if tmp_Q > Qmax:
                        fail = 1
                if fail:
                    tmp_cost = err_penalty
                else:
                    for ll in range(len(tmp_path)-1):
                        time = time + t[(tmp_path[ll],tmp_path[ll+1])]
                        if tmp_path[ll+1] in o_nodes and time < starting_times[tmp_path[ll+1]]:
                            time = starting_times[tmp_path[ll+1]]
                        if tmp_path[ll+1] in d_nodes:
                            tmp_cost = tmp_cost + time - starting_times[o_nodes[d_nodes.index(tmp_path[ll+1])]] - pi[tmp_path[ll+1]].value()
                        if tmp_path[ll+1] in l_nodes:
                            tmp_cost = tmp_cost + time - pi[tmp_path[ll+1]].value()
                    if time > T:
                        tmp_cost = err_penalty

                if tmp_cost < best_cost:
                    best_cost = tmp_cost
                    best_path = tmp_path
        if best_cost < cost:
            path = best_path
            cost = best_cost
    
    ###
    
    inc_extra_nodes = [node for node in path if node in l_nodes]
    for node in inc_extra_nodes:
        path_copy = path.copy()
        path_copy.remove(node)
        best_cost = 0
        best_path = path_copy
        for j in range(1,len(path_copy)):
            tmp_cost = 0
            tmp_path = path_copy[:j] + [node] + path_copy[j:]
            tmp_Q = len(passengers)
            fail = 0
            time = arr_time
            for node in tmp_path:
                tmp_Q = tmp_Q + q[node]
                if tmp_Q > Qmax:
                    fail = 1
            if fail:
                tmp_cost = err_penalty
            else:
                for ll in range(len(tmp_path)-1):
                    time = time + t[(tmp_path[ll],tmp_path[ll+1])]
                    if tmp_path[ll+1] in o_nodes and time < starting_times[tmp_path[ll+1]]:
                        time = starting_times[tmp_path[ll+1]]
                    if tmp_path[ll+1] in d_nodes:
                        tmp_cost = tmp_cost + time - starting_times[o_nodes[d_nodes.index(tmp_path[ll+1])]]- pi[tmp_path[ll+1]].value()
                    if tmp_path[ll+1] in l_nodes:
                        tmp_cost = tmp_cost + time - pi[tmp_path[ll+1]].value()
                if time > T:
                    tmp_cost = err_penalty
            if tmp_cost < best_cost:
                best_cost = tmp_cost
                best_path = tmp_path
        if best_cost < cost:
            path = best_path
            cost = best_cost
        
    ###    
           
    c = 0
    time = arr_time
    for i in range(len(path)-1):
        if path[i+1] in o_nodes:
            time = max([starting_times[path[i+1]], time + t[(path[i],path[i+1])]])
        else:
            time = time + t[(path[i],path[i+1])]
        if path[i+1] in d_nodes:
            c = c + time - starting_times[o_nodes[d_nodes.index(path[i+1])]]
        if path[i+1] in l_nodes:
            c = c + time
#    print(time)

            
    return(path, cost-gamma['c%i' % (car+1)].value(), c)