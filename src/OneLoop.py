from z3 import *

L = [
lambda x :(True and True),
lambda x :[(x[0] + 1), (x[1] + 2), ],
2,
0,
lambda x :[( x[0]+ 1), ( x[1]+ 2), ],
lambda x :(And( True, True)),
False,
]
