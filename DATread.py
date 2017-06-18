# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 16:28:24 2017

@author: Snok
"""
import numpy as np
import random
import math


def getT():
    f = open(r'D:\MasterThesis\DATA\1P2.DAT','r')
    
    p = []
    
    for line in f:
        line.strip()
        arr = line.split()
        p.append([int(arr[1]), int(arr[2])])
    
    car_nodes = [37, 18, 96]
    start_nodes = [4,30,65,87,25,62,14,52]
    end_nodes = [13,47,60,73,24,79,23,12]
    
    
    nodes = ['n%i' % (i+1) for i in range(12)]
    
    s_nodes = start_nodes + end_nodes + car_nodes
    e_nodes = start_nodes + end_nodes
    
    t = {(node1, node2) : 1000 for node1 in nodes for node2 in nodes}
    for i in range(len(s_nodes)):
        for j in range(len(e_nodes)):
            if i != j:
                vec1 = np.array(p[s_nodes[i]])
                vec2 = np.array(p[e_nodes[j]])
                t[("n%i"%(i+1),"n%i"%(j+1))] = np.linalg.norm(vec1-vec2,2)
        t[("n%i"%(i+1),"n%i"%(len(s_nodes)+1))] = 0
    
    return t
    
    
    
def getT2(seed, n_vehicles, n_customers, M):
    random.seed(seed)
    
    x = [math.floor(101*random.random()) for i in range(n_vehicles+2*n_customers+1)]
    y = [math.floor(101*random.random()) for i in range(n_vehicles+2*n_customers+1)]

    nodes = ['n%i' % (i+1) for i in range(n_vehicles+2*n_customers+1)]
    s_nodes = [i for i in range(2*n_customers+n_vehicles)]
    e_nodes = [i for i in range(2*n_customers)]

    t = {(node1, node2) : M for node1 in nodes for node2 in nodes}
    for i in s_nodes:
        for j in e_nodes:
            if i != j:
                vec1 = np.array([x[i], y[i]])
                vec2 = np.array([x[j], y[j]])
                t[("n%i" % (i+1), "n%i" % (j+1))] = np.linalg.norm(vec1-vec2,2)
        t[("n%i" % (i+1), nodes[-1])] = 0
    
    print(nodes)
    print(s_nodes)
    print(e_nodes)
    
    print(t)
    return t
    
    
    
    
getT2(56, 1,2,1000)
    