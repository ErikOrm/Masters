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


def opt(t, n_vehicles, n_customers, n_extra_customers, extra_dict, arr_times, starting_times, d_val, T, Q_max, err_penalty, n_iter):
#    
#    print(n_vehicles, n_customers, n_extra_customers, extra_dict, arr_times, starting_times, d_val, T, Q_max, err_penalty, n_iter)
#    for x in ["n%i" % (i+1) for i in range(2*n_customers + n_vehicles + n_extra_customers + 1)]:
#        for y in ["n%i" % (i+1) for i in range(2*n_customers + n_vehicles + n_extra_customers + 1)]:
#            print("%s-%s : %i" % (x, y, t[(x,y)]))

    routes = ['r%i_1' % (i+1) for i in range(n_vehicles)]
    nodes = ['n%i' % (i+1) for i in range(2*n_customers + n_vehicles + n_extra_customers + 1)]
    
    A = {(route, node): 0 for route in routes for node in nodes}
    
    B = {}
    H = {}
      
    red_costs = []
    red_cost = -1
    c = {}
    d = {}
    
    for i in range(n_vehicles):
        A[('r%i_1' % (i+1), 'n%i' % (2*n_customers+i+1))] = 1
        A[('r%i_1' % (i+1), 'n%i' % (2*n_customers+n_vehicles+n_extra_customers+1))] = 1
        c['r%i_1' % (i+1)] = 0
    
    
    for node in nodes:
        d[node] = d_val

    paths = {1: {i:['n%i' % (2*n_customers+i+1), 'n%i' % (2*n_customers+n_vehicles+n_extra_customers+1)] for i in range(n_vehicles)}}
    
    it = 0
    while red_cost < 0 and it<n_iter:
        pi, gamma = dual_problem(n_vehicles, it+1, n_customers, n_extra_customers, A, c, d)
#        print("pi: %s" % ([pi["n%i" % (n_customers + i + 1)].value() for i in range(n_customers)] + [pi["n%i" % (2*n_customers + n_vehicles + i + 1)].value() for i in range(n_extra_customers)]))
#        print("gamma: %s" % [gamma["c%i" % (i+1)].value() for i in range(n_vehicles)])
        
        path = {}
        r_cost = {}
        cost = {}
        for i in range(n_vehicles):
#            print('ROUTE: r%i_%i' % (i+1, it+2))
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
        
        it = it+1
        paths[it+1] = path
        red_cost = min([r_cost[(i+1)] for i in range(n_vehicles)])
        red_costs.append(red_cost)
        print("redcost: %s" % red_cost)
    
    lam = master_problem(n_vehicles, (it+1), n_customers, n_extra_customers, A, c, d_val)
    
    ret_dict = {(i+1):[] for i in range(n_vehicles)}
    for i in range(1, n_vehicles + 1):
        for j in range(1, len(paths) + 1):
            if lam['r%i_%i' % (i, j)].value() == 1:
                if ret_dict[i] != []:
                    raise(Exception)
                ret_dict[i] = paths[j][i]

    return ret_dict
    
    
    
    
    LPmaster_problem(n_vehicles, (it+1),n_customers, n_extra_customers, A, c, d_val)
#
#
#n_vehicles = 1
#n_customers = 2
#n_extra_customers = 0
#extra_dict = {i:[] for i in range(n_vehicles)}
##extra_dict[0] = [0,1]
##extra_dict[1] = [2]
#arr_times = {i:0 for i in range(n_vehicles)}
#starting_times = {("n%i" % (i + 1)):0 for i in range(n_customers)}
#starting_times["n1"] = 150
#d_val = 300
#T = 300
#Q_max = 2
#err_penalty = 3000
#seed = 11
#t = getT2(seed, n_vehicles, n_customers, n_extra_customers, T+1)
#n_iter = 500
#opt(t, n_vehicles, n_customers, n_extra_customers, extra_dict, arr_times, starting_times, d_val, T, Q_max, err_penalty, n_iter)