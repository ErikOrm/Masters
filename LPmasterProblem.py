import pulp

def LPmaster_problem(m, n_r, n, l, A, cost1, d):
#initialise the model
    master_problem = pulp.LpProblem('The master Problem', pulp.LpMinimize)

    
    # sets
    routes = ["r%i_%i" % (i+1, j+1) for i in range(m) for j in range(n_r)]
    nodes = ["n%i" % (i+1) for i in range(n,2*n)] + ["n%i" % (i+1) for i in range(2*n+m,2*n+m+l)]
    
    # create a dictionary of pulp variables with keys from ingredients
    ## the default lower bound is -inf
    lam = pulp.LpVariable.dict('lam%s', routes, lowBound = 0, upBound = 1.0)
    y = pulp.LpVariable.dict('y%s', nodes, lowBound = 0, upBound = 1.0)
    
    ## cost data
    cost2 = dict(zip(nodes, [d for x in range(len(nodes))]))
    
    ## create the objective
    master_problem += sum([cost1[i] * lam[i] for i in routes]) + sum([cost2[j] * y[j] for j in nodes])
    
    
    
    ##note these are constraints and not an objective as there is a equality/inequality
    for node in nodes:
        master_problem += sum([A[route, node]*lam[route] for route in routes]) + y[node] >= 1.0
              
    for i in range(m):
        master_problem += sum(lam[routes[n_r*i+j]] for j in range(n_r)) <= 1
                              
    
        
    ##problem is then solved with the default solver
    master_problem.solve()
    print("LP")
    print(master_problem.objective.value())    
#    print([x.value() for x in lam.values()])
    return master_problem.objective.value()