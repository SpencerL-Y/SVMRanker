from z3 import *

L = [
lambda x :((((((True and True ) and (True and (not((-1073741823 <= 0) and (0 <= 1073741823)))) ) if (not((-1073741823 <= 0) and (0 <= 1073741823))) else ((True and True ) and (True and (not(not((-1073741823 <= 0) and (0 <= 1073741823))))) ) ) and (True and (__VERIFIER_nondet_int() != 0)) ) if (__VERIFIER_nondet_int() != 0) else (True and (True and (not(__VERIFIER_nondet_int() != 0))) ) ) and (True and ((x[0] >= x[1]) and (x[0] <= (x[3] + x[2])))) ),
lambda x :[((0 if (not((-1073741823 <= 0) and (0 <= 1073741823))) else 0 ) if (__VERIFIER_nondet_int() != 0) else x[0] ), ((x[1] if (not((-1073741823 <= 0) and (0 <= 1073741823))) else x[1] ) if (__VERIFIER_nondet_int() != 0) else (x[1] + 1) ), (((x[2] - 1) if (not((-1073741823 <= 0) and (0 <= 1073741823))) else (x[2] - 1) ) if (__VERIFIER_nondet_int() != 0) else x[2] ), ((x[0] if (not((-1073741823 <= 0) and (0 <= 1073741823))) else x[0] ) if (__VERIFIER_nondet_int() != 0) else x[3] ), ],
4,
0,
lambda x :[If(( __VERIFIER_nondet_int()!= 0), If((Not((-1073741823 <= 0) and (0 <= 1073741823))), 0, 0 ), x[0] ), If(( __VERIFIER_nondet_int()!= 0), If((Not((-1073741823 <= 0) and (0 <= 1073741823))), x[1], x[1] ), ( x[1]+ 1) ), If(( __VERIFIER_nondet_int()!= 0), If((Not((-1073741823 <= 0) and (0 <= 1073741823))), ( x[2]- 1), ( x[2]- 1) ), x[2] ), If(( __VERIFIER_nondet_int()!= 0), If((Not((-1073741823 <= 0) and (0 <= 1073741823))), x[0], x[0] ), x[3] ), ],
lambda x :And(If(( __VERIFIER_nondet_int()!= 0), And(If((Not((-1073741823 <= 0) and (0 <= 1073741823))), And(And(True, True ), (And( True, (Not((-1073741823 <= 0) and (0 <= 1073741823))))) ), And(And(True, True ), (And( True, (Not(not((-1073741823 <= 0) and (0 <= 1073741823)))))) ) ), (And( True, ( __VERIFIER_nondet_int()!= 0))) ), And(True, (And( True, (Not(__VERIFIER_nondet_int() != 0)))) ) ), (And( True, (And( ( x[0]>= x[1]), ( x[0]<= ( x[3]+ x[2])))))) ),
False,
]


__VERIFIER_NONDET_COUNTER = 0

def __VERIFIER_nondet_int():
    global __VERIFIER_NONDET_COUNTER
    __VERIFIER_NONDET_COUNTER += 1
    try:
        from z3 import Int, is_expr
        import inspect
        frame = inspect.currentframe()
        if frame and frame.f_back:
            caller_locals = frame.f_back.f_locals
            x = caller_locals.get('x')
            if isinstance(x, (list, tuple)) and any(is_expr(item) for item in x):
                return Int(f"__VERIFIER_nondet_int_{__VERIFIER_NONDET_COUNTER}")
    except Exception:
        pass
    import random
    return random.randint(-10, 10)
