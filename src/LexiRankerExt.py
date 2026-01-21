'''
Lexicographic ranking function learner (CEGIS-based).
'''
import math
import z3

from Util import get_condition, get_statement, get_xpoints, is_type_real, _is_finite_list
from FindMultiphaseUtilExt import generateTemplatesStrategyExt

def _basis_from_template(template, num_vars):
    basis = []
    for row in template:
        powers = list(row[:num_vars])
        basis.append(powers)
    return basis

def _eval_monomial(powers, values):
    result = 1.0
    for idx, power in enumerate(powers):
        if power == 0:
            continue
        result *= values[idx] ** power
    return result

def _eval_monomial_z3(powers, vars_):
    result = z3.RealVal(1)
    for idx, power in enumerate(powers):
        if power == 0:
            continue
        term = vars_[idx]
        for _ in range(int(power) - 1):
            term = term * vars_[idx]
        result = result * term
    return result

def _eval_linear(basis, coeffs, values):
    total = 0.0
    for c, powers in zip(coeffs, basis):
        total += c * _eval_monomial(powers, values)
    return total

def _eval_linear_z3(basis, coeffs, vars_):
    total = z3.RealVal(0)
    for c, powers in zip(coeffs, basis):
        total = total + z3.RealVal(c) * _eval_monomial_z3(powers, vars_)
    return total

def _lexi_pred(fx, fxp):
    clauses = []
    prefix = []
    for i in range(len(fx)):
        if i == 0:
            clauses.append(fxp[i] < fx[i])
            prefix.append(fxp[i] <= fx[i])
        else:
            clauses.append(z3.And(*prefix, fxp[i] < fx[i]))
            prefix.append(fxp[i] <= fx[i])
    return z3.Or(*clauses)

def _z3_to_float(value):
    if z3.is_int_value(value):
        return float(value.as_long())
    if z3.is_rational_value(value):
        return float(value.numerator_as_long() / value.denominator_as_long())
    text = str(value)
    if text.endswith("?"):
        text = text[:-1]
    try:
        return float(text)
    except ValueError:
        return 0.0

def _guard_and_prime(L):
    if is_type_real(L):
        return L[-1], L[-2], True
    return L[-2], L[-3], False

def _sample_transitions(L, sample_strategy, min_samples, print_level):
    n = L[2]
    base_point = [0] * n
    m = 5
    h = 1.0
    if not is_type_real(L):
        h = 1
        m = int(max((100 ** (1 / n)) / 2, 0))
    samples = []
    attempts = 0
    while len(samples) < min_samples and attempts < 6:
        for p in get_xpoints(m, h, n, base_point):
            if get_condition(L, p):
                p_ = get_statement(L, p)
                if p_ is None or not _is_finite_list(p_):
                    continue
                samples.append((p, p_))
        attempts += 1
        if sample_strategy == "CONSTRAINT":
            h = max(h * 0.5, 0.5)
            m = max(m, 5)
        else:
            m = 2 * m
            h = 1.5 * h
    if print_level > 1:
        print("sampled transitions:", len(samples))
    return samples

def _solve_coeffs(samples, basis, depth, print_level):
    if not samples:
        return None
    coeffs = []
    solver = z3.Solver()
    for i in range(depth):
        row = [z3.Real(f"c_{i}_{j}") for j in range(len(basis))]
        coeffs.append(row)
        solver.add(z3.Or([c != 0 for c in row]))
        for c in row:
            solver.add(c >= -10, c <= 10)
    for x, xp in samples:
        fx = []
        fxp = []
        for i in range(depth):
            fx.append(sum(c * _eval_monomial(p, x) for c, p in zip(coeffs[i], basis)))
            fxp.append(sum(c * _eval_monomial(p, xp) for c, p in zip(coeffs[i], basis)))
        for i in range(depth):
            solver.add(fx[i] >= 0)
        solver.add(_lexi_pred(fx, fxp))
    if solver.check() != z3.sat:
        if print_level > 1:
            print("lexi: no coefficients for current samples")
        return None
    model = solver.model()
    result = []
    for row in coeffs:
        result.append([_z3_to_float(model.eval(c)) for c in row])
    # convert to floats for later z3 construction
    return result

def _verify(L, basis, coeffs, print_level):
    cond, prime, tr = _guard_and_prime(L)
    n = L[2]
    x = [z3.Real(f"xr_{i}") if tr else z3.Int(f"xi_{i}") for i in range(n)]
    xp = prime(x)
    fx = []
    fxp = []
    for row in coeffs:
        fx.append(_eval_linear_z3(basis, row, x))
        fxp.append(_eval_linear_z3(basis, row, xp))
    bad = z3.Or(z3.Or([f < 0 for f in fx]), z3.Not(_lexi_pred(fx, fxp)))
    s = z3.Solver()
    s.add(cond(x))
    s.add(bad)
    if s.check() == z3.sat:
        model = s.model()
        ce = [model.eval(v, model_completion=True) for v in x]
        ce = [_z3_to_float(v) for v in ce]
        if print_level > 1:
            print("lexi counterexample:", ce)
        return False, ce
    return True, None

def LearnLexiRankerExt(L, depth_bound, template_strategy, sample_strategy, print_level):
    templates = generateTemplatesStrategyExt(template_strategy, L[2])
    if not templates:
        return 'UNKNOWN', []
    template = templates[0]
    basis = _basis_from_template(template, L[2])
    samples = _sample_transitions(L, sample_strategy, 20, print_level)
    for depth in range(1, depth_bound + 1):
        if print_level > 0:
            print("lexi depth:", depth)
        current_samples = list(samples)
        for _ in range(20):
            coeffs = _solve_coeffs(current_samples, basis, depth, print_level)
            if coeffs is None:
                break
            ok, ce = _verify(L, basis, coeffs, print_level)
            if ok:
                return 'TERMINATE', coeffs
            if ce is None:
                return 'UNKNOWN', []
            ce_p = get_statement(L, ce)
            if ce_p is None or not _is_finite_list(ce_p):
                break
            current_samples.append((ce, ce_p))
    return 'UNKNOWN', []
