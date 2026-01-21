import os
import datetime
from LearnMultiRankerExt import LearnMultiRankerExt
from FindMultiphaseUtil import printSummary

def SVMLearnMultiExt(sourceFilePath, sourceFileName,
                     depth_bound,
                     parse_oldtime, parse_newtime,
                     sample_strategy, cutting_strategy, template_strategy,
                     print_level):
    from OneLoop import L
    rank_oldtime = datetime.datetime.now()
    result, rf_list = LearnMultiRankerExt(L, depth_bound, sample_strategy, cutting_strategy, template_strategy, print_level, 1, (), ())
    rank_newtime = datetime.datetime.now()
    if print_level > 0:
        if result == "TERMINATE":
            printSummary(len(rf_list), result, rf_list, True)
        else:
            print("--------------------LEARNING MULTIPHASE SUMMARY-------------------")
            print("LEARNING RESULT: ", result)
        print('Time For %s Is ---> %f ms\n' % (os.path.join(sourceFilePath, sourceFileName), float((parse_newtime - parse_oldtime).total_seconds()) * 1000 + float((rank_newtime - rank_oldtime).total_seconds()) * 1000))
        print('Program is terminating' if result == 'TERMINATE' else ("Information about terminating is unknown" if result == 'UNKNOWN' else 'Program is non-terminating'))
    return result, rf_list
