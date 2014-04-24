
import sys, os, codecs, re, time, math, operator
from collections import Counter



#import UnitTests
#if UnitTests.Test_CreateProbabilityTrainingDB():
#    print("Test_CreateProbabilityTrainingDB: Pass \n")
#else:
#    print("Test_CreateProbabilityTrainingDB: Failed \n")
#sys.stdin.read(1)
def Test_CreateProbabilityTrainingDB():
    import Classify
   
    # Set the global representation vector length  
    Classify.repVectorLen = 5;
     
    TestDB = []
    TestDB.append(([1,0,0,0,0],1))
    TestDB.append(([0,1,0,1,0],1))
    TestDB.append(([0,0,1,0,0],1))
    TestDB.append(([0,1,0,0,0],1))
    TestDB.append(([1,0,1,1,0],1))
    TestDB.append(([1,0,0,0,1],1))

    TestDB.append(([1,1,1,1,1],-1))
    TestDB.append(([0,0,0,0,0],-1))
    TestDB.append(([0,0,0,1,1],-1))
    TestDB.append(([0,0,0,0,1],-1))
    
    ProbabilityTrainingDb = Classify.CreateProbabilityTrainingDB(TestDB)

    if not(ProbabilityTrainingDb[1][0] == 6):
        return False
    if not(ProbabilityTrainingDb[-1][0] == 4):
        return False

    # Predicted outcomes
    PredOut_PositiveExists =    [(3+1)/(6+2),(2+1)/(6+2),(2+1)/(6+2),(2+1)/(6+2),(1+1)/(6+2)]    # count = [3,2,2,2,1]
    PredOut_PositiveNotExists = [(3+1)/(6+2),(4+1)/(6+2),(4+1)/(6+2),(4+1)/(6+2),(5+1)/(6+2)]    # count = [3,4,4,4,5]
    PredOut_NegativeExists =    [(1+1)/(4+2),(1+1)/(4+2),(1+1)/(4+2),(2+1)/(4+2),(3+1)/(4+2)]    # count = [1,1,1,2,3]
    PredOut_NegativeNotExists = [(3+1)/(4+2),(3+1)/(4+2),(3+1)/(4+2),(2+1)/(4+2),(1+1)/(4+2)]    # count = [3,3,3,2,1]
    
    for i in range(0,Classify.repVectorLen):   
        if not(ProbabilityTrainingDb[1][1][0][i] == PredOut_PositiveNotExists[i]):
            return False
        if not(ProbabilityTrainingDb[1][1][1][i] == PredOut_PositiveExists[i]):
            return False
        if not(ProbabilityTrainingDb[-1][1][0][i] == PredOut_NegativeNotExists[i]):
            return False
        if not(ProbabilityTrainingDb[-1][1][1][i] == PredOut_NegativeExists[i]):
            return False

    return True


def TokenDiff(inputFolderPath):
    
    # Count positive tokens 
    PosDic = Counter()
    PosinputFolderPath = os.path.join(inputFolderPath, "pos")
    txtFilesList = [ os.path.join(PosinputFolderPath, f) for f in os.listdir(PosinputFolderPath) if (os.path.isfile(os.path.join(PosinputFolderPath, f)) & str(f).endswith(".txt"))]
    for txtFile in txtFilesList:
        file = codecs.open(txtFile, "r", "utf-8")
        PosDic.update(Counter(file.read().split()))
        file.close()
        
    # Count Negative tokens
    NegDic = Counter()
    NeginputFolderPath = os.path.join(inputFolderPath, "neg")
    txtFilesList = [ os.path.join(NeginputFolderPath, f) for f in os.listdir(NeginputFolderPath) if (os.path.isfile(os.path.join(NeginputFolderPath, f)) & str(f).endswith(".txt"))]
    for txtFile in txtFilesList:
        file = codecs.open(txtFile, "r", "utf-8")
        NegDic.update(Counter(file.read().split()))
        file.close()

    # Calc differences 
    OnlyPos = []
    OnlyNeg = []
    InBoth = []
    for (PosKey,PosVal) in PosDic.items():
        NegVal = NegDic[PosKey]
        if NegVal == 0:
            OnlyPos.append( (PosKey,PosVal) )
        else:
            InBoth.append( (PosKey,abs(PosVal-NegVal),PosVal,NegVal) )
            NegDic.pop(PosKey)            
    for (NegKey,NegVal) in NegDic.items():
        OnlyNeg.append( (NegKey,NegVal) )

    
    # Write the results into the files
    OnlyPos.sort(key=operator.itemgetter(0))                  # Alphabetically sort
    OnlyPos.sort(key=operator.itemgetter(1),reverse= True)    # Sort by count
    OnlyPosFile = codecs.open(os.path.join(inputFolderPath, "OnlyPosFile.txt"), "w", "utf-8")
    OnlyPosFile.writelines((("%15d\t%30s\t%d " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(OnlyPos)))
    OnlyPosFile.close()

    OnlyNeg.sort(key=operator.itemgetter(0))                  # Alphabetically sort
    OnlyNeg.sort(key=operator.itemgetter(1),reverse= True)    # Sort by count
    OnlyNegFile = codecs.open(os.path.join(inputFolderPath, "OnlyNegFile.txt"), "w", "utf-8")
    OnlyNegFile.writelines((("%15d\t%30s\t%d " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(OnlyNeg)))
    OnlyNegFile.close()

    InBoth.sort(key=operator.itemgetter(0))                  # Alphabetically sort
    InBoth.sort(key=operator.itemgetter(1),reverse= True)    # Sort by count
    InBothFile = codecs.open(os.path.join(inputFolderPath, "InBothFile.txt"), "w", "utf-8")
    InBothFile.writelines((("%15d\t %30s\t diff:%d\t pos:%d\t neg:%d\t " + os.linesep) % (idx+1,val[0],val[1],val[2],val[3]) for idx, val in enumerate(InBoth)))
    InBothFile.close()

    print('Done!')