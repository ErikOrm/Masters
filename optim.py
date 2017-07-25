import pulp
import time
import itertools
import math
import random
from dualProblem import *
from subproblem2 import *
from subproblem_label import *
from masterProblem import *
from LPmasterProblem import *
from DATread import *


def opt(t, n_vehicles, n_customers, n_extra_customers, extra_dict, arr_times, starting_times, hot_start_paths, hot_start_costs, d_val, T, Q_max, err_penalty, n_iter, method):

    
    if hot_start_paths:
        routes = ['r%i_1' % (i+1) for i in range(n_vehicles)] + ['r%i_2' % (i+1) for i in range(n_vehicles)]
    else:
        routes = ['r%i_1' % (i+1) for i in range(n_vehicles)]
    nodes = ['n%i' % (i+1) for i in range(2*n_customers + n_vehicles + n_extra_customers + 1)]
    
    A = {(route, node): 0 for route in routes for node in nodes}

    red_costs = []
    red_cost = -1
    c = {}
    d = {}
    
    for i in range(n_vehicles):
        A[('r%i_1' % (i+1), 'n%i' % (2*n_customers+i+1))] = 1
        A[('r%i_1' % (i+1), 'n%i' % (2*n_customers+n_vehicles+n_extra_customers+1))] = 1
        c['r%i_1' % (i+1)] = 0
        if hot_start_paths:
            for j in range(len(hot_start_paths[i])):
                A[('r%i_2' % (i+1), hot_start_paths[i][j])] = 1
            c['r%i_2' % (i+1)] = hot_start_costs[i]
    
    
    for node in nodes:
        d[node] = d_val

    paths = {1: {i:['n%i' % (2*n_customers+i+1), 'n%i' % (2*n_customers+n_vehicles+n_extra_customers+1)] for i in range(n_vehicles)}}
    
    it = 0
    if hot_start_paths:
        paths[2] = {}
        it = 1
        for i in range(n_vehicles):
            paths[2][i+1] = hot_start_paths[i]
    
    
    while red_cost < -1e-3 and it<n_iter:
        pi, gamma = dual_problem(n_vehicles, it+1, n_customers, n_extra_customers, A, c, d)
#        print("pi: %s" % ([pi["n%i" % (n_customers + i + 1)].value() for i in range(n_customers)] + [pi["n%i" % (2*n_customers + n_vehicles + i + 1)].value() for i in range(n_extra_customers)]))
#        print("gamma: %s" % [gamma["c%i" % (i+1)].value() for i in range(n_vehicles)])
        
        path = {}
        r_cost = {}
        cost = {}
        for i in range(n_vehicles):
#            print('ROUTE: r%i_%i' % (i+1, it+2))
            if method == 'label':
                path[(i+1)], r_cost[(i+1)], cost[(i+1)] = sub_problem_label(n_customers, i, n_vehicles, n_extra_customers, extra_dict[i], arr_times[i], starting_times, pi, gamma, t, T, Q_max, err_penalty)
            elif method == 'insert':
                path[(i+1)], r_cost[(i+1)], cost[(i+1)] = sub_problem2(n_customers, i, n_vehicles, n_extra_customers, extra_dict[i], arr_times[i], starting_times, pi, gamma, t, T, Q_max, err_penalty)
                    
#            print(path[(i+1)])
#            print(r_cost[(i+1)])
#            print(cost[(i+1)])
#            
            for node in nodes:
                A[('r%i_%i' % (i+1, it+2), node)] = 0
            for node in path[(i+1)]:
                A[('r%i_%i' % (i+1, it+2), node)] = 1
            A[('r%i_%i' % (i+1, it+2), nodes[-1])] = 1
            c['r%i_%i' % (i+1, it+2)] = cost[(i+1)]
              
        #wait = input("PRESS ENTER TO CONTINUE.")
        
        
        paths[it+2] = path
        red_cost = min([r_cost[(i+1)] for i in range(n_vehicles)])
        red_costs.append(red_cost)
        print("redcost: %s" % red_cost)
        it = it+1
        if it == n_iter:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
    lam, MP_obj = master_problem(n_vehicles, (it+1), n_customers, n_extra_customers, A, c, d_val)
    
    ret_dict = {(i+1):['n%i' % (2*n_customers+i+1), 'n%i' % (2*n_customers+n_vehicles+n_extra_customers+1)] for i in range(n_vehicles)}
    for i in range(1, n_vehicles + 1):
        for j in range(1, len(paths) + 1):
            if lam['r%i_%i' % (i, j)].value() == 1:
                ret_dict[i] = paths[j][i]
    
    LP_obj = LPmaster_problem(n_vehicles, (it+1),n_customers, n_extra_customers, A, c, d_val)
    return ret_dict, MP_obj, LP_obj
  
    
    
    
    

start_time = time.time()    
n_vehicles = 2
n_customers = 5
n_extra_customers = 5
meth  = 'label'

T = 200
Q_max = 4
seed = 11
extra_dict = {i:[] for i in range(n_vehicles)}
for i in range(n_extra_customers):
    extra_dict[math.floor(n_vehicles*random.random())].append(i)
arr_times = {i:math.floor((T/4)*random.random()) for i in range(n_vehicles)}
starting_times = {("n%i" % (i + 1)):0 for i in range(n_customers)}
d_val = T
err_penalty = 3000
t = getT2(seed, n_vehicles, n_customers, n_extra_customers, T+1)
n_iter = 500
ret_dict, MP_obj, LP_obj = opt(t, n_vehicles, n_customers, n_extra_customers, extra_dict, arr_times, starting_times, [], [], d_val, T, Q_max, err_penalty, n_iter, meth)
print("time: %f" % (time.time()-start_time))





















