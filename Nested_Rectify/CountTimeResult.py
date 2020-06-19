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
i = 0
for name in fileList:
    if name.endswith(".bpl.log"):
       os.rename("name", str(i)+".bpl.log")
       i = i + 1
