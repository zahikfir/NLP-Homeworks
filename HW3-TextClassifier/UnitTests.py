
import sys, os, codecs, re, time, math, operator
from collections import Counter


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