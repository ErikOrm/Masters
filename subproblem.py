import pulp



def sub_problem(n, k, m, pi, gamma, t):
    
    
    #initialise the model
    sub_problem = pulp.LpProblem('The Dual Problem', pulp.LpMinimize)
    
    T = 1000 # 20
    startTime = 0
    M = 2000
    
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
    
    # create a dictionary of pulp variables with keys from ingredients
    ## the default lower bound is -inf
    H = pulp.LpVariable.dict('H_%s', d_nodes, lowBound = 0, upBound = T)
    x = pulp.LpVariable.dict('x', (nodes, nodes), lowBound = 0, upBound = 1, cat = "Integer")
    B = pulp.LpVariable.dict('B_%s', nodes, lowBound = 0, upBound = T)
    Q = pulp.LpVariable.dict('Q_%s', nodes, lowBound = 0, upBound = 2)
        
    ## create the objective
    sub_problem += sum([H[i] for i in d_nodes]) + sum([(B[i]) for i in o_nodes]) + 0.000001*B[z_nodes[0]] - sum([pi[i].value()*x[(i,j)] for i in d_nodes for j in nodes]) - gamma['c%i' % (k+1)].value()  
        
         
    ## subject to
    sub_problem += sum([x[(k_nodes[k], j)] for j in o_nodes+d_nodes+z_nodes]) == 1
    for i in nodes:
        for j in k_nodes:
            sub_problem += x[(i, j)] == 0
    sub_problem += sum([x[(i, z_nodes[0])] for i in o_nodes+d_nodes+k_nodes]) == 1
    sub_problem += sum([x[(z_nodes[0], j)] for j in nodes]) == 0
    
    for i in o_nodes + d_nodes:
        sub_problem += sum([x[(j, i)] for j in [s for s in nodes if s != i]]) - sum([x[(i, j)] for j in [s for s in nodes if s != i]]) == 0
    
    for i in range(len(o_nodes)):
        sub_problem += sum([x[(o_nodes[i], j)] for j in [s for s in nodes if s != i]]) - sum([x[(d_nodes[i], j)] for j in [s for s in nodes if s != i]]) == 0
    
    sub_problem += B[k_nodes[k]] >= startTime
    
    for i in [s for s in nodes if not s in z_nodes]:
        for j in [s for s in nodes if not s in k_nodes]:
            sub_problem += B[j] >= B[i] + t[(i,j)] - M*(1-x[(i,j)])
            
    for i in [s for s in nodes if not s in z_nodes]:
        for j in [s for s in nodes if not s in k_nodes]:
            sub_problem += Q[j] >= Q[i] + q[j] - 5*(1-x[(i,j)])
    
    for i in range(len(d_nodes)):
        sub_problem += H[d_nodes[i]] == B[d_nodes[i]] - B[o_nodes[i]]
    
    sub_problem.writeLP("sub.lp")
    
    ##problem is then solved with the default solver
    sub_problem.solve()
    #sub_problem.roundSolution()
    
    
    print(sub_problem.objective.value())
    
    for node_1 in nodes:
        for node_2 in nodes:
            try:
                if x[(node_1, node_2)].value() == 1:
                    print("%s %s: %i" %(node_1, node_2, x[(node_1, node_2)].value()))
            except:
                print("%s %s:" %(node_1, node_2))
            
    for node in nodes:
        print("%s: %s" % (node, B[node].value()))

    red_cost = sub_problem.objective.value()
    cost = sum([H[i].value() for i in d_nodes]) + sum([B[i].value() for i in o_nodes]) + 0.000001*B[z_nodes[0]].value()
#    print("cost: %s" % cost)
#    print("redcost: %s" % red_cost)
    return(x,B,H,red_cost, cost)