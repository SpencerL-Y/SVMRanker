from z3 import *

L = [
lambda x :(True and (((x[0] + x[1]) >= 1.0) and ((x[0] + 1.0) <= 0.0))),
lambda x :[(2.5 * x[0]), (3.0 * x[1]), ],
2,
0,
lambda x :[( 2.5* x[0]), ( 3.0* x[1]), ],
lambda x :(And( True, (And( ( ( x[0]+ x[1])>= 1.0), ( ( x[0]+ 1.0)<= 0.0))))),
]
T = [
[1, 0, 0], 
[0, 1, 0]]
