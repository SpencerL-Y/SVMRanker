import os
import datetime
from PiecewiseRankerExt import LearnPiecewiseRankerExt, format_piecewise_rf


def SVMLearnPiecewiseExt(sourceFilePath, sourceFileName,
                         parse_oldtime, parse_newtime,
                         sample_strategy, template_strategy,
                         print_level, predicates, max_iters,
                         print_rf=False, save_rf=None):
    from OneLoop import L
    rank_oldtime = datetime.datetime.now()
    result, coeffs, basis, predicate_labels = LearnPiecewiseRankerExt(
        L,
        template_strategy,
        sample_strategy,
        print_level,
        predicates,
        max_iters,
    )
    rank_newtime = datetime.datetime.now()
    rf_text = None
    if result == 'TERMINATE' and coeffs and basis:
        rf_text = format_piecewise_rf(coeffs, basis, predicate_labels)
    if print_rf and rf_text:
        print("--------------------PIECEWISE RANKING FUNCTION-------------------")
        print(rf_text)
    if save_rf and rf_text:
        os.makedirs(os.path.dirname(os.path.abspath(save_rf)), exist_ok=True)
        with open(save_rf, "w", encoding="utf-8") as f:
            f.write(rf_text + "\n")
    if print_level > 0:
        print("--------------------LEARNING PIECEWISE SUMMARY-------------------")
        print("LEARNING RESULT: ", result)
        print('Time For %s Is ---> %f ms\n' % (
            os.path.join(sourceFilePath, sourceFileName),
            float((parse_newtime - parse_oldtime).total_seconds()) * 1000 +
            float((rank_newtime - rank_oldtime).total_seconds()) * 1000))
        print('Program is terminating' if result == 'TERMINATE' else (
            "Information about terminating is unknown" if result == 'UNKNOWN'
            else 'Program is non-terminating'))
    return result, coeffs
