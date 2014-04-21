#********************** NLP **********************#
# H.W 3
# Haim Shalelashvily    200832780
# Zahi Kfir             200681476
#********************** NLP **********************#

import sys, os, time, codecs, math
from collections import Counter

# global var which will hold the size of the representation vectors
repVectorLen = 0

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
def GetIndexedDictionary(inputFolderPath):
    
    startTime = time.clock()

    dic = Counter()

    # Get all the txt file paths from the positive folder
    print("Creating dictionary (feature vector) from the positive reviews input folder")
    posFolder = os.path.join(inputFolderPath, "pos")
    txtFilesList = [ os.path.join(posFolder, f) for f in os.listdir(posFolder) if (os.path.isfile(os.path.join(posFolder, f)) & str(f).endswith(".txt"))]
    
    # update the dictionary with each review
    for txtFile in txtFilesList:
        file = codecs.open(txtFile,"r","utf-8")
        dic.update(Counter(file.read().split()))
        file.close()

    # Get all the txt file paths from the positive folder
    print("Updating the dictionary (feature vector) from the negative reviews input folder")
    posFolder = os.path.join(inputFolderPath, "neg")
    txtFilesList = [ os.path.join(posFolder, f) for f in os.listdir(posFolder) if (os.path.isfile(os.path.join(posFolder, f)) & str(f).endswith(".txt"))]
    
    # update the dictionary with each review
    for txtFile in txtFilesList:
        file = codecs.open(txtFile,"r","utf-8")
        dic.update(Counter(file.read().split()))
        file.close()
        
    # Temp fast dictionary
    #dic = {"good":0,"bad":1}

    # set the representation vector len
    global repVectorLen
    repVectorLen = len(dic)

    # set index to each value
    for i, item in enumerate(dic):
        dic[item] = i

    print("Get dictionary was executed in ", time.clock()-startTime)
    print(len(dic), " features in the list")
    
    # return a key ordered dictionary
    return dic

# create an empty representation vector
def GetEmptyRepresentationVector():
    return [0] * repVectorLen

# create a representation vector to a review
def CreateRepresentationVector(reviewPath, indexedFeaturesDic):
    
    # initialize a feature vector for this file
    repVec = GetEmptyRepresentationVector()

    # create a list of tokens
    file = codecs.open(reviewPath, "r", "utf-8")
    
    # for each token, if it in the feature list enable his flag
    for token in set(file.read().split()):
        if token in indexedFeaturesDic:
            repVec[indexedFeaturesDic[token]] = 1

    file.close()

    return repVec

# add the reviews within the specified path to the db with the given label using only the featured words
def AddVectorsToTrainingVectors(db, inputFolderPath, indexedFeaturesDic, label):
    
    # Get all the txt file paths from the input folder
    txtFilesList = [ os.path.join(inputFolderPath, f) for f in os.listdir(inputFolderPath) if (os.path.isfile(os.path.join(inputFolderPath, f)) & str(f).endswith(".txt"))]
    
    # update the dictionary with each review vector
    for txtFile in txtFilesList:
        
        # add the tuple (representationVector , label) to the global db
        trainExample = (CreateRepresentationVector(txtFile, indexedFeaturesDic) , label)
        db.append(trainExample)

    # return the updated db
    return db

# create the training vector DB
def CreateTrainingVectorDB(inputFolderPath, indexedFeaturesDic):
    
    startTime = time.clock()

    #initialize an empty DB
    db = []

    print("Add Positive reviews to the training set")
    db = AddVectorsToTrainingVectors(db, os.path.join(inputFolderPath, "pos"), indexedFeaturesDic,  1)
    print("Add Negative reviews to the training set")
    db = AddVectorsToTrainingVectors(db, os.path.join(inputFolderPath, "neg"), indexedFeaturesDic, -1)

    print("CreateTrainingVectorDB was executed in ", time.clock()-startTime)

    return db

# create the training vector db's probability db
def CreateProbabilityTrainingDB(vectorDb):
    
    print("Start creating probability Training DB")
    startTime = time.clock()

    # N is the size of the train DB
    N = len(vectorDb)

    # initialize the probability db
    probabilityDb = {1 : [0, {0 : GetEmptyRepresentationVector(), 1 : GetEmptyRepresentationVector()}],
                    -1 : [0, {0 : GetEmptyRepresentationVector(), 1 : GetEmptyRepresentationVector()}]}

    classSumIndex = 0
    featuresCountersArrayIndex = 1

    # run over all the vectors in the training Db and count the occurrances
    for trainingVector in vectorDb:
        
        vectorClassification = trainingVector[1]

        # increase the number of occurrances of the class
        probabilityDb[vectorClassification][classSumIndex] = probabilityDb[vectorClassification][classSumIndex] + 1

        # increase the number of the occurrances of the specific feature within a specific class
        for featureIdx in range(repVectorLen):

            vectorCurrentFeature = trainingVector[0][featureIdx]

            probabilityDb[vectorClassification][featuresCountersArrayIndex][vectorCurrentFeature][featureIdx] = probabilityDb[vectorClassification][featuresCountersArrayIndex][vectorCurrentFeature][featureIdx] + 1

    # calculate the probabilities using add 1 laplace smoothing (adding 1 to the numerator and the number of classes to the denominator) and replace the counts
    for clasificationClass in probabilityDb.keys():
        for counterVector in probabilityDb[clasificationClass][1].values():
            for featureIdx in range(repVectorLen):
               counterVector[featureIdx] = (counterVector[featureIdx] + 1) / (probabilityDb[clasificationClass][classSumIndex] + len(probabilityDb.keys()))


    print("probabilityTrainingDb creation was executed in ", time.clock()-startTime)

    # return the db
    return probabilityDb

# run ten fold cross validation on the training db to evaluate it's results
# prints avarage of: recall, percision, accuracy, f-score
def CrossValidateDB(vectorDb):
    
    # get the size of the db
    N = len(vectorDb)
    posStart = 0 
    negStart = math.ceil(N/2) 
    
    # number of folds
    numFolds = 10
    precision = []
    recall    = [] 
    accurracy = []
    fScore    = []
  
    # run ten folds
    for i in range(numFolds):

        print("Evaluating fold #", i)

        print("Start copying arrays to train and test dbs")
        startTime = time.clock()

        # initialize the training and test db
        train = vectorDb[posStart:math.ceil(posStart + i*(N/(numFolds*2)))]
        test  = vectorDb[math.ceil(posStart + i*(N/(numFolds*2))): math.ceil(posStart + (i+1)*(N/(numFolds*2)))]
        train.extend(vectorDb[math.ceil(posStart + (i+1)*(N/(numFolds*2))): math.ceil(N/2)])

        train.extend(vectorDb[negStart:math.ceil(negStart + i*(N/(numFolds*2)))])
        test.extend(vectorDb[math.ceil(negStart + i*(N/(numFolds*2))): math.ceil(negStart + (i+1)*(N/(numFolds*2)))])
        train.extend(vectorDb[math.ceil(negStart + (i+1)*(N/(numFolds*2))):])

        print("copies was executed in ", time.clock()-startTime)

        # create probability train db
        probTrainDb = CreateProbabilityTrainingDB(train)

        TP = FP = TN = FN = 0
        
        # run classification on each vector in the test db
        for testVec in test:
            
            # classify the vector
            classification = NaiveBayesClassifyVector(testVec[0], probTrainDb)
            
            # update statistics
            if classification == testVec[1]: # true result
                if classification == 1: TP = TP + 1 # positive result
                else: TN = TN + 1 # negative result
            else: # false result
                if classification == -1: FN = FN + 1 # negative result
                else: FP = FP + 1 # positive result

        precision.append((TP / (TP + FP)))
        recall.append((TP / (TP + FN)))
        accurracy.append(((TP + TN) / (TP + TN + FP + FN)))
        fScore.append(((2 * precision[i] * recall[i]) / (precision[i] + recall[i]))) # blanced fScore using a=1/2

        # print the results of the current fold
        print("precision : ", precision[i])
        print("recall : ", recall[i])
        print("accurracy : ", accurracy[i])
        print("fScore : ", fScore[i])

    # print the avarage over all folds
    print("avg precision : ", float(sum(precision))/len(precision))
    print("avg recall : ", float(sum(recall))/len(recall))
    print("avg accurracy : ", float(sum(accurracy))/len(accurracy))
    print("avg fScore : ", float(sum(fScore))/len(fScore))

# classify the given vector using naive Bayes algorithm
def NaiveBayesClassifyVector(vec, trainingProbabilityDb):
    
    print("Start classifing vector")
    startTime = time.clock()
        
    # helpers
    N = len(trainingProbabilityDb)
    classSumIndex = 0
    featuresCountersArrayIndex = 1

    # initialize the classes
    classes = [1, -1]

    # check what is the most likely class for the vector
    classesProb = [0, 0]

    # for each class calculate it's probability
    for classIdx in range(len(classes)):
            
        # calculate the probabilities using add 1 laplace smoothing (adding 1 to the numerator and the number of classes to the denominator)
        classesProb[classIdx] = math.log(trainingProbabilityDb[classes[classIdx]][classSumIndex] / N)
        for featureIdx in range(repVectorLen):
            classesProb[classIdx] = classesProb[classIdx] + math.log((trainingProbabilityDb[classes[classIdx]][featuresCountersArrayIndex][vec[featureIdx]][featureIdx] + 1) / (trainingProbabilityDb[classes[classIdx]][classSumIndex] + len(classes)))
        classesProb[classIdx] = math.exp(classesProb[classIdx])

    print("classification was executed in ", time.clock()-startTime)

    # return the chosen class
    return classes[classesProb.index(max(classesProb))]

# classify the reviews located in the test folder path using NaiveBayes algorithm 
def NaiveBayesClassify(testFolderPath, trainingProbabilityDb, indexedFeaturesDic):
    
     # Get all the txt file paths from the test folder
    txtFilesList = [ os.path.join(testFolderPath, f) for f in os.listdir(testFolderPath) if (os.path.isfile(os.path.join(testFolderPath, f)) & str(f).endswith(".txt"))]
    
    # try to classify each txtFile
    for txtFile in txtFilesList:
        
        # create the vector representing the current review 
        vec = CreateRepresentationVector(txtFile, indexedFeaturesDic)

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
indexedFeaturesDic = GetIndexedDictionary(InputFilesFolder)

# create the train DB vectors
TrainingVectorDb = CreateTrainingVectorDB(InputFilesFolder, indexedFeaturesDic)

# if we are in evaluation mode
if executionMode == "-e":
    CrossValidateDB(TrainingVectorDb)

# if we are in classify mode
if executionMode == "-c":

    # create the probability training db
    ProbabilityTrainingDb = CreateProbabilityTrainingDB(TrainingVectorDb)

    # Classify the new reviews using NaiveBayes classifier
    NaiveBayesClassify(TestsFilesFolder, ProbabilityTrainingDb, indexedFeaturesDic)

print("Total Time (sec):\t\t\t" ,time.clock() - StartTime)