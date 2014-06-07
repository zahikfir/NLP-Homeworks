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
# returns fileData: list of sentences, each sentence is a list of tokens
# fileData[0][1] = 'dog'  -> the second token of the first sentence is dog
def ReadData(filePath):
    
    fileData = []
    testFile = codecs.open(filePath,"r","utf-8")     # Open the test file
    testSentences = testFile.read().lower().split('\n')  # split the data into sentences list           
    for sentence in testSentences:                           
        fileData.append(sentence.split())                # split the sentence into tokens list + append

    return fileData


print("\n---------------------- HW5 - CKY algorithm ----------------------\n")
TotalStartTime = time.clock()

# get Command Line Arguments 
grammarFilePath,testFilePath,outputFilePath = GetCommandLineArguments()

# parse the test file 
testData = ReadData(testFilePath)

#grammarData = ReadData(grammarFilePath)

print("\nAll procedures have been completed in ",time.clock() - TotalStartTime," sec")
print("\tresults are in: "+outputFilePath+" file \n")
print("---------------------- HW5 - CKY algorithm ----------------------\n")