import pulp
import time
import itertools
import math
import random
from dualProblem import *
from subproblem import *
from masterProblem import *

routes = ['r11', 'r21', 'r31']
nodes = ['n%i' % (i+1) for i in range(12)]

t = {(node1, node2) : 30 for node1 in nodes for node2 in nodes}

for node in nodes:
    if node != 'n12':
        t[(node, 'n12')] = 0
          
for node1 in nodes:
    for node2 in nodes:
        if not node2 in ['n9', 'n10', 'n11', 'n12'] and node1 != node2 and node1 != 'n12':
            t[(node1, node2)] = random.random()

A = {(route, node): 0 for route in routes for node in nodes}
A[('r11', 'n9')] = 1
A[('r11', 'n12')] = 1
A[('r21', 'n10')] = 1
A[('r21', 'n12')] = 1
A[('r31', 'n11')] = 1
A[('r31', 'n12')] = 1

B = {}
H = {}
  

red_costs = []
red_cost = -1
i = 0
c = {}
d = {}
c['r11'] = 0
c['r21'] = 0
c['r31'] = 0
for node in nodes:
    d[node] = 10


while red_cost <0 and i<15:  
    pi, gamma = dual_problem(3,i+1,4,A, c, d)
    print("pi: %s" % [pi["n5"].value(), pi["n6"].value(), pi["n7"].value(), pi["n8"].value()])
    print("gamma: %s" % [gamma["c1"].value(), gamma["c2"].value(), gamma["c2"].value()])
    print('ROUTE: r1%i' % (i+2))
    x1, B1, H1, r_cost1, cost1 = sub_problem(4,0,3,pi, gamma, t)
    print('ROUTE: r2%i' % (i+2))
    x2, B2, H2, r_cost2, cost2 = sub_problem(4,1,3,pi, gamma, t)
    print('ROUTE: r3%i' % (i+2))
    x3, B3, H3, r_cost3, cost3 = sub_problem(4,2,3,pi, gamma, t)
    for node in nodes:
        A[('r1%i' % (i+2), node)] = 0
        A[('r2%i' % (i+2), node)] = 0
        A[('r3%i' % (i+2), node)] = 0
    
    for node1 in nodes:
        for node2 in nodes:
            if x1[(node1, node2)].value() == 1:
                if A[('r1%i' % (i+2), node1)] == 0:
                    A[('r1%i' % (i+2), node1)] = 1
                else:
                    raise(Exception)
            if x2[(node1, node2)].value() == 1:
                if A[('r2%i' % (i+2), node1)] == 0:
                    A[('r2%i' % (i+2), node1)] = 1
                else:
                    raise(Exception)
            if x3[(node1, node2)].value() == 1:
                if A[('r3%i' % (i+2), node1)] == 0:
                    A[('r3%i' % (i+2), node1)] = 1
                else:
                    raise(Exception)
    A[('r1%i' % (i+2), 'n12')] = 1
    A[('r2%i' % (i+2), 'n12')] = 1
    A[('r3%i' % (i+2), 'n12')] = 1
      
    c['r1%i' % (i+2)] = cost1
    c['r2%i' % (i+2)] = cost2
    c['r3%i' % (i+2)] = cost3
    
      
    i = i+1
    red_cost = max([r_cost1, r_cost2, r_cost3])
    red_costs.append(red_cost)
    print("redcost: %s" % red_cost)

master_problem(3, (i+1),4, A, c)

