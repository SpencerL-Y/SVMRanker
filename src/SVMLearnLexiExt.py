import os
import datetime
from LexiRankerExt import LearnLexiRankerExt

def SVMLearnLexiExt(sourceFilePath, sourceFileName,
                    depth_bound,
                    parse_oldtime, parse_newtime,
                    sample_strategy, template_strategy,
                    print_level):
    from OneLoop import L
    rank_oldtime = datetime.datetime.now()
    result, coeffs = LearnLexiRankerExt(L, depth_bound, template_strategy, sample_strategy, print_level)
    rank_newtime = datetime.datetime.now()
    if print_level > 0:
        print("--------------------LEARNING LEXICOGRAPHIC SUMMARY-------------------")
        print("LEARNING RESULT: ", result)
        print('Time For %s Is ---> %f ms\n' % (os.path.join(sourceFilePath, sourceFileName), float((parse_newtime - parse_oldtime).total_seconds()) * 1000 + float((rank_newtime - rank_oldtime).total_seconds()) * 1000))
        print('Program is terminating' if result == 'TERMINATE' else ("Information about terminating is unknown" if result == 'UNKNOWN' else 'Program is non-terminating'))
    return result, coeffs
