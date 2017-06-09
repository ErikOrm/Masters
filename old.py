# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 12:10:10 2017

@author: Snok
"""

def simulate_FIFO(self):
        
        start_time = time.time()
        self.unserved_users = []
        self.n_served = 0
        self.waiting_times_dict = {user:np.inf for user in self.users}
        time_user_dict = {t:[] for t in range(1,self.time+1)}
        for user in self.users:
            time_user_dict[user.start_time].append(user)
        
        arrival_dict = {t:[] for t in range(1,self.time+1)}
        arrival_dict[1] = self.vehicles
        
        
        for t in range(1,self.time):
            # ADD USERS
            self.unserved_users.extend(time_user_dict[t])
            
            # Car Decisions
            for vehicle in arrival_dict[t]:
                if vehicle.path:
                    arc = [arc for arc in self.graph.arcs if arc.start_node == vehicle.node and arc.end_node == vehicle.path[0]][0]
                    try:
                        arrival_dict[t+arc.length].append(vehicle)
                    except:
                        #print("Couldn't fit")
                        pass
                    vehicle.node = vehicle.path[0]
                    vehicle.path = vehicle.path[1:]
                elif vehicle.target_users:
                    self.waiting_times_dict[vehicle.target_users[0]] = t
                    vehicle.pick_up(vehicle.target_users[0])
                    vehicle.path = d.dijkstra(vehicle.users[0].start_node, vehicle.users[0].end_node, self.graph.nodes, self.graph.arcs)[0]
                    arrival_dict[t+1].append(vehicle)
                elif vehicle.users:
                    vehicle.drop_off(vehicle.users[0])
                    self.n_served = self.n_served + 1
                    arrival_dict[t+1].append(vehicle)
            
            for user in self.unserved_users:
                if arrival_dict[t]:
                    dist_vehicles_dict = {}
                    for vehicle in [vehicle for vehicle in arrival_dict[t] if (not vehicle.target_users) and (not vehicle.users)]:
                        length = self.dist_dict[(vehicle.node, user.start_node)]
                        dist_vehicles_dict[length] = vehicle
                    if dist_vehicles_dict:                      
                        vehicle = dist_vehicles_dict[min(dist_vehicles_dict.keys())]
                        vehicle.target_users.append(user)
                        self.unserved_users.remove(user)
                        arrival_dict[t+1].append(vehicle)
                        arrival_dict[t].remove(vehicle)
                        vehicle.path = d.dijkstra(vehicle.node, user.start_node, self.graph.nodes, self.graph.arcs)[0]
                    
            for vehicle in self.vehicles:
                if (not vehicle.path) and (not vehicle.target_users) and (not vehicle.users):
                    arrival_dict[t+1].append(vehicle)
            
            
            arrival_dict[t] = []
            
        for t in range(1,self.time):
            for user in time_user_dict[t]:
                self.waiting_times_dict[user] = self.waiting_times_dict[user]-t
        
        print(time.time()-start_time)

        return [np.mean([x for x in self.waiting_times_dict.values() if x != np.inf]), self.n_served]
        
        
    def simulate_CC(self):
        
        start_time = time.time()
        self.unserved_users = []
        self.n_served = 0
        self.waiting_times_dict = {user:np.inf for user in self.users}
        time_user_dict = {t:[] for t in range(1,self.time+1)}
        for user in self.users:
            time_user_dict[user.start_time].append(user)
        
        arrival_dict = {t:[] for t in range(1,self.time+1)}
        arrival_dict[1] = self.vehicles
        
        
        for t in range(1,self.time):
            # ADD USERS
            self.unserved_users.extend(time_user_dict[t])
            
            # Car Decisions
            for vehicle in arrival_dict[t]:
                if vehicle.path:
                    arc = [arc for arc in self.graph.arcs if arc.start_node == vehicle.node and arc.end_node == vehicle.path[0]][0]
                    try:
                        arrival_dict[t+arc.length].append(vehicle)
                    except:
                        #print("Couldn't fit")
                        pass
                    vehicle.node = vehicle.path[0]
                    vehicle.path = vehicle.path[1:]
                elif vehicle.target_users:
                    self.waiting_times_dict[vehicle.target_users[0]] = t
                    vehicle.pick_up(vehicle.target_users[0])
                    vehicle.path = d.dijkstra(vehicle.users[0].start_node, vehicle.users[0].end_node, self.graph.nodes, self.graph.arcs)[0]
                    arrival_dict[t+1].append(vehicle)
                elif vehicle.users:
                    vehicle.drop_off(vehicle.users[0])
                    self.n_served = self.n_served + 1
                    arrival_dict[t+1].append(vehicle)
            
        
            if arrival_dict[t]:
                for vehicle in [vehicle for vehicle in arrival_dict[t] if (not vehicle.target_users) and (not vehicle.users)]:
                    dist_user_dict = {}
                    for user in self.unserved_users:
                        length = self.dist_dict[(vehicle.node, user.start_node)]
                        dist_user_dict[length] = user
                    if dist_user_dict:                      
                        user = dist_user_dict[min(dist_user_dict.keys())]
                        vehicle.target_users.append(user)
                        self.unserved_users.remove(user)
                        arrival_dict[t+1].append(vehicle)
                        arrival_dict[t].remove(vehicle)
                        vehicle.path = d.dijkstra(vehicle.node, user.start_node, self.graph.nodes, self.graph.arcs)[0]
                
            for vehicle in self.vehicles:
                if (not vehicle.path) and (not vehicle.target_users) and (not vehicle.users):
                    arrival_dict[t+1].append(vehicle)
            
            arrival_dict[t] = []
            
        for t in range(1,self.time):
            for user in time_user_dict[t]:
                self.waiting_times_dict[user] = self.waiting_times_dict[user]-t

        print(time.time()-start_time)
        return [np.mean([x for x in self.waiting_times_dict.values() if x != np.inf]), self.n_served]

    def simulate_RE(self):
        ## FIX PATHS AND ARRIVAL_DICTS
        
        start_time = time.time()
        self.unserved_users = []
        self.n_served = 0
        self.waiting_times_dict = {user:np.inf for user in self.users}
        time_user_dict = {t:[] for t in range(1,self.time+1)}
        for user in self.users:
            time_user_dict[user.start_time].append(user)
        
        arrival_dict = {t:[] for t in range(1,self.time+1)}
        arrival_dict[1] = self.vehicles
        
        
        for t in range(1,self.time):
#            print(t)
            # ADD USERS
            self.unserved_users.extend(time_user_dict[t])
            # Car Decisions
            for vehicle in arrival_dict[t]:
                if vehicle.users:
                    if vehicle.path:
                        try:
                            arrival_dict[t+math.ceil(self.dist_dict[(vehicle.node, vehicle.path[0])])].append(vehicle)
                        except:
                            pass
                        vehicle.node = vehicle.path[0]
                        vehicle.path = vehicle.path[1:]
                    else:
                        vehicle.drop_off(vehicle.users[0])
                        self.n_served = self.n_served + 1
                elif vehicle.target_users:
                    if not vehicle.path:
                        self.waiting_times_dict[vehicle.target_users[0]] = t
                        vehicle.pick_up(vehicle.target_users[0])
                        vehicle.path = d.dijkstra(vehicle.users[0].start_node, vehicle.users[0].end_node, self.graph.nodes, self.graph.arcs)[0]
                        try:
                            arrival_dict[t+math.ceil(self.dist_dict[(vehicle.node, vehicle.path[0])])].append(vehicle)
                        except:
                            pass
                        vehicle.node = vehicle.path[0]
                        vehicle.path = vehicle.path[1:]
                
                
            unoccupied_vehicles  = [vehicle for vehicle in self.vehicles if (not vehicle.users) and (not vehicle.target_users)]
            if self.unserved_users and unoccupied_vehicles:
                if len(unoccupied_vehicles) < len(self.unserved_users):
                    for vehicle in unoccupied_vehicles:
                        min_len = np.inf
                        if self.unserved_users:
                            for user in self.unserved_users:
                                length = self.dist_dict[(vehicle.node, user.start_node)]
                                if length < min_len:
                                    the_user = user
                                    min_len = length
#                            print("Assign")
                            vehicle.target_users.append(the_user)
                            self.unserved_users.remove(the_user)          
                else:
                    served_users = []
                    for user in self.unserved_users:
                        min_len = np.inf
                        if unoccupied_vehicles:
                            for vehicle in unoccupied_vehicles:    
                                length = self.dist_dict[(vehicle.node, user.start_node)]
                                if length < min_len:
                                    the_vehicle = vehicle
                                    min_len = length
#                                print("Assign2")
                            the_vehicle.target_users.append(user)
                            unoccupied_vehicles.remove(the_vehicle)
                            served_users.append(user)
                    for user in served_users:
                        self.unserved_users.remove(user)
                            
                requested_vehicles = [vehicle for vehicle in self.vehicles if (not vehicle.users)]
                for i in range(len(requested_vehicles)):
#                    gainz = []
                    for j in range(i+1,len(requested_vehicles)):
                        if requested_vehicles[i].target_users:
                            c1 = self.dist_dict[(requested_vehicles[i].node, requested_vehicles[i].target_users[0].start_node)]
                            n2 = self.dist_dict[(requested_vehicles[j].node, requested_vehicles[i].target_users[0].start_node)]
                        else:
                            c1 = 0
                            n2 = 0
                        if requested_vehicles[j].target_users:
                            c2 = self.dist_dict[(requested_vehicles[j].node, requested_vehicles[j].target_users[0].start_node)]
                            n1 = self.dist_dict[(requested_vehicles[i].node, requested_vehicles[j].target_users[0].start_node)]
                        else:
                            c2 = 0
                            n1 = 0

                        if c1 + c2 > n1 + n2:

                            print("swap")
                            if requested_vehicles[i].target_users:
                                if requested_vehicles[j].target_users:
                                    user1 = requested_vehicles[i].target_users[0]
                                    user2 = requested_vehicles[j].target_users[0]
                                    requested_vehicles[i].target_users.remove(user1)
                                    requested_vehicles[i].target_users.append(user2)
                                    requested_vehicles[j].target_users.remove(user2)
                                    requested_vehicles[j].target_users.append(user1)
                                else:
                                    user1 = requested_vehicles[i].target_users[0]
                                    requested_vehicles[i].target_users.remove(user1)
                                    requested_vehicles[j].target_users.append(user1)
                                    
                            else:
                                user1 = requested_vehicles[i].target_users[0]
                                requested_vehicles[i].target_users.remove(user1)
                                requested_vehicles[j].target_users.append(user1)
                            requested_vehicles[i].path = []
                            requested_vehicles[j].path = []



            for vehicle in self.vehicles:
                if (not vehicle.target_users) and (not vehicle.users):
                    arrival_dict[t+1].append(vehicle)
                elif vehicle.target_users and not vehicle.users:
                    if not vehicle.path and vehicle.target_users[0].start_node != vehicle.node:
#                        print("Gets path")
                        vehicle.path = d.dijkstra(vehicle.node, vehicle.target_users[0].start_node, self.graph.nodes, self.graph.arcs)[0]
                    if vehicle in arrival_dict[t] and vehicle.target_users[0].start_node != vehicle.node:
                        try:
                            arrival_dict[t+math.ceil(self.dist_dict[(vehicle.node, vehicle.path[0])])].append(vehicle)
                        except:
                            pass
#                        print("Moves")
                        vehicle.node = vehicle.path[0]
                        vehicle.path = vehicle.path[1:]
                    else:
                        arrival_dict[t+1].append(vehicle)

                        

            arrival_dict[t] = []

        for t in range(1,self.time):
            for user in time_user_dict[t]:
                self.waiting_times_dict[user] = self.waiting_times_dict[user]-t
        
        print(time.time()-start_time)
        return [np.mean([x for x in self.waiting_times_dict.values() if x != np.inf]), self.n_served]

#  size, size_x, size_y, n_users, n_vehicles, vehicle_cap, time
times_fifo = 0
n_fifo = 0
times_cc = 0
n_cc = 0
times_re = 0
n_re = 0
n_iter = 5
for i in range(n_iter):
    D = dispatcher(30,1000,1000,1000,50,2,5000)
    tmp_list = D.simulate_FIFO()
    times_fifo = times_fifo + tmp_list[0]
    n_fifo = n_fifo + tmp_list[1]    
#    E = dispatcher(30,1000,1000,1000,50,2,1000)
#    tmp_list = E.simulate_CC()
#    times_cc = times_cc + tmp_list[0]
#    n_cc = n_cc + tmp_list[1]    
    F = dispatcher(30,1000,1000,1000,50,2,5000)
    tmp_list = F.simulate_RE()
    times_re = times_re + tmp_list[0]
    n_re = n_re + tmp_list[1]  
print(times_fifo/n_iter)
print(n_fifo/n_iter)
#print(times_cc/n_iter)
#print(n_cc/n_iter)
print(times_re/n_iter)
print(n_re/n_iter)
