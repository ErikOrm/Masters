
from DATread import *

class label():
    def __init__(self, parent, node, time, load, cost, open_requests, unreachable, label_dict):
        self.parent = parent
        self.node = node
        self.time = time
        self.load = load
        self.cost = cost
        self.open_requests = open_requests
        self.unreachable = unreachable
        self.label_dict = label_dict
        
    def extend(self, n, m, Q, t, T, pi):
        for req in self.open_requests:
            tmp_node = "n%i" % (req + n + 1)
            tmp_time = self.time + t[("n%i" % (self.node + 1), tmp_node)]
            tmp_load = self.load - 1
            if (tmp_time < T):
                tmp_cost = self.cost + self.time - pi[tmp_node]
                tmp_open_req = self.open_requests.copy()
                tmp_open_req.remove(req)
                tmp_unreachable = self.unreachable.copy()
                self.label_dict[(req + n, 'untreated')].append( label(self.node, req + n, tmp_time, tmp_load, tmp_cost, tmp_open_req, tmp_unreachable, self.label_dict))
                
        for req in [i for i in range(n) if not i in self.unreachable]:
            tmp_node = "n%i" % (req +1)
            tmp_time = self.time + t[("n%i" % (self.node + 1), tmp_node)]
            tmp_load = self.load + 1
            if (tmp_load < Q) and (tmp_time < T):
                tmp_cost = self.cost
                tmp_open_req = self.open_requests.copy()
                tmp_open_req.add(req)
                tmp_unreachable = self.unreachable.copy()
                tmp_unreachable.add(req)
                self.label_dict[(req, 'untreated')].append(label(self.node, req, tmp_time, tmp_load, tmp_cost, tmp_open_req, self.unreachable, self.label_dict))
                
        if not self.open_requests:
            self.label_dict[(2*n+m, 'treated')].append(label(self.node, (2*n+m+1), self.time, self.load, self.cost, self.open_requests, self.unreachable, self.label_dict))
        self.label_dict[(self.node, 'treated')].append(self)
        self.label_dict[(self.node, 'untreated')].remove(self)
        
        



def sub_problem_label(n, k, m, pi, gamma, t, T, Qmax):
    
    label_dict = {(i, j):[] for i in range(2*n+m+1) for j in ['untreated','treated']}
    label_dict[(2*n+k, 'untreated')].append(label(None, 2*n+k, 0, 0, 0, set(), set(), label_dict))
    
    cont = True
    while  cont:
        cont = False
        for i in range(2*n+m+1):
            if label_dict[(i, 'untreated')]:
                cont = True
                for lab in label_dict[(i, 'untreated')]:
                    lab.extend(n, m, Qmax, t, T, pi)
                    
    return label_dict
    
m = 2
n = 3
pi = {"n%i" % (i+1):200 for i in range(3,6)}
gamma = {"c%i" % (i+1):0 for i in range(2)}
T = 1000
seed = 34
t = getT2(seed, n_vehicles, n_customers, T+1)
Qmax = 2
A = sub_problem_label(n, 0, m, pi, gamma, t, T, Qmax)

path = [11]
