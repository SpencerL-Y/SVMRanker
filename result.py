import os

def Get_LassoRankerResult(filename):
	f = open(filename,'r')
	NP = False
	IsTerminated = None
	for line in f:
		if (line.find('RESULT: Ultimate proved your program to be correct!')) != -1:
			IsTerminated = True
		if (line.find('Nontermination argument in form of an infinite execution')) != -1:
			IsTerminated = False
		if (line.find('RESULT: Ultimate could not prove your program: Toolchain returned no result')) != -1:
			NP = True
		po = line.find('Toolchain (without parser) took')
		if po != -1:
			line = line[po:].strip()
			Time = float(line.split(' ')[4])
		
	if  IsTerminated is None  and NP :
		return Time, 'UNKNOWN'
	elif IsTerminated and  not NP:
		return Time, 'Y'
	elif not IsTerminated and NP:
		return Time , 'N'
	else :
		raise Exception(filename+'---> problem')

def GetSVMTime(filename):
	f = open(filename,'r')
	time = {}
	for line in f:
		if line.strip() == '':
			continue
		line = line.strip().split(' ')
		t = line[-2]
		num = line[2].strip().split('/')[-1]
		num = num.strip().split('.')[0]
		time[int(num)] = float(t)
	return time
def GetSVMResult(filename):
	f = open(filename,'r')
	NP = False
	IsTerminated = None
	for line in f:
		if line.find('------Using Template ')!=-1:
			IsTerminated = None
		if line.find('it is not terminated, an infinate loop with initial condition:') != -1:
			IsTerminated = 'N'
		elif line.find('Found Ranking Fcuntion') == 0:
			IsTerminated = 'Y'
		elif line.find('Failed to prove it is terminated') == 0:
			IsTerminated = 'UNKNOWN'
	return IsTerminated

lassoranker_dir =  r'LassoRanker/Log_File_2019-05-02-19-53-31'
SVM_dir = r'SVM_Loop/Log_File_2019-05-04-00-33-24'
result = open('result.log','w')
sy,sn,sun = 0,0,0
ly,ln,lun = 0,0,0
SVM_Time = GetSVMTime(os.path.join(SVM_dir,'AnalysisTimeForALL.log'))
SVM_Result = {}

Lasso_Time = {}
Lasso_Result = {}
for i in range(200):
	lasso_file = os.path.join(lassoranker_dir,str(i)+'.bpl.log')
	if os.path.isfile(lasso_file):
		time,result = Get_LassoRankerResult(lasso_file)
		Lasso_Time[i] = time
		Lasso_Result[i] = result
		if result == 'Y':
			sy +=1
		elif result == 'N':
			sn+=1
		elif result == 'UNKNOWN':
			sun +=1

	svm_file = os.path.join(SVM_dir,str(i)+'.bpl.log')
	if os.path.isfile(svm_file):
		result = GetSVMResult(svm_file)
		if result is None:
			SVM_Result[i] = 'TO'
			lun +=1
		elif result == 'UNKNOWN':
			SVM_Result[i] = 'UNKNOWN'
			lun += 1
		elif result == 'Y':
			SVM_Result[i] = 'Y'
			ly += 1
		else:
			SVM_Result[i] = 'N'
			ln += 1

##############Result.file###################
result = open('scatter.log','w')
for i in range(150):
	if i in Lasso_Time and i in SVM_Time:
		result.write('('+str(Lasso_Time[i])+', '+str(SVM_Time[i])+')\n')
result.close()
result = open('result.csv','w')
for i in Lasso_Time:
		result.write(str(i) + ', '+ str(Lasso_Time[i])+', '+(str(SVM_Time[i]) if SVM_Result[i]!='TO' else '300000') + ', '+ Lasso_Result[i] + ',' +SVM_Result[i]+'\n')
result.close()
print(Lasso_Time)
print(Lasso_Result)
print(SVM_Time)
print(SVM_Result)
print(sy,sn,sun)
print(ly,ln,lun)


