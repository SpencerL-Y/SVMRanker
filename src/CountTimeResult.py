import os
import numpy as np
import random
import datetime
from sklearn.svm import LinearSVC
from z3 import *
import signal
import time
import re

train_expression = re.compile(r"train_ranking_functioning time = ")

dirName = sys.argv[1]

fileList = os.listdir(dirName)
for name in fileList:
    if name.endswith(".bpl.log"):
        with open(dirName + name, "r", encoding="utf-8") as f:
            changed = False
            print(dirName + name)
            for line in f:
                match = train_expression.search(line)
                #print(match.group(0))