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
    
    phase = 1
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
            elif method in ['insert', 'reinsert']:
                path[(i+1)], r_cost[(i+1)], cost[(i+1)] = sub_problem2(n_customers, i, n_vehicles, n_extra_customers, extra_dict[i], arr_times[i], starting_times, pi, gamma, t, T, Q_max, err_penalty, method)
            elif method == 'both':
                if phase == 1:
                    path[(i+1)], r_cost[(i+1)], cost[(i+1)] = sub_problem2(n_customers, i, n_vehicles, n_extra_customers, extra_dict[i], arr_times[i], starting_times, pi, gamma, t, T, Q_max, err_penalty, method)
                elif phase == 2:
                    path[(i+1)], r_cost[(i+1)], cost[(i+1)] = sub_problem_label(n_customers, i, n_vehicles, n_extra_customers, extra_dict[i], arr_times[i], starting_times, pi, gamma, t, T, Q_max, err_penalty)
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
              
        
        paths[it+2] = path
        red_cost = min([r_cost[(i+1)] for i in range(n_vehicles)])
        red_costs.append(red_cost)
#        print("redcost: %s" % red_cost)
        it = it+1
        if it == n_iter:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    
        if red_cost >= -1e-3 and phase == 1 and method == 'both':
            red_cost = -1
            phase = 2
            
    lam, MP_obj = master_problem(n_vehicles, (it+1), n_customers, n_extra_customers, A, c, d_val)
    
    ret_dict = {(i+1):['n%i' % (2*n_customers+i+1), 'n%i' % (2*n_customers+n_vehicles+n_extra_customers+1)] for i in range(n_vehicles)}
    for i in range(1, n_vehicles + 1):
        for j in range(1, len(paths) + 1):
            if lam['r%i_%i' % (i, j)].value() == 1:
                ret_dict[i] = paths[j][i]
    
    LP_obj = LPmaster_problem(n_vehicles, (it+1),n_customers, n_extra_customers, A, c, d_val)
    return ret_dict, MP_obj, LP_obj
  
    
    

n_vehicles =         [2]*5   +  [5]*5   + [5]*5
n_customers =        [10]*5  +  [20]*5  + [15]*5
n_extra_customers =  [3]*5   +  [5]*5   + [10]*5
T =                  [300]*5 +  [200]*5 + [200]*5
Q_max =              [2]*5   +  [2]*5   + [4]*5
seed =               [x+463 for x in [112,43,21423,2162,6,26,273247,32473,65,3,5346,263456,983245186,986457896,3245678,3256,7343325,52456,62,7,247,474,57,273246737,32347,3457,276,4236,346,26,78,865,436,72436,2436261,146,46471,1734157,148365,135145,62,457,572,134515,346213456,632,2342,1364,1643,1346,321446]]

times = []
MP_s = []
LP_s = []
times1 = []
MP_s1 = []
LP_s1 = []
times2 = []
MP_s2 = []
LP_s2 = []
F = open('save5.txt','w') 
for j in range(len(n_vehicles)):
    
    extra_dict = {i:[] for i in range(n_vehicles[j])}
    for i in range(n_extra_customers[j]):
        ve = math.floor(n_vehicles[j]*random.random())
        while len(extra_dict[ve]) >= Q_max[j]:
            ve = math.floor(n_vehicles[j]*random.random())
        extra_dict[ve].append(i)
    arr_times = {i:math.floor((T[j]/4)*random.random()) for i in range(n_vehicles[j])}
    starting_times = {("n%i" % (i + 1)):0 for i in range(n_customers[j])}
    d_val = T[j]
    err_penalty = 3000
    t = getT2(seed[j], n_vehicles[j], n_customers[j], n_extra_customers[j], T[j]+1)
    n_iter = 500
   
    start_time = time.time()    
    ret_dict, MP_obj, LP_obj = opt(t, n_vehicles[j], n_customers[j], n_extra_customers[j], extra_dict, arr_times, starting_times, [], [], d_val, T[j], Q_max[j], err_penalty, n_iter, 'label')
    times.append(time.time()-start_time)
    MP_s.append(MP_obj)
    LP_s.append(LP_obj)
    F.write("%f | %f | %f \n " % (MP_obj, LP_obj,time.time()-start_time))
    
    start_time = time.time()    
    ret_dict, MP_obj1, LP_obj1 = opt(t, n_vehicles[j], n_customers[j], n_extra_customers[j], extra_dict, arr_times, starting_times, [], [], d_val, T[j], Q_max[j], err_penalty, n_iter, 'reinsert')
    times1.append(time.time()-start_time)
    MP_s1.append(MP_obj1)
    LP_s1.append(LP_obj1)
    F.write("%f | %f | %f | " % (MP_obj1, LP_obj1,time.time()-start_time))
    
    start_time = time.time()    
    ret_dict, MP_obj2, LP_obj2 = opt(t, n_vehicles[j], n_customers[j], n_extra_customers[j], extra_dict, arr_times, starting_times, [], [], d_val, T[j], Q_max[j], err_penalty, n_iter, 'both')
    times2.append(time.time()-start_time)
    MP_s2.append(MP_obj2)
    LP_s2.append(LP_obj2)
    F.write("%f | %f | %f\n" % (MP_obj2, LP_obj2,time.time()-start_time))

F.close()

