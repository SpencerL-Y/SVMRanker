from z3 import *

L = [
lambda x :(True and ((x[0] < 0.0) and ((x[1] < 0.0) and ((x[2] < 0.0) and ((x[2] < (7.0 * x[1])) and (x[1] < (11.0 * x[0]))))))),
lambda x :[(2.0 * x[0]), (3.0 * x[1]), (5.0 * x[2]), ],
3,
0,
lambda x :[( 2.0* x[0]), ( 3.0* x[1]), ( 5.0* x[2]), ],
lambda x :(And( True, (And( ( x[0]< 0.0), (And( ( x[1]< 0.0), (And( ( x[2]< 0.0), (And( ( x[2]< ( 7.0* x[1])), ( x[1]< ( 11.0* x[0])))))))))))),
]
T = [
[1, 0, 0, 0], 
[0, 1, 0, 0], 
[0, 0, 1, 0]]
