'''
Extended template strategies for multiphase learning.
'''
def _monomial_vector(num_of_vars, powers):
    return list(powers) + [1]

def _linear_monomials(num_of_vars):
    monomials = []
    for i in range(num_of_vars):
        powers = [0] * num_of_vars
        powers[i] = 1
        monomials.append(powers)
    monomials.append([0] * num_of_vars)
    return [_monomial_vector(num_of_vars, p) for p in monomials]

def _quadratic_monomials(num_of_vars, include_cross=True, include_square=True):
    monomials = []
    for i in range(num_of_vars):
        powers = [0] * num_of_vars
        powers[i] = 1
        monomials.append(powers)
    if include_square:
        for i in range(num_of_vars):
            powers = [0] * num_of_vars
            powers[i] = 2
            monomials.append(powers)
    if include_cross:
        for i in range(num_of_vars):
            for j in range(i + 1, num_of_vars):
                powers = [0] * num_of_vars
                powers[i] = 1
                powers[j] = 1
                monomials.append(powers)
    monomials.append([0] * num_of_vars)
    return [_monomial_vector(num_of_vars, p) for p in monomials]

def generateTemplatesStrategyExt(strategy, num_of_vars):
    if strategy == "LINEAR":
        return [_linear_monomials(num_of_vars)]
    if strategy == "QUAD":
        return [_quadratic_monomials(num_of_vars, include_cross=True, include_square=True)]
    if strategy == "PAIRWISE":
        return [_quadratic_monomials(num_of_vars, include_cross=True, include_square=False)]
    return []

def changeTemplate(L, template):
    L[4] = template
