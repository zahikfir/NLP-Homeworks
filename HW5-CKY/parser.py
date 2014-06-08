#********************** NLP **********************#
# H.W 5
# Haim Shalelashvily    200832780
# Zahi Kfir             200681476
#********************** NLP **********************#

import sys, os, time, codecs, math,re
from collections import Counter

# Return the execution mode and the appropriate command arguments
def GetCommandLineArguments():
    try:
        if len(sys.argv) < 4: 
            sys.exit()

        grammarFilePath = sys.argv[sys.argv.index("--grammar") + 1]
        testFilePath = sys.argv[sys.argv.index("--test") + 1]
        outputFilePath = sys.argv[sys.argv.index("--output") + 1]

    except:  # if one of the option parameters is missing
        sys.exit("\nWrong input. Please check your command line arguments \n--grammar GRAMER/FILE/PATH --test TEST/FILE/PATH --output  OUTPUT/FILE/PATH\n")

    
    print('Program parameters description: \n\t Grammar file path: {0} \n\t Test file path: {1} \n\t Output file path: {2}\n'.format(grammarFilePath, testFilePath, outputFilePath))

    return grammarFilePath,testFilePath,outputFilePath


# Read data from file 
# returns fileData: list of rows, each row is a list of tokens
# fileData[0][1] = 'dog'  -> the second token of the first row is dog
def ReadFile(filePath):
    
    fileData = []
    file = codecs.open(filePath,"r","utf-8")   # Open the file
    rows = file.read().split('\n')             # split the data into rows list           
    for row in rows:                           
        fileData.append(row.split())           # split the row into tokens list

    return fileData


# Read the grammar file
# return grammar = a dictionary where the keys are the rules body and the value is a list of pairs
#                  each pair is the rule head and the probability
#   e.g.  for the 2 ruls:   0.1 N -> stops
#                           0.2 V -> stops
#                           grammar['stops'] = [('N', '0.1'), ('V', '0.2')]
def ReadGrammarFile(grammarFilePath):
    grammar = dict()
    
    # read list of rules
    grammarData = ReadFile(grammarFilePath)
    nonTerminalsList = []
    
    # for each rule
    for rule in grammarData:
        
        if len(rule) == 4:              # terminal
            key = rule[3]               # key is the rule body!            
        elif len(rule) == 5:            # 2 non-terminal
            key = rule[3]+" "+rule[4]   # key is the rule body!    
        
        if key in grammar:
            grammar[key].append( (rule[1],rule[0]) )    # append (rule-head, rule-probability) 
        else:
            grammar[key] = [(rule[1],rule[0])]          # append (rule-head, rule-probability)
        
        if (rule[1] not in nonTerminalsList):
            nonTerminalsList.append(rule[1])

    return grammar, nonTerminalsList

# Creates a three dimensional matrix of size: sentenceLen X sentenceLen X nonTerminalsLen
def CreateCkyMatrix(sentenceLen, nonTerminalsLen):

    ckyMatrix = []
    for i in range(0,sentenceLen):
        ckyMatrix.append([])
        for j in range(0,sentenceLen):
            ckyMatrix[i].append([])
            for k in range(0, nonTerminalsLen):
                ckyMatrix[i][j].append(0)

    return ckyMatrix

# TODO
def FillCkyMatrix(sentence, grammar, nonTerminalList):
    
    ckyMatrix = CreateCkyMatrix(len(sentence), len(nonTerminalList))
    ckyTraceBackMatrix = CreateCkyMatrix(len(sentence), len(nonTerminalList))
    
    for j in range(0, len(sentence)):
        
        for rule in grammar[sentence[j]]:
            nonTerminalIdx = nonTerminalList.index(rule[0])
            ckyMatrix[j][j][nonTerminalIdx] = float(grammar[sentence[j]][0][1])
            ckyTraceBackMatrix[j][j][nonTerminalIdx] = sentence[j]

        for i in range(j-1,-1,-1):
            for k in range(i, j):
                for nonTerminalIdxB in range(len(nonTerminalList)):
                    if (ckyMatrix[i][k][nonTerminalIdxB] > 0):
                        for nonTerminalIdxC in range(len(nonTerminalList)):
                            if (ckyMatrix[k+1][j][nonTerminalIdxC] > 0):
                                # create the B C string
                                currentNonTerminals = nonTerminalList[nonTerminalIdxB]+" "+nonTerminalList[nonTerminalIdxC]
                                if currentNonTerminals in grammar:
                                    for rule in grammar[currentNonTerminals]:
                                        p = float(rule[1]) * ckyMatrix[i][k][nonTerminalIdxB] * ckyMatrix[k+1][j][nonTerminalIdxC]
                                        # Todo - check for disambiguity
                                        if (ckyMatrix[i][j][nonTerminalList.index(rule[0])] < p):
                                            ckyMatrix[i][j][nonTerminalList.index(rule[0])] = p
                                            ckyTraceBackMatrix[i][j][nonTerminalList.index(rule[0])] = str.format("{0} {1} {2} X {3} {4} {5}",i,k,nonTerminalList[nonTerminalIdxB],k+1,j,nonTerminalList[nonTerminalIdxC])

    return ckyMatrix, ckyTraceBackMatrix

def CreateDerviationTree(ckyTraceBackMatrix, nonTerminalList, i ,j ,k):
    
    derivationTree = ""

    derivationTree += "["
    derivationTree += nonTerminalList[k] + " "
    trace = (str)(ckyTraceBackMatrix[i][j][k]).split()
    if (len(trace) > 1):
        derivationTree += CreateDerviationTree(ckyTraceBackMatrix, nonTerminalList, int(trace[0]), int(trace[1]), nonTerminalList.index(trace[2]))
        derivationTree += CreateDerviationTree(ckyTraceBackMatrix, nonTerminalList, int(trace[4]), int(trace[5]), nonTerminalList.index(trace[6]))
    else: derivationTree += trace[0]
    derivationTree += "]"
    return derivationTree


# TODO
def BuildDerivationTree(ckyMatrix, ckyTraceBackMatrix, nonTerminalList):

    i = 0
    j = len(ckyTraceBackMatrix[0]) - 1
    k = nonTerminalList.index("S")

    derivationTree = CreateDerviationTree(ckyTraceBackMatrix, nonTerminalList, i, j, k)

    return derivationTree

# write the derivation tree into file 
def WriteTreeIntoFile(sentence,derivationTree,file):
    
    # write the sentence
    for token in sentence:
        file.write(token+" ")
    file.write(os.linesep)
    
    # write the derivation tree 
    file.write(derivationTree)
    file.write(os.linesep)
    file.write(os.linesep)
    
    return True




print("\n---------------------- HW5 - CKY algorithm ----------------------\n")
TotalStartTime = time.clock()

# get Command Line Arguments 
grammarFilePath,testFilePath,outputFilePath = GetCommandLineArguments()

# read the grammar file
grammar, nonTerminalList = ReadGrammarFile(grammarFilePath)

# read the test file 
testData = ReadFile(testFilePath)

# open the output file
outFile = codecs.open(outputFilePath, "w", "utf-8")

# build derivation tree for each sentence using CKY algorithm
for sentence in testData:
    if len(sentence) > 0:
        ckyMatrix, ckyTraceBackMatrix = FillCkyMatrix(sentence, grammar, nonTerminalList)
        derivationTree = BuildDerivationTree(ckyMatrix, ckyTraceBackMatrix, nonTerminalList)
        WriteTreeIntoFile(sentence,derivationTree,outFile)

print("\nAll procedures have been completed in ",time.clock() - TotalStartTime," sec")
print("\tresults are in: "+outputFilePath+" file \n")
print("---------------------- HW5 - CKY algorithm ----------------------\n")





