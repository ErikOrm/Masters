# -*- coding: utf-8 -*-
import numpy as np

def dijkstra(start_node, end_node, nodes, arcs):
    
    len_dict = {node:np.inf for node in nodes}
    len_dict[start_node] = 0
    
    ancestor_dict = {}
    
    current_node = start_node
    
    while current_node != end_node:
        
        for arc in [arc for arc in arcs if arc.start_node == current_node and arc.end_node in len_dict.keys()]:
            length = len_dict[current_node]+arc.length
            if length < len_dict[arc.end_node]:
                ancestor_dict[arc.end_node] = current_node
                len_dict[arc.end_node] = length
        
        len_dict.pop(current_node,None)
        current_node = [node for node in len_dict.keys() if len_dict[node] == min(len_dict.values())][0]

    path = [end_node]
    while path[-1] != start_node:
        path.append(ancestor_dict[path[-1]])
    return (path[-2::-1], len_dict[end_node])