#********************** NLP **********************#
# H.W 3
# Haim Shalelashvily    200832780
# Zahi Kfir             200681476
#********************** NLP **********************#

import sys, os, time, codecs
from collections import Counter

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
    return dic.keys()

# create a feature vector dictionary from array
def ArrayToZeroedDictionary(arr, dic = {}):
    for item in arr:
        dic[item] = 0
    return dic

# add the reviews within the specified path to the db with the given label using only the featured words
def AddVectorsToTrainingVectors(db, inputFolderPath, featuresArr, label):
    
    # Get all the txt file paths from the positive folder
    txtFilesList = [ os.path.join(inputFolderPath, f) for f in os.listdir(inputFolderPath) if (os.path.isfile(os.path.join(inputFolderPath, f)) & str(f).endswith(".txt"))]
    
    # update the dictionary with each review
    dic = {}
    for txtFile in txtFilesList:
        
        # initialize a feature vector for this file
        featuresDic = ArrayToZeroedDictionary(featuresArr, dic)

        # create a list of tokens
        tokens = codecs.open(txtFile,"r","utf-8").read().split()
        
        # for each token, if it in the feature list enable his flag
        for token in tokens:
            if token in featuresArr:
                featuresDic[token] = 1

        # add the tuple (featureVec , label) to the global db
        trainExample = (featuresDic.values(), label)
        db.append(trainExample)

    # return the updated db
    return db

# create the training vector DB
def CreateTrainingVectorDB(inputFolderPath, featuresArr):
    
    #initialize an empty DB
    db = []

    db = AddVectorsToTrainingVectors(db, os.path.join(inputFolderPath, "pos"), featuresArr,  1)
    db = AddVectorsToTrainingVectors(db, os.path.join(inputFolderPath, "neg"), featuresArr, -1)

    return db

#********************** NLP **********************#
# Main Program 

StartTime = time.clock()

# parse the command line arguments
executionMode,InputFilesFolder,TestsFilesFolder = GetCommandLineArguments()

# create the feature vector - For now from all the words in the text
featuresArr = GetDictionary(InputFilesFolder)

# create the train DB vectors
TrainingVectorDb = CreateTrainingVectorDB(InputFilesFolder, featuresArr)

print("Total Time (sec):\t\t\t" ,time.clock() - StartTime)