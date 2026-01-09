
import sys
import os
import datetime
import random

def fillOneLoop():
    os.system(" echo \"from z3 import *\" > OneLoop.py")
    os.system(" echo \"L,T = [], []\" >> OneLoop.py")
 

def getLoopInfo():
	infoFullPath = os.path.join(os.path.split(os.path.realpath(__file__))[0],'info.tmp')
	if not os.path.exists(infoFullPath):
		print('Please parsing Boogie first')
		raise Exception('Please parsing Boogie first')
	f = open(infoFullPath,'r')
	information = ''
	for line in f.readline():
		information+=line
	return information.strip().split()

def parseBoogieProgramMulti(sourceFile, outFile):
    path = os.path.split(os.path.realpath(__file__))[0]
    bpl_input = sourceFile if os.path.isabs(sourceFile) else os.path.abspath(sourceFile)
    jar = os.path.abspath(os.path.join(path, '..', 'Boogie2python', 'boogie2python.jar'))
    out_py = os.path.abspath(os.path.join(path, outFile))
    info_tmp = os.path.abspath(os.path.join(path, 'info.tmp'))

    (sourceFilePath, sourceFileName) = os.path.split(sourceFile)
    
    version = '.'.join(sys.version.strip().split(' ')[0].split('.')[0:2])
    parse_oldtime=datetime.datetime.now()
    generatePythonLoopCommand = [
    	'java', 
    	'-jar', 
    	jar, 
    	bpl_input, 
    	'0', 
    	out_py, 
    	info_tmp
    ]
    parse_oldtime=datetime.datetime.now()
    os.system(' '.join(generatePythonLoopCommand))
    # parsing_boogie(
    # 	os.path.abspath(os.path.join(path,'../Boogie2python/boogie2python.jar')),
    # 	os.path.join(path,sourceFilePath,sourceFileName), 
    # 	os.path.join(path,'OneLoop.py'), 
    # 	os.path.join(path,javaOutputInfo)
    # 	)
    Info = getLoopInfo()
    parse_newtime = datetime.datetime.now()
    templatePath = 'template'
    templateFileName = '.'.join([sourceFileName.strip(),'template'])
    return sourceFilePath, sourceFileName, templatePath, templateFileName, Info, parse_oldtime, parse_newtime

def parseBoogieProgramNested(sourceFile, outFile):
    path = os.path.split(os.path.realpath(__file__))[0]
    bpl_input = sourceFile if os.path.isabs(sourceFile) else os.path.abspath(sourceFile)
    jar = os.path.abspath(os.path.join(path, '..', 'Boogie2python', 'boogie2python.jar'))
    out_py = os.path.abspath(os.path.join(path, outFile))
    info_tmp = os.path.abspath(os.path.join(path, 'info.tmp'))

    (sourceFilePath, sourceFileName) = os.path.split(sourceFile)
    
    version = '.'.join(sys.version.strip().split(' ')[0].split('.')[0:2])
    parse_oldtime=datetime.datetime.now()
    generatePythonLoopCommand = [
    	'java', 
    	'-jar', 
    	jar, 
    	bpl_input, 
    	'0', 
    	out_py, 
    	info_tmp
    ]
    os.system(' '.join(generatePythonLoopCommand))
    # parsing_boogie(
    # 	os.path.abspath(os.path.join(path,'../Boogie2python/boogie2python.jar')),
    # 	os.path.join(path,sourceFilePath,sourceFileName), 
    # 	os.path.join(path,'OneLoop.py'), 
    # 	os.path.join(path,javaOutputInfo)
    # 	)
    Info = getLoopInfo()
    parse_newtime = datetime.datetime.now()
    templatePath = 'template'
    templateFileName = '.'.join([sourceFileName.strip(),'template'])
    return sourceFilePath, sourceFileName, templatePath, templateFileName, Info, parse_oldtime, parse_newtime