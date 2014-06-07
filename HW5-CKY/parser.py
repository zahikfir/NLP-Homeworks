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
        
    return grammar

# TODO
def FillCkyMatrix(sentence,grammar):
    ckyMatrix = []

    return ckyMatrix

# TODO
def BuildDerivationTree(ckyMatrix):
    derivationTree = []

    return derivationTree

# TODO
def WriteTreeIntoFile(sentence,derivationTree,outputFilePath):

    return True




print("\n---------------------- HW5 - CKY algorithm ----------------------\n")
TotalStartTime = time.clock()

# get Command Line Arguments 
grammarFilePath,testFilePath,outputFilePath = GetCommandLineArguments()

# read the grammar file
grammar = ReadGrammarFile(grammarFilePath)

# read the test file 
testData = ReadFile(testFilePath)

# build derivation tree for each sentence using CKY algorithm
for sentence in testData:
    ckyMatrix = FillCkyMatrix(sentence,grammar)
    derivationTree = BuildDerivationTree(ckyMatrix)
    WriteTreeIntoFile(sentence,derivationTree,outputFilePath)

print("\nAll procedures have been completed in ",time.clock() - TotalStartTime," sec")
print("\tresults are in: "+outputFilePath+" file \n")
print("---------------------- HW5 - CKY algorithm ----------------------\n")




