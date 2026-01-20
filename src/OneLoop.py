from z3 import *

L = [
lambda x :(((True and (True and (x[0] < 10)) ) if (x[0] < 10) else (True and (True and (not(x[0] < 10))) ) ) and (True and (x[0] != 0)) ),
lambda x :[((x[0] + 1) if (x[0] < 10) else (x[1] - 1) ), ((x[1] - 1) if (x[0] < 10) else (x[1] - 1) ), ],
2,
0,
lambda x :[If(( x[0]< 10), ( x[0]+ 1), ( x[1]- 1) ), If(( x[0]< 10), ( x[1]- 1), ( x[1]- 1) ), ],
lambda x :And(If(( x[0]< 10), And(True, (And( True, ( x[0]< 10))) ), And(True, (And( True, (Not(x[0] < 10)))) ) ), (And( True, ( x[0]!= 0))) ),
False,
]
