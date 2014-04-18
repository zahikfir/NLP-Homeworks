#********************** NLP **********************#
# H.W 3
# Haim Shalelashvily    200832780
# Zahi Kfir             200681476
#********************** NLP **********************#

import sys, os, time, codecs
from collections import Counter

StartTime = time.clock()

# Return the execution mod and the appropriate command arguments
def GetCommandLineArguments():
    try:
        # Get the command line argument
        if len(sys.argv) < 2: sys.exit("Please enter an execution mode: -e for evaluation or -c for classification")
        executionMode = sys.argv[1]

        # if execution mode is evaluation
        if (executionMode == '-e'):
            if len(sys.argv) < 4: sys.exit("To run classify.py in evaluation mode run the command: classify.py -e -training FolderWithInputFiles")
            InputFilesFolder = sys.argv[sys.argv.index("-training") + 1]
            TestsFilesFolder = None
        # else if we are in classify mode
        elif (executionMode == '-c'):
            if len(sys.argv) < 6: sys.exit("To run classify.py in classify mode, run the command: classify.py -c -training FolderWithInputFiles -test FolderWithTestFiles")
            InputFilesFolder = sys.argv[sys.argv.index("-training") + 1]
            TestsFilesFolder = sys.argv[sys.argv.index("-test") + 1]
        # wrong execution mode
        else: sys.exit("Please enter an execution mode: -e for evaluation or -c for classification")
    
    # if one of the option parameters is missing
    except: sys.exit("Wrong input. Please check your command line arguments")
    
    print('Start Program. Execution mode: {0}, InputFolder: {1}, TestFolder: {2}'.format(executionMode, InputFilesFolder, TestsFilesFolder))

    return executionMode,InputFilesFolder,TestsFilesFolder
    
# Temporarly Function - Create a feature vector from all the words in the corpus
def GetDictionary(inputFolderPath):
    
    dic = Counter()

    # Get all the txt file paths from the positive folder
    print("Creating dictionary (feature vector) from the positive reviews input folder")
    posFolder = os.path.join(inputFolderPath, "pos")
    txtFilesList = [ os.path.join(posFolder, f) for f in os.listdir(posFolder) if (os.path.isfile(os.path.join(posFolder, f)) & str(f).endswith(".txt"))]
    
    # update the dictionary with each review
    for txtFile in txtFilesList:
        dic.update(Counter(codecs.open(txtFile,"r","utf-8").read().split()))

    # Get all the txt file paths from the positive folder
    print("Updating the dictionary (feature vector) from the negative reviews input folder")
    posFolder = os.path.join(inputFolderPath, "neg")
    txtFilesList = [ os.path.join(posFolder, f) for f in os.listdir(posFolder) if (os.path.isfile(os.path.join(posFolder, f)) & str(f).endswith(".txt"))]
    
    # update the dictionary with each review
    for txtFile in txtFilesList:
        dic.update(Counter(codecs.open(txtFile,"r","utf-8").read().split()))

    # return the entire dictionary
    return dic

# parse the command line arguments
executionMode,InputFilesFolder,TestsFilesFolder = GetCommandLineArguments()

# create the feature vector - For now from all the words in the text
featureVector = GetDictionary(InputFilesFolder)

print("Total Time (sec):\t\t\t" ,time.clock() - StartTime)