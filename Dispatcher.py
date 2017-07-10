import random as r
import matplotlib.pyplot as plt
import math
from Dijkstra import *
import numpy as np
import time
from optim import opt
from scipy.spatial import Delaunay

class graph:
    
    def __init__(self, size, size_x, size_y):
        self.size = size #int
        self.size_x = size_x #m
        self.size_y = size_y #m
        self.initialise_nodes()
        self.initialse_arcs()
        
#
#    def initialise_nodes(self):
#        self.nodes = []
#        for i in range(0,math.ceil(self.size_x/10)):
#            for j in range(0,math.ceil(self.size_y/10)):
#                if (i+j) % 2 == 0:
#                    self.nodes.append(node(len(self.nodes)+1,i*10,j*10))
#            
#    def initialse_arcs(self):
#        self.arcs = []
#        for node_1 in self.nodes:
#            for node_2 in self.nodes:
#                if node_1 != node_2:
#                    if math.sqrt(pow(node_1.x-node_2.x,2) + pow(node_1.y-node_2.y,2)) < 15:
#                        self.arcs.append(arc(len(self.arcs)+1,node_1,node_2))
#                        self.arcs.append(arc(len(self.arcs)+1,node_2,node_1))
                        
                        
    def initialise_nodes(self):
        self.nodes = []
        for i in range(30):
            x = 100*r.random()
            y = 100*r.random()
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
        
def intersect(A,B,C,D):
    k1 = (B.y-A.y)/(B.x-A.x)
    k2 = (D.y-C.y)/(D.x-C.x)
    m1 = A.y-k1*A.x
    m2 = C.y-k2*C.x
    crossX = (m2-m1)/(k1-k2)
    if min(A.x, B.x) < crossX < max(A.x, B.x) and min(C.x, D.x) < crossX < max(C.x, D.x):
        return True
    else:
        return False

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
        self.users = []
        self.target_users = []
        self.target_node = []
        
        
    def __repr__(self):
        return "vehicle-%i" % self.ID
        
    
    def pickup(self, user, time):
        if (not self.node == user.start_node) or len(self.users) == self.capacity:
            pass# raise Exception("Disallowed pickup")
        elif time < user.start_time:
            return "wait"
        else:
#            print("pickup")
            self.target_users.remove(user)
            self.users.append(user)
            return "pickup"
            
            
    def dropoff(self, user):
        if (not self.node == user.end_node) or not user in self.users:
            raise Exception("Disallowed dropoff")
        else:
#            print("dropoff")
            self.users.remove(user)
            
    def assign(self, user):
        self.target_users.append(user)
        
    def deassign(self, user):
        if user in self.target_users:
            self.target_users.remove(user)
        else:
            raise Exception("%s is not in %s and can't be deassigned" % (user, self))
        
        
class model:
    
    def __init__(self, size, size_x, size_y, n_users, n_vehicles, vehicle_cap, time):
        
        self.graph = graph(size, size_x, size_y)
        self.create_user_template(n_users, time)
        self.create_vehicle_template(n_vehicles, vehicle_cap)
        self.time = time
        self.vehicle_cap = vehicle_cap
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
        if mode == 'dynamic':
            for user in self.users:
                time_user_dict[user.start_time].append(user)
        elif mode == 'static':
            for user in self.users:
                time_user_dict[1].append(user)
        self.at_node = {t:[] for t in range(1,self.time+1)}
        for vehicle in self.vehicles:
            self.at_node[1].append(vehicle)
        
        for t in range(1,self.time):
                    
            # ADD USERS
            self.unserved_users.extend(time_user_dict[t])
#            if mode == 'dynamic':
#                dispatcher.on_added_users(self, t, time_user_dict[t])
          
            # VEHICLE ARRIVALS, PICKUPS and DROPOFFS
            for vehicle in self.at_node[t]:
                if vehicle.path:
                    vehicle.node = vehicle.path[0]
                    vehicle.path = vehicle.path[1:]
#                    print("Reaches node %s at time %i" % (vehicle.node, t))
  
            # onNextTimestep
            dispatcher.on_next_timestep(self, t, self.vehicle_cap, mode)

                  
            for vehicle in self.at_node[t]:
#                print(vehicle)
#                print("-----")
                
                cont = True
                while cont:
                    cont = False
                    for user in vehicle.users:
                        if user.end_node == vehicle.node:
#                            print(vehicle)
#                            print("dropoff: %s" % user)
#                            print(user.start_node, user.end_node)
#                            print(t)
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
                        if user.start_node == vehicle.node:
#                            print(vehicle)
#                            print("pickup %s" % user)
#                            print(user.start_node, user.end_node)
#                            print(t)
                            res = vehicle.pickup(user, t)
                            if res == "wait":
                                vehicle.path = [vehicle.node] + vehicle.path
                                wait = True
                            elif  res == "pickup":
#                                self.waiting_times_dict[user] = t
                                self.unserved_users.remove(user)
                                dispatcher.on_pickup(self, vehicle)
                                cont = True
              


                if not wait and vehicle.path and math.ceil(self.dist_dict[(vehicle.node, vehicle.path[0])]) > 0:
                    try:
                        self.at_node[t+math.ceil(self.dist_dict[(vehicle.node, vehicle.path[0])])].append(vehicle)
                    except:
                        self.at_node[t+1].append(vehicle)
                else:
                    self.at_node[t+1].append(vehicle)
            

            self.at_node[t] = []
            
            
        for t in range(1,self.time):
            for user in time_user_dict[t]:
                self.waiting_times_dict[user] = self.waiting_times_dict[user]-user.start_time
        
        print(time.time()-start_time)
              

        return [np.mean([x for x in self.waiting_times_dict.values() if x != np.inf]), self.n_served]
            
          
class final_dispatcher():
    
    def __init__(self):
        self.to_update = []

    def on_next_timestep(self, model, t, Q_max, mode):
        
        err_penalty = 2000
        n_iter = 150
        freq = 50
        if mode == 'static':
            freq = 10000
            T = model.time
            d_val = model.time
        elif mode == 'dynamic':
            T = min(model.time-t, 200)
            d_val = T

        if t % freq == 1:
            
            print("t: %i" % t)
            
            passenger_dict = {}
            passengers = []
            l = 0
            arrival_dict = {c:0 for c in range(len(model.vehicles))}
            tmp_passenger_no = 0
            keep_track_of_passengers_dict = {}
            for vehicle in model.vehicles:
                vehicle.target_users = []
                passenger_dict[model.vehicles.index(vehicle)] = []
                for user in vehicle.users:
                    passenger_dict[model.vehicles.index(vehicle)].append(tmp_passenger_no)
                    keep_track_of_passengers_dict[tmp_passenger_no] = user
                    tmp_passenger_no = tmp_passenger_no + 1
                passengers.extend(vehicle.users)
                l += len(vehicle.users)
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
                
            for tt in range(t, min(model.time, t+T)):
                for vehicle in model.at_node[tt]:
                    arrival_dict[model.vehicles.index(vehicle)] = tt-t
            
            starting_times = {("n%i" % (i + 1)):(max(0,model.unserved_users[i].start_time-t)) for i in range(n)}
            
            print([(x, x.start_node, x.end_node, x.start_time) for x in model.unserved_users])
            ret_dict = opt(travel_times, m, n, l, passenger_dict, arrival_dict, starting_times, d_val, T, Q_max, err_penalty, n_iter)
            #ret_dict = {1: ['n21', 'n8', 'n7', 'n18', 'n6', 'n17', 'n1', 'n16', 'n3', 'n13', 'n11', 'n23'], 2: ['n22', 'n9', 'n10', 'n20', 'n5', 'n15', 'n19', 'n4', 'n2', 'n14', 'n12', 'n23']}
            print(ret_dict)

            duplicate_list = []
            for i in range(len(ret_dict)):
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
                for j in tmp_path:
                    if j<n:
                        vehicle.target_users.append(model.unserved_users[j])
                        vehicle.path.extend(dijkstra(vehicle.path[-1], model.unserved_users[j].start_node, model.graph.nodes, model.graph.arcs)[0])
                    elif n<=j<2*n:
                        vehicle.path.extend(dijkstra(vehicle.path[-1], model.unserved_users[j-n].end_node, model.graph.nodes, model.graph.arcs)[0])
                    elif 2*n<=j<2*n+m:
                        vehicle.path.append(next_node)
                    elif 2*n+m<=j<2*n+m+l:
                        vehicle.path.extend(dijkstra(vehicle.path[-1], keep_track_of_passengers_dict[(j-2*n-m)].end_node, model.graph.nodes, model.graph.arcs)[0])

#                print(vehicle.path)
                        
    def on_pickup(self, model, vehicle):
        pass
    
    def on_dropoff(self, model, vehicle):
        pass
  
#    def on_added_users(self, model, t, users):
#        
#        for user in users:
#            insert(user, model.vehicles)
#        
        
        
        
        
        
        
        
        
    
times_final = 0
n_final = 0
times_final2 = 0
n_final2 = 0

r.seed(52363)
mod = model(0,100,100,50,10,2,600)
d = final_dispatcher()
tmp_list = mod.simulate(d, 'dynamic')
times_final = times_final + tmp_list[0]
n_final = n_final + tmp_list[1]
tmp_list = mod.simulate(d, 'static')
times_final2 = times_final2 + tmp_list[0]
n_final2 = n_final2 + tmp_list[1]
    
print(times_final)
print(n_final)
print(times_final*n_final + (50-n_final)*400)
print(times_final2)
print(n_final2)
print(times_final2*n_final2 + (50-n_final2)*400)

