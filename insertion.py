"""
Not handling starting times
"""

from Dijkstra import *

def insert(user, model, t):
    
    dist_dict = model.dist_dict
    best_cost = 10000
    best_vehicle  = []
    best_path = []
    for vehicle in model.vehicles:
        v_cost = 10000
        v_path = []

        cost = 0
        if vehicle.short_path:
            if vehicle in model.at_node[t]:
                start_node = vehicle.node
            else:
                start_node = vehicle.path[0] 
            load = len(vehicle.users)
            time = vehicle.arrival_time
            T_path = [(start_node, 'k')] + vehicle.short_path
            for k in range(len(T_path)-1):
                time  = time + dist_dict[(T_path[k][0], T_path[k+1][0])]
                if T_path[k+1][1] =='s':
                    #time = max([time, user.start_time]) # ERROR
                    load = load + 1
                if T_path[k+1][1] =='e':
                    cost = cost + time
                    load = load - 1
                assert load <= model.vehicle_cap
        base_cost = cost
                
        for i in range(len(vehicle.short_path)+1):
            for j in range(i,len(vehicle.short_path)+1):
                tmp_path = vehicle.short_path[:i] + [(user.start_node, 's1')] + vehicle.short_path[i:j] + [(user.end_node, 'e1')] + vehicle.short_path[j:]
                cost = 0
                if vehicle in model.at_node[t]:
                    start_node = vehicle.node
                else:
                    start_node = vehicle.path[0] 
                time = vehicle.arrival_time
                load = len(vehicle.users)
                T_path = [(start_node,'k')] + tmp_path
                for k in range(len(T_path)-1):
                    time  = time + dist_dict[(T_path[k][0], T_path[k+1][0])]
                    if T_path[k+1][1] in ['s', 's1']:
                        #time = max([time, user.start_time])  # ERROR
                        load = load + 1
                    if T_path[k+1][1] in ['e', 'e1']:
                        cost = cost + time
                        load = load - 1
                    if load > model.vehicle_cap:
                        cost = 10000
                        
                if cost-base_cost<v_cost:
                    v_path = tmp_path
                    v_cost = cost-base_cost
                    v_start = start_node
        if v_cost < best_cost:
            best_cost = v_cost
            best_path = v_path
            best_vehicle = vehicle
            best_start = v_start
            
    
            
    build_path = [best_start]
    order = 0
    best_vehicle.short_path = []
    for i in range(len(best_path)):
        best_vehicle.short_path.append(best_path[i])
        build_path.extend(model.path_dict[(build_path[-1], best_path[i][0])])
        if best_path[i][1] == 's':
            order = order + 1
        if best_path[i][1] == 's1':
            best_vehicle.target_users = best_vehicle.target_users[:order] + [user] + best_vehicle.target_users[order:]
    best_vehicle.path = build_path
    
    for i in range(len(best_vehicle.short_path)):
        if best_vehicle.short_path[i][1] == 's1':
            best_vehicle.short_path[i] = (best_vehicle.short_path[i][0],'s')
        elif best_vehicle.short_path[i][1] == 'e1':
            best_vehicle.short_path[i] = (best_vehicle.short_path[i][0],'e')         



            