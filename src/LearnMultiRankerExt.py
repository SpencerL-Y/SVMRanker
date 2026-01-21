'''
Extended multiphase learning with richer templates.
'''
from Util import *
from FindMultiphaseUtilExt import changeTemplate, generateTemplatesStrategyExt
from LearnRanker import *

def _template_dimension(L_test):
    template = L_test[4]
    return len(template)

def LearnRankerNoBoundLoopBodyExt(L_test, sample_strategy, print_level, x, y):
    ret = 'UNKNOWN'
    listOfUxDimension = []
    dim = _template_dimension(L_test)
    for _ in range(L_test[3]):
        listOfUxDimension.append(dim)
    if print_level > 1:
        print("listOfDimension", listOfUxDimension)
    listOfUx, last_coef_array = parse_template_handcraft(L_test[4], L_test[2], listOfUxDimension)
    rf = NestedNoBoundTemplate(
        listOfUx,
        [0.001] * len(listOfUx),
        last_coef_array
    )
    ret, new_x, new_y = train_ranking_function_strategic(L_test, rf, sample_strategy, print_level, x, y)
    if ret == 'TERMINATE':
        no_bound_return = 'CORRECT'
    elif ret == 'NONTERM':
        no_bound_return = 'NONTERM'
    else:
        no_bound_return = 'FALSE'
    return no_bound_return, rf

def LearnRankerBoundedLoopBodyExt(L_test, sample_strategy, print_level, x, y):
    ret = 'UNKNOWN'
    listOfUxDimension = []
    dim = _template_dimension(L_test)
    for _ in range(L_test[3]):
        listOfUxDimension.append(dim)
    if print_level > 1:
        print("listOfDimension", listOfUxDimension)
    listOfUx, last_coef_array = parse_template_handcraft(L_test[4], L_test[2], listOfUxDimension)
    rf = NestedTemplate(
        listOfUx,
        [0.001] * len(listOfUx),
        0,
        last_coef_array
    )
    ret, new_x, new_y = train_ranking_function_strategic(L_test, rf, sample_strategy, print_level, x, y)
    return ret, rf

def train_multi_ranking_function_backtracking_loopbody_ext(L, x, y, rf_list, templates, templateNum, currentDepth, depthBound, sample_strategy, cutting_strategy, print_level):
    if print_level > 0:
        print("-------------------START BACKTRACK LEARNING--------------------")
    result = 'UNKNOWN'
    if currentDepth < depthBound:
        for num in range(len(templates)):
            if print_level > 0:
                print('--------------------- Depth: ', currentDepth, "templateNum:", num, " Learn bounded ---------------------" )
            changeTemplate(L, templates[num])
            result, rf = LearnRankerBoundedLoopBodyExt(L, sample_strategy, print_level, (), ())
            if print_level > 0:
                print("-----RESULT:", result, "-------")
            if result != 'UNKNOWN':
                rf_list.append(rf)
                return result, rf_list

        while templateNum < len(templates):
            if print_level > 0:
                print('--------------------- Depth: ', currentDepth, "templateNum:", templateNum, " Learn unbound ---------------------" )
            changeTemplate(L, templates[templateNum])
            ret, rf = LearnRankerNoBoundLoopBodyExt(L, sample_strategy, print_level, (), ())
            if ret == 'CORRECT':
                L_new = ConjunctRankConstraintL(L, rf, print_level, cutting_strategy)
                rf_list.append(rf)
                result, rf_list = train_multi_ranking_function_backtracking_loopbody_ext(L_new, x, y, rf_list, templates, 0, currentDepth + 1, depthBound, sample_strategy, cutting_strategy, print_level)
                if print_level > 0:
                    print("-----RESULT:", result, "-------")
                if result == 'UNKNOWN':
                    rf_list.pop()
                    templateNum += 1
                else:
                    return result, rf_list
            elif ret == 'NONTERM':
                rf_list.append(rf)
                rf_list = []
                return 'NONTERM', rf_list
            elif ret == 'FALSE':
                templateNum += 1
        return 'UNKNOWN', rf_list
    elif currentDepth == depthBound:
        while templateNum < len(templates) and result == 'UNKNOWN':
            if print_level > 0:
                print('--------------------- Depth: ', currentDepth, "templateNum:", templateNum, " Learn bounded ---------------------" )
            changeTemplate(L, templates[templateNum])
            result, rf = LearnRankerBoundedLoopBodyExt(L, sample_strategy, print_level, (), ())
            if print_level > 0:
                print("-----RESULT:", result, "-------")
            if result != 'UNKNOWN':
                rf_list.append(rf)
                return result, rf_list
            templateNum += 1
        return 'UNKNOWN', rf_list
    else:
        return 'UNKNOWN', rf_list

def train_multi_ranking_function_backtracking_ext(L, x, y, templates, depthBound, sample_strategy, cutting_strategy, print_level):
    i = 1
    result = 'UNKNOWN'
    while i <= depthBound and result == 'UNKNOWN':
        rf_list = []
        ret, rf_list = train_multi_ranking_function_backtracking_loopbody_ext(L, x, y, rf_list, templates, 0, 1, i, sample_strategy, cutting_strategy, print_level)
        i += 1
    return ret, rf_list

def LearnMultiRankerExt(L, db, sample_strategy, cuttingStrategy, template_strategy, print_level, nestedPhase, x, y):
    L_loop = L
    L_loop[3] = nestedPhase
    templatesLib = generateTemplatesStrategyExt(template_strategy, L[2])
    if not templatesLib:
        return 'UNKNOWN', []
    L_loop.insert(4, templatesLib[0])
    result, rf_list = train_multi_ranking_function_backtracking_ext(L, x, y, templatesLib, db, sample_strategy, cuttingStrategy, print_level)
    return result, rf_list
