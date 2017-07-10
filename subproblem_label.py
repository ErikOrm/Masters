
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
        
    def extend(self, n, m, l, Q, t, T, pi):
        for req in self.open_requests:
            tmp_node = "n%i" % (req + 1)
            tmp_time = self.time + t[("n%i" % (self.node + 1), tmp_node)]
            tmp_load = self.load - 1
            if (tmp_time < T):
                tmp_cost = self.cost + tmp_time - pi[tmp_node].value()
                tmp_open_req = self.open_requests.copy()
                tmp_open_req.remove(req)
                tmp_unreachable = self.unreachable.copy()
                self.label_dict[(req, 'untreated')].append(label(self, req, tmp_time, tmp_load, tmp_cost, tmp_open_req, tmp_unreachable, self.label_dict))
                
        for req in [i for i in range(n) if not i in self.unreachable]:
            tmp_node = "n%i" % (req + 1)
            tmp_time = self.time + t[("n%i" % (self.node + 1), tmp_node)]
            tmp_load = self.load + 1
            if (tmp_load <= Q) and (tmp_time < T):
                tmp_cost = self.cost
                tmp_open_req = self.open_requests.copy()
                tmp_open_req.add(n+req)
                tmp_unreachable = self.unreachable.copy()
                tmp_unreachable.add(req)
                self.label_dict[(req, 'untreated')].append(label(self, req, tmp_time, tmp_load, tmp_cost, tmp_open_req, tmp_unreachable, self.label_dict))
                
        if not self.open_requests:
            self.label_dict[(2*n+m+l, 'treated')].append(label(self, (2*n+m+l), self.time, self.load, self.cost, self.open_requests, self.unreachable, self.label_dict))
        self.label_dict[(self.node, 'treated')].append(self)
        self.label_dict[(self.node, 'untreated')].remove(self)
        
        



def sub_problem_label(n, k, m, l, passengers, arr_time, pi, gamma, t, T, Qmax, dummy):
    
    p = [(2*n+m+i) for i in passengers] 
    label_dict = {(i, j):[] for i in range(2*n+m+l+1) for j in ['untreated','treated']}
    label_dict[(2*n+k, 'untreated')].append(label(None, 2*n+k, arr_time, len(p), 0, set(p), set(), label_dict))
    
    cont = True
    while  cont:
        cont = False
        for i in range(2*n+m+l+1):
            if label_dict[(i, 'untreated')]:
                cont = True

#                remove_set = set()
#                length = len(label_dict[(i, 'untreated')])
#                for j in range(length):
#                    for k in range(j+1, length):
#                        lab1 = label_dict[(i, 'untreated')][j]
#                        lab2 = label_dict[(i, 'untreated')][k]
#                        if lab1.cost <= lab2.cost and lab1.load <= lab2.load and lab1.time <= lab2.time and lab1.unreachable == lab2.unreachable and lab1.open_requests == lab2.open_requests:
#                            remove_set.add(k)
#                        elif lab2.cost <= lab1.cost and lab2.load <= lab1.load and lab2.time <= lab1.time and lab2.unreachable == lab1.unreachable and lab2.open_requests == lab1.open_requests:
#                            remove_set.add(j)
#                for index in sorted(list(remove_set), reverse=True):
#                    del label_dict[(i, 'untreated')][index]

                for lab in label_dict[(i, 'untreated')]:
                    lab.extend(n, m, l, Qmax, t, T, pi)
        
                        
    best_lab = label_dict[(2*n+m+l, 'treated')][0]
    for lab in label_dict[(2*n+m+l, 'treated')]:
        if lab.cost < best_lab.cost:
            best_lab = lab
    
    reduced_cost = best_lab.cost - gamma['c%i' % (k+1)].value()
    cost = 0            
    path = [best_lab.node]
    labels = [best_lab]
    while best_lab.parent:
        if n<=best_lab.node<2*n or 2*n+m<=best_lab.node<2*n+m+l:
            cost = cost + best_lab.time
        best_lab = best_lab.parent
        path.append(best_lab.node)
        labels.append(best_lab)
    
    return ["n%i" % (i+1) for i in path[::-1]], reduced_cost, cost
    
#m = 2
#n = 3
#pi = {"n%i" % (i+1):200 for i in range(3,6)}
#gamma = {"c%i" % (i+1):0 for i in range(2)}
#T = 200
#seed = 34
#t = getT2(seed, m, n, T+1)
#Qmax = 2
#path, red_cost, cost, labels = sub_problem_label(n, 0, m, pi, gamma, t, T, Qmax, 2)
#

