from z3 import *

L = [
lambda x :(True and (x[2] > 0)),
lambda x :[((3 * x[0]) - (4 * x[1])), ((4 * x[0]) + (3 * x[1])), ((x[2] + x[0]) - 1), x[0], ],
4,
0,
lambda x :[( ( 3* x[0])- ( 4* x[1])), ( ( 4* x[0])+ ( 3* x[1])), ( ( x[2]+ x[0])- 1), x[0], ],
lambda x :(And( True, ( x[2]> 0))),
False,
]
