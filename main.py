import pulp
import time
import itertools
import math
import random
from dualProblem import *
from subproblem import *
from masterProblem import *
from DATread import *

n_vehicles = 3
n_customers = 4
d_val = 200
T = 200
err_penalty = 3000
Q_max = 4
seed = 15
t = getT2(seed, n_vehicles, n_customers, T+1)
n_iter = 500

routes = ['r%i_1' % (i+1) for i in range(n_vehicles)]
nodes = ['n%i' % (i+1) for i in range(2*n_customers + n_vehicles + 1)]

A = {(route, node): 0 for route in routes for node in nodes}

red_costs = []
red_cost = -1
c = {}
d = {}

for i in range(n_vehicles):
    A[('r%i_1' % (i+1), 'n%i' % (2*n_customers+i+1))] = 1
    A[('r%i_1' % (i+1), 'n%i' % (2*n_customers+n_vehicles+1))] = 1
    c['r%i_1' % (i+1)] = 0


for node in nodes:
    d[node] = d_val

it = 0
while red_cost <0 and it<n_iter:  
    pi, gamma = dual_problem(n_vehicles, it+1, n_customers, A, c, d)
    print("pi: %s" % [pi["n%i" % (n_customers + i + 1)].value() for i in range(n_customers)])
    print("gamma: %s" % [gamma["c%i" % (i+1)].value() for i in range(n_vehicles)])
    
    x = {}
    path = {}
    r_cost = {}
    cost = {}
    for i in range(n_vehicles):
        print('ROUTE: r%i_%i' % (i+1, it+2))
        x[(i+1)], r_cost[(i+1)], cost[(i+1)] = sub_problem(n_customers, i, n_vehicles, pi, gamma, t, T, Q_max, err_penalty)
        for node in nodes:
            A[('r%i_%i' % (i+1, it+2), node)] = 0
        for node1 in nodes:
            for node2 in nodes:
                if x[(i+1)][(node1,node2)].value() == 1: 
                    A[('r%i_%i' % (i+1, it+2), node1)] = 1
        A[('r%i_%i' % (i+1, it+2), nodes[-1])] = 1
        c['r%i_%i' % (i+1, it+2)] = cost[(i+1)]
          
    it = it+1
    red_cost = max([r_cost[(i+1)] for i in range(n_vehicles)])
    red_costs.append(red_cost)
    print("redcost: %s" % red_cost)

master_problem(n_vehicles, (it+1),n_customers, A, c, d_val)


