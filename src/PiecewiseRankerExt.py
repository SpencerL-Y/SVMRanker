'''
Piecewise ranking function learner (CEGIS-based).
'''
import z3

from Util import get_statement, is_type_real, _is_finite_list
from FindMultiphaseUtilExt import generateTemplatesStrategyExt
from LexiRankerExt import (
    _basis_from_template,
    _eval_monomial,
    _eval_monomial_z3,
    _sample_transitions,
    _guard_and_prime,
    _z3_to_float,
)


def _make_vars(num_vars, use_real):
    if use_real:
        return [z3.Real(f"x{i}") for i in range(num_vars)]
    return [z3.Int(f"x{i}") for i in range(num_vars)]


def _parse_predicates(predicates, num_vars, use_real):
    xvars = _make_vars(num_vars, use_real)
    env = {
        "And": z3.And,
        "Or": z3.Or,
        "Not": z3.Not,
        "Implies": z3.Implies,
        "If": z3.If,
        "Abs": z3.Abs,
        "x": xvars,
    }
    for i, var in enumerate(xvars):
        env[f"x{i}"] = var
    parsed = []
    for text in predicates:
        expr = eval(text, {"__builtins__": {}}, env)
        if not z3.is_bool(expr):
            raise ValueError(f"predicate is not boolean: {text}")
        parsed.append(z3.simplify(expr))
    return xvars, parsed


def _extract_ite_predicates(L, use_real):
    _, prime, _ = _guard_and_prime(L)
    xvars = _make_vars(L[2], use_real)
    xp = prime(xvars)
    preds = []
    for expr in xp:
        if z3.is_app_of(expr, z3.Z3_OP_ITE):
            pred = expr.arg(0)
            if not any(z3.eq(pred, old) for old in preds):
                preds.append(pred)
    return xvars, preds


def _eval_predicate(pred, values, xvars, use_real):
    subs = []
    for i, val in enumerate(values):
        if use_real:
            subs.append((xvars[i], z3.RealVal(float(val))))
        else:
            subs.append((xvars[i], z3.IntVal(int(val))))
    simplified = z3.simplify(z3.substitute(pred, subs))
    if z3.is_true(simplified):
        return True
    if z3.is_false(simplified):
        return False
    return False


def _region_index(values, predicates, xvars, use_real):
    idx = 0
    for pred in predicates:
        idx = (idx << 1) | (1 if _eval_predicate(pred, values, xvars, use_real) else 0)
    return idx


def _build_region_conditions(predicates, xvars, vars_):
    regions = []
    subs = [(xvars[i], vars_[i]) for i in range(len(xvars))]
    for ridx in range(2 ** len(predicates)):
        bits = []
        for i in range(len(predicates)):
            bits.append(bool((ridx >> (len(predicates) - 1 - i)) & 1))
        conds = []
        for bit, pred in zip(bits, predicates):
            pred_sub = pred if vars_ is xvars else z3.substitute(pred, subs)
            conds.append(pred_sub if bit else z3.Not(pred_sub))
        regions.append(z3.And(*conds))
    return regions


def _eval_linear_z3(basis, coeffs, vars_):
    total = z3.RealVal(0)
    for c, powers in zip(coeffs, basis):
        total = total + z3.RealVal(c) * _eval_monomial_z3(powers, vars_)
    return total


def _piecewise_expr(predicates, xvars, vars_, basis, coeffs):
    regions = _build_region_conditions(predicates, xvars, vars_)
    expr = _eval_linear_z3(basis, coeffs[-1], vars_)
    for ridx in range(len(coeffs) - 2, -1, -1):
        expr = z3.If(regions[ridx], _eval_linear_z3(basis, coeffs[ridx], vars_), expr)
    return expr


def _solve_piecewise_coeffs(samples, basis, predicates, xvars, use_real, print_level, coef_bound=10):
    if not samples:
        return None
    region_count = 2 ** len(predicates)
    coeffs = []
    solver = z3.Solver()
    region_used = set()
    for xval, xpval in samples:
        region_used.add(_region_index(xval, predicates, xvars, use_real))
        region_used.add(_region_index(xpval, predicates, xvars, use_real))
    for r in range(region_count):
        row = [z3.Real(f"c_{r}_{j}") for j in range(len(basis))]
        coeffs.append(row)
        if r in region_used:
            solver.add(z3.Or([c != 0 for c in row]))
        for c in row:
            solver.add(c >= -coef_bound, c <= coef_bound)
    for xval, xpval in samples:
        rx = _region_index(xval, predicates, xvars, use_real)
        rxp = _region_index(xpval, predicates, xvars, use_real)
        fx = sum(c * _eval_monomial(p, xval) for c, p in zip(coeffs[rx], basis))
        fxp = sum(c * _eval_monomial(p, xpval) for c, p in zip(coeffs[rxp], basis))
        solver.add(fx >= 0)
        solver.add(fxp < fx)
    if solver.check() != z3.sat:
        if print_level > 1:
            print("piecewise: no coefficients for current samples")
        return None
    model = solver.model()
    result = []
    for row in coeffs:
        result.append([_z3_to_float(model.eval(c)) for c in row])
    return result


def _verify_piecewise(L, basis, coeffs, predicates, xvars, print_level):
    cond, prime, use_real = _guard_and_prime(L)
    x = xvars
    xp = prime(x)
    fx = _piecewise_expr(predicates, xvars, x, basis, coeffs)
    fxp = _piecewise_expr(predicates, xvars, xp, basis, coeffs)
    bad = z3.Or(fx < 0, z3.Not(fxp < fx))
    s = z3.Solver()
    s.add(cond(x))
    s.add(bad)
    if s.check() == z3.sat:
        model = s.model()
        ce = [model.eval(v, model_completion=True) for v in x]
        ce = [_z3_to_float(v) for v in ce]
        if print_level > 1:
            print("piecewise counterexample:", ce)
        return False, ce
    return True, None


def _format_coeff(value):
    if abs(value) < 1e-9:
        return "0"
    text = f"{value:.6g}"
    if text == "-0":
        text = "0"
    return text


def _format_monomial(powers):
    parts = []
    for idx, power in enumerate(powers):
        if power == 0:
            continue
        if power == 1:
            parts.append(f"x{idx}")
        else:
            parts.append(f"x{idx}^{int(power)}")
    if not parts:
        return "1"
    return " * ".join(parts)


def format_piecewise_rf(coeffs, basis, predicate_texts):
    lines = []
    if not predicate_texts:
        predicate_texts = []
    region_count = len(coeffs)
    for ridx in range(region_count):
        bits = []
        for i in range(len(predicate_texts)):
            bits.append(bool((ridx >> (len(predicate_texts) - 1 - i)) & 1))
        if predicate_texts:
            conds = []
            for bit, pred in zip(bits, predicate_texts):
                conds.append(pred if bit else f"not ({pred})")
            cond_text = " and ".join(conds)
        else:
            cond_text = "true"
        terms = []
        for c, powers in zip(coeffs[ridx], basis):
            if abs(c) < 1e-9:
                continue
            mono = _format_monomial(powers)
            coef = abs(c)
            coef_text = _format_coeff(coef)
            if mono == "1":
                term = coef_text
            elif abs(coef - 1.0) < 1e-9:
                term = mono
            else:
                term = f"{coef_text} * {mono}"
            sign = "-" if c < 0 else "+"
            terms.append((sign, term))
        if not terms:
            expr = "0"
        else:
            sign, term = terms[0]
            expr = f"- {term}" if sign == "-" else term
            for sign, term in terms[1:]:
                expr += f" {sign} {term}"
        lines.append(f"Region {ridx}: {cond_text}")
        lines.append(f"  f(x) = {expr}")
    return "\n".join(lines)


def LearnPiecewiseRankerExt(L, template_strategy, sample_strategy, print_level, predicate_texts=None, max_iters=60):
    use_real = is_type_real(L)
    predicates = []
    xvars = None
    predicate_labels = None
    if predicate_texts:
        xvars, predicates = _parse_predicates(predicate_texts, L[2], use_real)
        predicate_labels = list(predicate_texts)
    else:
        xvars, predicates = _extract_ite_predicates(L, use_real)
        predicate_labels = [str(p) for p in predicates]
    if not predicates:
        if print_level > 0:
            print("piecewise: no predicates available")
        return 'UNKNOWN', [], [], []
    templates = generateTemplatesStrategyExt(template_strategy, L[2])
    if not templates:
        return 'UNKNOWN', [], [], []
    basis = _basis_from_template(templates[0], L[2])
    samples = _sample_transitions(L, sample_strategy, 20, print_level)
    if print_level > 1:
        print("piecewise predicates:", [str(p) for p in predicates])
        print("piecewise regions:", 2 ** len(predicates))
    for _ in range(max_iters):
        coeffs = _solve_piecewise_coeffs(samples, basis, predicates, xvars, use_real, print_level)
        if coeffs is None:
            break
        ok, ce = _verify_piecewise(L, basis, coeffs, predicates, xvars, print_level)
        if ok:
            return 'TERMINATE', coeffs, basis, predicate_labels
        if ce is None:
            return 'UNKNOWN', [], [], []
        ce_p = get_statement(L, ce)
        if ce_p is None or not _is_finite_list(ce_p):
            break
        samples.append((ce, ce_p))
    return 'UNKNOWN', [], [], []
