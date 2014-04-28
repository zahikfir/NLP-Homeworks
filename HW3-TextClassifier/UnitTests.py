
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
    
    TotalStartTime = time.clock()

    StartTime = time.clock()
    # Count positive tokens 
    PosDic = Counter()
    PosFileSpred = Counter()
    PosCount = 0;
    PosinputFolderPath = os.path.join(inputFolderPath, "pos")
    PosTxtFilesList = [ os.path.join(PosinputFolderPath, f) for f in os.listdir(PosinputFolderPath) if (os.path.isfile(os.path.join(PosinputFolderPath, f)) & str(f).endswith(".txt"))]
    for txtFile in PosTxtFilesList:
        PosCount = PosCount + 1;
        SpredCounted = []
        file = codecs.open(txtFile, "r", "utf-8")
        TokenList = file.read().split()
        for Token in TokenList:
            PosDic.update([Token])
            if not(Token in SpredCounted):
                SpredCounted.append(Token)
                PosFileSpred.update([Token])
        file.close()
    print("Count positive tokens (sec):\t\t\t" ,time.clock() - StartTime)
    
    StartTime = time.clock()
    # Count Negative tokens 
    NegDic = Counter()
    NegFileSpred = Counter()
    NegCount = 0
    NegInputFolderPath = os.path.join(inputFolderPath, "neg")
    NegTxtFilesList = [ os.path.join(NegInputFolderPath, f) for f in os.listdir(NegInputFolderPath) if (os.path.isfile(os.path.join(NegInputFolderPath, f)) & str(f).endswith(".txt"))]
    for txtFile in NegTxtFilesList:
        NegCount = NegCount + 1
        SpredCounted = []
        file = codecs.open(txtFile, "r", "utf-8")
        TokenList = file.read().split()
        for Token in TokenList:
            NegDic.update([Token])
            if not(Token in SpredCounted):
                SpredCounted.append(Token)
                NegFileSpred.update([Token])
        file.close()
    print("Count Negative tokens (sec):\t\t\t" ,time.clock() - StartTime)

    StartTime = time.clock()
    # Calc differences 
    OnlyPos = []
    OnlyNeg = []
    InBoth = []
    for (PosKey,PosVal) in PosDic.items():
        NegVal = NegDic[PosKey]
        if NegVal == 0:
            OnlyPos.append( (PosKey,PosVal,PosFileSpred[PosKey]))
        else:
            InBoth.append( (PosKey,abs(PosVal-NegVal),PosVal,PosFileSpred[PosKey],NegVal,NegFileSpred[PosKey]) )
            NegDic.pop(PosKey)            
    for (NegKey,NegVal) in NegDic.items():
        OnlyNeg.append( (NegKey,NegVal,NegFileSpred[NegKey]) )
    print("Calc differences (sec):\t\t\t" ,time.clock() - StartTime)
    
    StartTime = time.clock()
    # Write the results into the files
    OnlyPos.sort(key=operator.itemgetter(0))                  # Alphabetically sort
    OnlyPos.sort(key=operator.itemgetter(1),reverse= True)    # Sort by count
    OnlyPosFile = codecs.open(os.path.join(inputFolderPath, "OnlyPosFile.txt"), "w", "utf-8")
    OnlyPosFile.writelines(("\t\t\t Total Positive reviews %d " + os.linesep) % (PosCount))
    OnlyPosFile.writelines((("%15d\t %30s\t %d\t spred-%d\t " + os.linesep) % (idx + 1, val[0], val[1],val[2] ) for idx, val in enumerate(OnlyPos)))
    OnlyPosFile.close()

    OnlyPos.sort(key=operator.itemgetter(0))                  # Alphabetically sort
    OnlyPos.sort(key=operator.itemgetter(2),reverse= True)    # Sort by count
    OnlyPosFile = codecs.open(os.path.join(inputFolderPath, "OnlyPosFile_SortBySpred.txt"), "w", "utf-8")
    OnlyPosFile.writelines(("\t\t\t Total Positive reviews %d " + os.linesep) % (PosCount))
    OnlyPosFile.writelines((("%15d\t %30s\t %d\t spred-%d\t " + os.linesep) % (idx + 1, val[0], val[1],val[2] ) for idx, val in enumerate(OnlyPos)))
    OnlyPosFile.close()

    OnlyNeg.sort(key=operator.itemgetter(0))                  # Alphabetically sort
    OnlyNeg.sort(key=operator.itemgetter(1),reverse= True)    # Sort by count
    OnlyNegFile = codecs.open(os.path.join(inputFolderPath, "OnlyNegFile.txt"), "w", "utf-8")
    OnlyNegFile.writelines(("\t\t\t Total negative reviews %d " + os.linesep) % (NegCount))
    OnlyNegFile.writelines((("%15d\t %30s\t %d\t spred-%d\t " + os.linesep) % (idx + 1, val[0], val[1],val[2] ) for idx, val in enumerate(OnlyNeg)))
    OnlyNegFile.close()

    OnlyNeg.sort(key=operator.itemgetter(0))                  # Alphabetically sort
    OnlyNeg.sort(key=operator.itemgetter(2),reverse= True)    # Sort by count
    OnlyNegFile = codecs.open(os.path.join(inputFolderPath, "OnlyNegFile_SortBySpred.txt"), "w", "utf-8")
    OnlyNegFile.writelines(("\t\t\t Total negative reviews %d " + os.linesep) % (NegCount))
    OnlyNegFile.writelines((("%15d\t %30s\t %d\t spred-%d\t " + os.linesep) % (idx + 1, val[0], val[1],val[2] ) for idx, val in enumerate(OnlyNeg)))
    OnlyNegFile.close()

    InBoth.sort(key=operator.itemgetter(0))                  # Alphabetically sort
    InBoth.sort(key=operator.itemgetter(1),reverse= True)    # Sort by count
    InBothFile = codecs.open(os.path.join(inputFolderPath, "InBothFile.txt"), "w", "utf-8")
    InBothFile.writelines(("\t\t\t Total Positive reviews %d " + os.linesep) % (PosCount))
    InBothFile.writelines(("\t\t\t Total negative reviews %d " + os.linesep) % (NegCount))
    InBothFile.writelines((("%15d\t %30s\t diff:%d\t pos:%d\t pospred:%d\t neg:%d\t negpred:%d\t" + os.linesep) % (idx+1,val[0],val[1],val[2],val[3],val[4],val[5]) for idx, val in enumerate(InBoth)))
    InBothFile.close()
    print("Write the files (sec):\t\t\t" ,time.clock() - StartTime)

    StartTime = time.clock()
    # Create Feture Dic
    FeturesDic = Counter()
    Iter = 0;
    
    for Token,Appearances,Spred in OnlyPos:
        if Spred >= 2:
            FeturesDic[Token] = Iter;
            Iter = Iter + 1
    for Token,Appearances,Spred in OnlyNeg:
        if Spred >= 2:
            FeturesDic[Token] = Iter;
            Iter = Iter + 1
    inBothList = []
    for Item in enumerate(InBoth):
        differenceRatio = max( (Item[1][4]/Item[1][2]) , (Item[1][2]/Item[1][4]) )
        inBothList.append( (Item[1][0],differenceRatio) )
    inBothList.sort(key=operator.itemgetter(0))
    inBothList.sort(key=operator.itemgetter(1),reverse= True)
    for item in inBothList:
        if item[1] > 1:
            FeturesDic[item[0]] = Iter;
            Iter = Iter + 1

    print("Create Feture Dic (sec):\t\t\t" ,time.clock() - StartTime)

    # Set the global representation vector length  
    # TODO !!!
   
    print("TokenDiff() Done in (sec):\t\t\t" ,time.clock() - TotalStartTime)
    return FeturesDic