#********************** NLP **********************#
# H.W 3
# Haim Shalelashvily    200832780
# Zahi Kfir             200681476
#********************** NLP **********************#

import sys, os, time, codecs, math
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

# create a representation vector to a review
def CreateRepresentationVector(reviewPath, featuresArr):
    
    # initialize a feature vector for this file
    featuresDic = ArrayToZeroedDictionary(featuresArr)

    # create a list of tokens
    tokens = codecs.open(reviewPath, "r", "utf-8").read().split()
        
    # for each token, if it in the feature list enable his flag
    for token in tokens:
        if token in featuresArr:
            featuresDic[token] = 1

    # return only the vector
    representationVector = list(featuresDic.values())

    # free the allocated memory of the dictionary
    del(featuresDic)

    return representationVector

# add the reviews within the specified path to the db with the given label using only the featured words
def AddVectorsToTrainingVectors(db, inputFolderPath, featuresArr, label):
    
    # Get all the txt file paths from the input folder
    txtFilesList = [ os.path.join(inputFolderPath, f) for f in os.listdir(inputFolderPath) if (os.path.isfile(os.path.join(inputFolderPath, f)) & str(f).endswith(".txt"))]
    
    # update the dictionary with each review vector
    for txtFile in txtFilesList:
        
        # add the tuple (representationVector , label) to the global db
        trainExample = (CreateRepresentationVector(txtFile, featuresArr) , label)
        db.append(trainExample)

    # return the updated db
    return db

# create the training vector DB
def CreateTrainingVectorDB(inputFolderPath, featuresArr):
    
    #initialize an empty DB
    db = []

    print("Add Positive reviews to the training set")
    db = AddVectorsToTrainingVectors(db, os.path.join(inputFolderPath, "pos"), featuresArr,  1)
    print("Add Negative reviews to the training set")
    db = AddVectorsToTrainingVectors(db, os.path.join(inputFolderPath, "neg"), featuresArr, -1)

    return db

# run ten fold cross validation on the training db to evaluate it's results
# prints avarage of: recall, percision, accuracy, f-score
def CrossValidateDB(vectorDb, featruresArr):
    #TODO
    return None

# classify the given vector using naive Bayes algorithm
def NaiveBayesClassifyVector(vec, trainingVectorsDb):
    # N is the size of the train DB
    N = len(trainingVectorsDb)

    # initialize the classes
    classes = [1, -1]

    # check what is the most likely class for the vector
    classesProb = [0, 0]

    # for each class calculate it's probability
    for classIdx in range(len(classes)):
            
        # counter for all the occurrances of the class in the training DB
        sum_c = 0

        # counters array for all the occurrances of a feature with the specified class in the training DB
        sum_features = [0] * len(vec)

        # run over all the vectors in the training Db and count the occurrances
        for trainingVector in TrainingVectorDb:
            if trainingVector[1] == classes[classIdx]:
                sum_c = sum_c + 1
                for featureIdx in range(len(vec)):
                    if trainingVector[0][featureIdx] == vec[featureIdx]:
                        sum_features[featureIdx] = sum_features[featureIdx] + 1

        # calculate the probabilities using add 1 laplace smoothing (adding 1 to the numerator and the number of classes to the denominator)
        classesProb[classIdx] = math.log(sum_c / N)
        for featureIdx in range(len(vec)):
            classesProb[classIdx] = classesProb[classIdx] + math.log((sum_features[featureIdx] + 1) / (sum_c + len(classes)))
        classesProb[classIdx] = math.exp(classesProb[classIdx])

    # return the chosen class
    return classes[classesProb.index(max(classesProb))]

# classify the reviews located in the test folder path using NaiveBayes algorithm 
def NaiveBayesClassify(testFolderPath, trainingVectorsDb, featuresArr):
    
     # Get all the txt file paths from the test folder
    txtFilesList = [ os.path.join(testFolderPath, f) for f in os.listdir(testFolderPath) if (os.path.isfile(os.path.join(testFolderPath, f)) & str(f).endswith(".txt"))]
    
    # try to classify each txtFile
    for txtFile in txtFilesList:
        
        # create the vector representing the current review 
        vec = CreateRepresentationVector(txtFile, featuresArr)

        # classify the vector
        classification = NaiveBayesClassifyVector(vec, trainingVectorsDb)

        # take the class wich maximize the probability and print it 
        print(txtFile, classification)

#********************** NLP **********************#
# Main Program 

StartTime = time.clock()

# parse the command line arguments
executionMode,InputFilesFolder,TestsFilesFolder = GetCommandLineArguments()

# create the feature vector - For now from all the words in the text
featuresArr = GetDictionary(InputFilesFolder)

# create the train DB vectors
TrainingVectorDb = CreateTrainingVectorDB(InputFilesFolder, featuresArr)

# if we are in evaluation mode
if executionMode == "-e":
    CrossValidateDB(TrainingVectorDb, featuresArr)

# if we are in classify mode
if executionMode == "-c":
    # Classify the new reviews using NaiveBayes classifier
    NaiveBayesClassify(TestsFilesFolder, TrainingVectorDb, featuresArr)

print("Total Time (sec):\t\t\t" ,time.clock() - StartTime)