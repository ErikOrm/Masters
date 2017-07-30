import random as r
import matplotlib.pyplot as plt
import math
from Dijkstra import *
import numpy as np
import time
from optim import opt
from scipy.spatial import Delaunay
from insertion import *

class graph:
    
    def __init__(self, size, size_x, size_y):
        self.size = size #int
        self.size_x = size_x #m
        self.size_y = size_y #m
        self.initialise_nodes()
        self.initialse_arcs()
        
                       
    def initialise_nodes(self):
        self.nodes = []
        for i in range(self.size):
            x = self.size_x*r.random()
            y = self.size_y*r.random()
            self.nodes.append(node(len(self.nodes)+1,x,y))
            
    def initialse_arcs(self):
        self.arcs = []
        points = np.array([[node.x, node.y] for node in self.nodes])
        tri = Delaunay(points)
        tmp_dict = {i:set() for i in range(len(self.nodes))}
        for simp in tri.simplices:
            tmp_dict[simp[0]].add(simp[1])
            tmp_dict[simp[0]].add(simp[2])
            tmp_dict[simp[1]].add(simp[0])
            tmp_dict[simp[1]].add(simp[2])
            tmp_dict[simp[2]].add(simp[0])
            tmp_dict[simp[2]].add(simp[1])
            
        for i in range(len(self.nodes)):
            tmp_dict[i] = list(tmp_dict[i])
            for j in range(len(tmp_dict[i])):
                self.arcs.append(arc(len(self.arcs)+1,self.nodes[i],self.nodes[tmp_dict[i][j]]))
                                
        
    def plot(self):
        plt.figure(num=None, figsize=(10, 10), dpi=120, facecolor='w', edgecolor='w')
        plt.plot([node.x for node in self.nodes], [node.y for node in self.nodes],'ro')
        for arc in self.arcs:
            plt.plot([arc.start_node.x, arc.end_node.x], [arc.start_node.y, arc.end_node.y])
        plt.show
            
class node:
    
    def __init__(self,ID,x,y):
        self.ID = ID
        self.x = x
        self.y = y
        
    def __str__(self):
        return "Node: ID:%i, x:%f, y:%f" % (self.ID, self.x, self.y)
        
    def __repr__(self):
        return "(%i,%.2f,%.2f)" % (self.ID, self.x, self.y)

class arc:
    
    def __init__(self,ID,start_node,end_node):
        self.ID = ID
        self.start_node = start_node
        self.end_node = end_node
        self.length = math.ceil(math.sqrt(pow(start_node.x-end_node.x,2)+pow(start_node.y-end_node.y,2)))
        
        
    def __str__(self):
        return "Arc: ID:%i, s:%i, e:%i" % (self.ID, self.start_node.ID, self.end_node.ID)
        
    def __repr__(self):
        return "(%i,%i,%i)" % (self.ID, self.start_node.ID, self.end_node.ID)      
        

class user:
    
    def __init__(self, ID, start_time, start_node, end_node):
        self.ID = ID
        self.start_time  = start_time
        self.start_node = start_node
        self.end_node = end_node
    
    def __repr__(self):
        return "user-%i" % self.ID
        
class vehicle:
    
    def __init__(self, ID, start_node, capacity):
        self.ID = ID
        self.node = start_node
        self.capacity = capacity
        self.path = []
        self.short_path = []
        self.users = []
        self.target_users = []
        self.arrival_time = 1
        
        
    def __repr__(self):
        return "vehicle-%i" % self.ID
        
    
    def pickup(self, user, time):
        if (not self.node == user.start_node) or len(self.users) == self.capacity:
            raise Exception("Disallowed pickup")
        elif time < user.start_time:
            return "wait"
        else:
            self.target_users.remove(user)
            self.users.append(user)
            return "pickup"
            
            
    def dropoff(self, user):
        if (not self.node == user.end_node) or not user in self.users:
            raise Exception("Disallowed dropoff")
        else:
            self.users.remove(user)
            
    def assign(self, user):
        self.target_users.append(user)
        
    def deassign(self, user):
        if user in self.target_users:
            self.target_users.remove(user)
        else:
            raise Exception("%s is not in %s and can't be deassigned" % (user, self))
        
        
class model:
    
    def __init__(self, size, size_x, size_y, n_users, n_vehicles, vehicle_cap, time, reopt, horizon):
        
        self.graph = graph(size, size_x, size_y)
        self.create_user_template(n_users, time)
        self.create_vehicle_template(n_vehicles, vehicle_cap)
        self.time = time
        self.vehicle_cap = vehicle_cap
        self.reopt = reopt
        self.horizon = horizon
        self.dist_dict = {}
        self.path_dict = {}
        for node1 in self.graph.nodes:
            for node2 in self.graph.nodes:
               self.path_dict[(node1, node2)], self.dist_dict[(node1, node2)] = dijkstra(node1, node2, self.graph.nodes, self.graph.arcs)
        
        
    def create_user_template(self, n_users, time):

        self.users_template = []
        for i in range(n_users):
            start_node = r.sample(self.graph.nodes,1)[0]
            end_node = r.sample([node for node in self.graph.nodes if node != start_node],1)[0]
            start_time = r.randint(1,math.ceil((1/2)*time))
            self.users_template.append(user(len(self.users_template)+1, start_time, start_node, end_node))
            
    def read_user_template(self):
        
        tmp_users = []
        for u in self.users_template:
            tmp_users.append(user(u.ID, u.start_time, u.start_node, u.end_node))
        return tmp_users
        
    def create_vehicle_template(self, n_vehicles, vehicle_cap):
        
        self.vehicles_template = []
        for i in range(n_vehicles):
            start_node = r.sample(self.graph.nodes,1)[0]
            self.vehicles_template.append(vehicle(len(self.vehicles_template)+1, start_node, vehicle_cap))
            
    def read_vehicle_template(self):
        
        tmp_vehicles = []
        for v in self.vehicles_template:
            tmp_vehicles.append(vehicle(v.ID, v.node, v.capacity))
        return tmp_vehicles
        
        
    def simulate(self, dispatcher, mode):
        
        start_time = time.time()
        self.unserved_users = []
        self.n_served = 0
        self.users = self.read_user_template()
        self.vehicles = self.read_vehicle_template()
        self.waiting_times_dict = {user:np.inf for user in self.users}
        time_user_dict = {t:[] for t in range(1,self.time+1)}
        if mode[0] in ['dynamic', 'dynamic_insert']:
            for user in self.users:
                time_user_dict[user.start_time].append(user)
        elif mode[0] == 'static':
            for user in self.users:
                time_user_dict[1].append(user)
        self.at_node = {t:[] for t in range(1,self.time+1)}
        for vehicle in self.vehicles:
            self.at_node[vehicle.arrival_time].append(vehicle)
        
        pickup_times = {v:[] for v in self.vehicles}

        for t in range(1,self.time):
            
                    
            # ADD USERS
            self.unserved_users.extend(time_user_dict[t])

            # VEHICLE ARRIVALS
            for vehicle in self.at_node[t]:
                if vehicle.path:
                    vehicle.node = vehicle.path[0]
                    vehicle.path = vehicle.path[1:]
  
            # onNextTimestep
            dispatcher.on_next_timestep(self, t, self.vehicle_cap, mode, time_user_dict[t])

            for vehicle in self.at_node[t]:

                cont = True
                while cont:
                    cont = False
                    for user in vehicle.users:
                        if user.end_node == vehicle.node == vehicle.short_path[0][0]:
                            assert vehicle.node == vehicle.short_path[0][0], "%s : %s : %s : %s" % (vehicle, user, vehicle.node, vehicle.short_path[0])
                            vehicle.short_path = vehicle.short_path[1:]
                            pickup_times[vehicle].append(t)
#                            print("%s dropoff %s at %i" % (vehicle, user, t))
                            vehicle.dropoff(user)
                            dispatcher.on_dropoff(self, vehicle)
                            self.n_served = self.n_served + 1
                            self.waiting_times_dict[user] = t
                            cont = True
                            break

                wait = False
                cont = True
                while cont:
                    cont = False
                    if vehicle.target_users:
                        user = vehicle.target_users[0]
                        if user.start_node == vehicle.node == vehicle.short_path[0][0]:
                            res = vehicle.pickup(user, t)
                            if res == "wait":
                                vehicle.path = [vehicle.node] + vehicle.path
                                wait = True
                            elif  res == "pickup":
#                                print("%s pickup %s at %i" % (vehicle, user, t))
#                                print(vehicle.node, user.start_node)
                                assert vehicle.node == vehicle.short_path[0][0], "%s : %s : %s : %s" % (vehicle, user, vehicle.node, vehicle.short_path[0])
                                vehicle.short_path = vehicle.short_path[1:]
                                self.unserved_users.remove(user)
                                dispatcher.on_pickup(self, vehicle)
                                pickup_times[vehicle].append(t)
                                cont = True
              


                if not wait and vehicle.path:
                    if math.ceil(self.dist_dict[(vehicle.node, vehicle.path[0])]) > 0:
                        if t+math.ceil(self.dist_dict[(vehicle.node, vehicle.path[0])]) <= self.time:
                            self.at_node[t+math.ceil(self.dist_dict[(vehicle.node, vehicle.path[0])])].append(vehicle)
                            vehicle.arrival_time = t+math.ceil(self.dist_dict[(vehicle.node, vehicle.path[0])])
                        else:
                            pass
                    else:
                        assert vehicle.node == vehicle.path[0]
                        vehicle.node = vehicle.path[0]
                        vehicle.path = vehicle.path[1:]
                        if vehicle.path:
                            assert math.ceil(self.dist_dict[(vehicle.node, vehicle.path[0])]) > 0
                            self.at_node[t+math.ceil(self.dist_dict[(vehicle.node, vehicle.path[0])])].append(vehicle)
                            vehicle.arrival_time = t+math.ceil(self.dist_dict[(vehicle.node, vehicle.path[0])])
                        else:
                            self.at_node[t+1].append(vehicle)
                            vehicle.arrival_time = t+1
                else:
                    self.at_node[t+1].append(vehicle)
                    vehicle.arrival_time = t+1
            

            self.at_node[t] = []
            if time.time()-start_time >300:
                return [-1,-1]
            
        for t in range(1,self.time):
            for user in time_user_dict[t]:
                if self.waiting_times_dict[user] == np.inf:
                    self.waiting_times_dict[user] = self.time-user.start_time
                else:
                    self.waiting_times_dict[user] = self.waiting_times_dict[user]-user.start_time
        
        print(time.time()-start_time)
             

        return [sum([x for x in self.waiting_times_dict.values()]), time.time()-start_time]
            
          
class final_dispatcher():
    
    def __init__(self):
        self.to_update = []

    def on_next_timestep(self, model, t, Q_max, mode, new_users):
        err_penalty = 2000
        n_iter = 250
        if mode[0] == 'static':
            freq = 10000
            T = model.time
            d_val = model.time
        elif mode[0] in ['dynamic', 'dynamic_insert']:
            freq = model.reopt
            T = min(model.time-t, model.horizon)
            d_val = T

        if t % freq == 1:
            
            print("t: %i" % t)
            
            passenger_dict = {}  # vehicle index : passenger index
            passengers = []
            arrival_dict = {c:0 for c in range(len(model.vehicles))}
            tmp_passenger_no = 0
            keep_track_of_passengers_dict = {} # passenger index : user
            for vehicle in model.vehicles:
                vehicle.target_users = []
                passenger_dict[model.vehicles.index(vehicle)] = []
                for user in vehicle.users:
                    passenger_dict[model.vehicles.index(vehicle)].append(tmp_passenger_no)
                    keep_track_of_passengers_dict[tmp_passenger_no] = user
                    tmp_passenger_no = tmp_passenger_no + 1
                passengers.extend(vehicle.users)
            l = len(passengers)
            n = len(model.unserved_users)
            m = len(model.vehicles)
            
            n_nodes = 2*n + m + l + 1
            travel_times = {("n%i" % (i+1), "n%i" % (j+1)):1000 for i in range(n_nodes) for j in range(n_nodes)}
            for user1 in model.unserved_users:
                for user2 in model.unserved_users:
                    travel_times[("n%i" % (model.unserved_users.index(user1) + 1), "n%i" % (model.unserved_users.index(user2) + 1))] = model.dist_dict[(user1.start_node, user2.start_node)]
                    travel_times[("n%i" % (model.unserved_users.index(user1) + n + 1), "n%i" % (model.unserved_users.index(user2) + 1))] = model.dist_dict[(user1.end_node, user2.start_node)]
                    travel_times[("n%i" % (model.unserved_users.index(user1) + 1), "n%i" % (model.unserved_users.index(user2) + n + 1))] = model.dist_dict[(user1.start_node, user2.end_node)]
                    travel_times[("n%i" % (model.unserved_users.index(user1) + n + 1), "n%i" % (model.unserved_users.index(user2) + n + 1))] = model.dist_dict[(user1.end_node, user2.end_node)]

                for user2 in passengers:
                    travel_times[("n%i" % (model.unserved_users.index(user1) + 1), "n%i" % (2*n + m + passengers.index(user2) + 1))] = model.dist_dict[(user1.start_node, user2.end_node)]
                    travel_times[("n%i" % (model.unserved_users.index(user1) + n + 1), "n%i" % (2*n + m + passengers.index(user2) + 1))] = model.dist_dict[(user1.end_node, user2.end_node)]

                travel_times[("n%i" % (model.unserved_users.index(user1) + 1), "n%i" % (2*n+m+l+1))] = 0
                travel_times[("n%i" % (model.unserved_users.index(user1) + n + 1), "n%i" % (2*n+m+l+1))] = 0


            for user1 in passengers:
                for user2 in model.unserved_users:
                    travel_times[("n%i" % (2*n + m + passengers.index(user1) + 1), "n%i" % (model.unserved_users.index(user2) + 1))] = model.dist_dict[(user1.end_node, user2.start_node)]
                    travel_times[("n%i" % (2*n + m + passengers.index(user1) + 1), "n%i" % (model.unserved_users.index(user2) + n + 1))] = model.dist_dict[(user1.end_node, user2.end_node)]
                    
                for user2 in passengers:
                    travel_times[("n%i" % (2*n + m + passengers.index(user1) + 1), "n%i" % (2*n + m + passengers.index(user2) + 1))] = model.dist_dict[(user1.end_node, user2.end_node)]
                    
                travel_times[("n%i" % (2*n + m + passengers.index(user1) + 1), "n%i" % (2*n+m+l+1))] = 0


            for vehicle in model.vehicles:
                if vehicle in model.at_node[t]:
                    node = vehicle.node
                else: 
                    node = vehicle.path[0]  

                for user2 in model.unserved_users:
                    travel_times[("n%i" % (2*n + model.vehicles.index(vehicle) + 1), "n%i" % (model.unserved_users.index(user2) + 1))] = model.dist_dict[(node, user2.start_node)]
                    travel_times[("n%i" % (2*n + model.vehicles.index(vehicle) + 1), "n%i" % (model.unserved_users.index(user2) + n + 1))] = model.dist_dict[(node, user2.end_node)]

                for user2 in passengers:
                    travel_times[("n%i" % (2*n + model.vehicles.index(vehicle) + 1), "n%i" % (2*n + m + passengers.index(user2) + 1))] = model.dist_dict[(node, user2.end_node)]
                    
                travel_times[("n%i" % (2*n + model.vehicles.index(vehicle) + 1), "n%i" % (2*n+m+l+1))] = 0
                
            for node in range(n_nodes):
                travel_times[("n%i" % (node+1), "n%i" % (node+1))] = 1000
                             
                             
            for tt in range(t, min(model.time, t+T+1)):
                for vehicle in model.at_node[tt]:
                    arrival_dict[model.vehicles.index(vehicle)] = tt-t
            
            starting_times = {("n%i" % (i + 1)):(max(0,model.unserved_users[i].start_time-t)) for i in range(n)}
            
                              
            hot_start_paths = {}
            hot_start_costs = {}
            for vehicle in model.vehicles:
                hs_cost = 0
                if vehicle in model.at_node[t]:
                    last_node = vehicle.node
                else:
                    last_node = vehicle.path[0] 
                load = len(vehicle.users)
                time = arrival_dict[model.vehicles.index(vehicle)]
                                    
                hs_path = ["n%i" % (2*n + model.vehicles.index(vehicle) + 1)]
                p_users = []
                for node in vehicle.short_path:
                    node = node[0]
                    time = time + model.dist_dict[(last_node, node)]
                    last_node = node
                    for user in vehicle.users:
                        if node == user.end_node:
                            hs_path.append("n%i" % (2*n + m + passengers.index(user) + 1))
                            hs_cost = hs_cost + time
                        load = load - 1
                    for user in vehicle.target_users:
                        if node == user.start_node:
                            hs_path.append("n%i" % (model.unserved_users.index(user) + 1))
                            if time < starting_times["n%i" % (model.unserved_users.index(user) + 1)]:
                                time = starting_times["n%i" % (model.unserved_users.index(user) + 1)]
                            p_users.append(user)
                            load = load + 1
                        if node == user.end_node:
                            hs_path.append("n%i" % (model.unserved_users.index(user) + n + 1))
                            hs_cost = hs_cost + time - starting_times["n%i" % (model.unserved_users.index(user) + 1)]
                            assert user in p_users
                            load = load - 1
                    assert load <= model.vehicle_cap
                hot_start_paths[model.vehicles.index(vehicle)] = hs_path + ["n%i" % (2*n+m+l+1)]
                hot_start_costs[model.vehicles.index(vehicle)] = hs_cost
            

            ret_dict, MP, LP = opt(travel_times, m, n, l, passenger_dict, arrival_dict, starting_times, hot_start_paths, hot_start_costs, d_val, T, Q_max, err_penalty, n_iter, mode[1])
            
            duplicate_list = []
            for i in range(len(ret_dict)):
                assert ret_dict[i+1][0] == "n%i" % (2*n + i + 1)
                tmp_path = [int(x[1:])-1 for x in ret_dict[i+1]]
                remove_indices = []
                for j in range(len(tmp_path)):
                    if tmp_path[j] in duplicate_list:
                        remove_indices.append(j)
                    else:
                        duplicate_list.append(tmp_path[j])
                remove_indices.reverse()
                for index in remove_indices:
                    tmp_path.pop(index)
                        
                vehicle = model.vehicles[i]
                if vehicle in model.at_node[t]:
                    next_node = vehicle.node
                else: 
                    next_node = vehicle.path[0] 
                vehicle.path = []
                vehicle.short_path = []

                for j in tmp_path:
                    if j<n:
                        vehicle.target_users.append(model.unserved_users[j])
                        vehicle.path.extend(model.path_dict[(vehicle.path[-1], model.unserved_users[j].start_node)])
                        vehicle.short_path.append((model.unserved_users[j].start_node, 's'))
                    elif n<=j<2*n:
                        vehicle.path.extend(model.path_dict[(vehicle.path[-1], model.unserved_users[j-n].end_node)])
                        vehicle.short_path.append((model.unserved_users[j-n].end_node, 'e'))
                    elif 2*n<=j<2*n+m:
                        assert vehicle.path == []
                        vehicle.path.append(next_node)
                    elif 2*n+m<=j<2*n+m+l:
                        vehicle.path.extend(model.path_dict[(vehicle.path[-1], keep_track_of_passengers_dict[(j-2*n-m)].end_node)])
                        vehicle.short_path.append((keep_track_of_passengers_dict[(j-2*n-m)].end_node, 'e'))
                        
        elif mode[0] == 'dynamic_insert':
            for user in new_users:
                insert(user, model, t)
                
                        
                        
    def on_pickup(self, model, vehicle):
        pass
    
    def on_dropoff(self, model, vehicle):
        pass
        

D = 5
n =       [60]*D  + [60]*D   + [80]*D   + [40]*D   + [80]*D
m =       [5]*D  + [5]*D    + [10]*D   + [5]*D    + [10]*D
t =       [800]*D + [1000]*D + [800]*D  + [600]*D  + [800]*D
cap =     [2]*D   + [2]*D    + [2]*D    + [2]*D    + [2]*D
p =       [30]*D  + [30]*D   + [30]*D   + [30]*D   + [30]*D
reopt =   [50]*D  + [50]*D   + [50]*D   + [50]*D   + [30]*D
horizon = [200]*D + [200]*D  + [300]*D  + [200]*D  + [200]*D
seeds = [i+j for i in [12314,34634,214,3245,1516] for j in [124,435,3,2357,137,1,2345,5754,7,12346,45673,1345,2135752,2342,5834,863,242342,23525,26264567,1324325,124235,1452362,15346,2347,564,124234,23214,4363456,1234,124]]*5
niter = 5

F = open('gen6.txt','w') 
time1 = []
time2 = []
val1 = []
val2 = []
for i in range(len(n)):
    print(i)
    r.seed(seeds[i])
    mod = model(p[i],100,100,n[i],m[i],cap[i],t[i], reopt[i], horizon[i])
    d = final_dispatcher()
    dyn = mod.simulate(d, ('dynamic_insert','label'))
    dyni = mod.simulate(d, ('dynamic_insert','reinsert'))
    both = mod.simulate(d, ('dynamic_insert', 'both'))
    F.write("&%.1f & %.1f && %.1f & %.1f && %.1f & %.1f\n" % (dyn[0], dyn[1],dyni[0], dyni[1], both[0], both[1]))
    val1.append(dyn[0])
    val2.append(dyni[0])
    time1.append(dyn[1])
    time2.append(dyni[1])
F.close()
#
#vall1 = [sum(val1[:D])/D, sum(val1[150:300])/150, sum(val1[300:450])/150, sum(val1[450:600])/150, sum(val1[600:750])/150]
#vall2 = [sum(val2[:D])/D, sum(val2[150:300])/150, sum(val2[300:450])/150, sum(val2[450:600])/150, sum(val2[600:750])/150]
#timee1 = [sum(time1[:D])/D, sum(time1[150:300])/150, sum(time1[300:450])/150, sum(time1[450:600])/150, sum(time1[600:750])/150]
#timee2 = [sum(time2[:D])/D, sum(time2[150:300])/150, sum(time2[300:450])/150, sum(time2[450:600])/150, sum(time2[600:750])/150]
# &2119.0 & 1.2 & 2135.0 & 0.9 & 1487.0 & 3.7 