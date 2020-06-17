from z3 import *

L = [
lambda x :(((True and (True and (__VERIFIER_nondet_int() != 0)) ) if (__VERIFIER_nondet_int() != 0) else (True and (True and (not(__VERIFIER_nondet_int() != 0))) ) ) and (True and (x[1] <= x[2])) ),
lambda x :[((x[0] + 1) if (__VERIFIER_nondet_int() != 0) else (x[0] - 1) ), ((x[1] + 1) if (__VERIFIER_nondet_int() != 0) else (x[1] + 1) ), (x[2] if (__VERIFIER_nondet_int() != 0) else x[2] ), ],
3,
0,
lambda x :[If(( __VERIFIER_nondet_int()!= 0), ( x[0]+ 1), ( x[0]- 1) ), If(( __VERIFIER_nondet_int()!= 0), ( x[1]+ 1), ( x[1]+ 1) ), If(( __VERIFIER_nondet_int()!= 0), x[2], x[2] ), ],
lambda x :And(If(( __VERIFIER_nondet_int()!= 0), And(True, (And( True, ( __VERIFIER_nondet_int()!= 0))) ), And(True, (And( True, (Not(__VERIFIER_nondet_int() != 0)))) ) ), (And( True, ( x[1]<= x[2]))) ),
False,
]
T = [
[1, 0, 0, 0], 
[0, 1, 0, 0], 
[0, 0, 1, 0], 
[1, 0, 0, 0], 
[0, 1, 0, 0], 
[0, 0, 1, 0], 
[1, 0, 0, 0], 
[0, 1, 0, 0], 
[0, 0, 1, 0], 
[1, 0, 0, 0], 
[0, 1, 0, 0], 
[0, 0, 1, 0], 
[1, 0, 0, 0], 
[0, 1, 0, 0], 
[0, 0, 1, 0], 
[1, 0, 0, 0], 
[0, 1, 0, 0], 
[0, 0, 1, 0]]
