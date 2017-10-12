# Masters

The program is run by creating a model object in the dispatcher class:

mod = model(p,x,y,n,m,cap,t, reopt, horizon)

p: nbr of nodes
x,y: size of map rectangle
n: nbr of customers
m: nbr of cars
cap: car capacity
t: simulation time
reopt: reoptimisation time
horizon: reoptimsation horizon


Then create a dispatcher (create a final_dispatcher, dunno if the other work):

d = final_dispatcher()


Then run the simulation (the first arg is whether the insertion heuristic should be used and the second is which method to use for the subproblems):

dyn = mod.simulate(d, ('dynamic_insert','label'))


['dynamic', 'static', 'dynamic_insert'], ['label', 'reinsert', 'both']

