import pulp
import math

def dual_problem(n_c, n_r, n_n, n_ec, A, c, d):

    #initialise the model
    dual_problem = pulp.LpProblem('The Dual Problem', pulp.LpMaximize)
    
    # sets
    routes = ["r%i_%i" % (i+1, j+1) for i in range(n_c) for j in range(n_r)]
    nodes = ["n%i" % (i+1+n_n) for i in range(n_n)] + ["n%i" % (i+1+2*n_n+n_c) for i in range(n_ec)]
    cars = ["c%i" % (i+1) for i in range(n_c)]
    
    # create a dictionary of pulp variables with keys from ingredients
    ## the default lower bound is -inf
    pi = pulp.LpVariable.dict('pi%s', nodes, lowBound = 0)
    gamma = pulp.LpVariable.dict('gamma%s', cars, upBound = 0)
    
    
    dual_problem += sum([pi[i] for i in nodes]) + sum([gamma[j] for j in cars])
    
    for it in range(len(routes)):
        route = routes[it]
        car = cars[math.floor(it/n_r)]
        dual_problem += sum([A[route, node]*pi[node] for node in nodes]) + gamma[car] <= c[route]
    
    for node in nodes:
        dual_problem += pi[node] <= d[node]
                              
    ##problem is then solved with the default solver
    dual_problem.solve()

   
    return(pi, gamma)