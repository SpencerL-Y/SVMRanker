from z3 import *

L = [
lambda x :(True and True),
lambda x :[(x[0] + 1), ],
1,
0,
lambda x :[( x[0]+ 1), ],
lambda x :(And( True, True)),
False,
]
