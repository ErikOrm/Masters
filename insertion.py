"""
Not handling starting times
"""

from Dijkstra import *

def insert(user, vehicles):
    for vehicle in vehicles:
        v_cost = 0
        for node in vehicle.path:
            
        