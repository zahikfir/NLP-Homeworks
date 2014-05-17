#********************** NLP **********************#
# H.W 4
# Haim Shalelashvily    200832780
# Zahi Kfir             200681476
#********************** NLP **********************#

import sys, os, time, codecs, math,re
from collections import Counter


# Return the execution mod and the appropriate command arguments
def GetCommandLineArguments():
    try:
        if len(sys.argv) < 4: 
            sys.exit()

        executionMode = sys.argv[1]
        trainFilePath = sys.argv[sys.argv.index("--train") + 1]

        if (executionMode == '-v'):         # Evaluation mode
            evalOrTestFilePath = sys.argv[sys.argv.index("--eval") + 1]
        elif (executionMode == '-t'):       # Test mode 
            evalOrTestFilePath = sys.argv[sys.argv.index("--test") + 1]
        else:                               # wrong execution mode
            sys.exit()
    
    except:                                 # if one of the option parameters is missing
        sys.exit("\nWrong input. Please check your command line arguments \nTo run hmm.py in evaluation mode run: \n\t hmm.py -v --train TRAINING_FILE.txt --eval EVALUATION_FILE.txt \nTo run hmm.py in testing mode run: \n\t hmm.py -t --train TRAINING_FILE.txt --test TESTING_FILE.txt")
    
    print('Program parameters description: \n\t Execution mode: {0} \n\t trainFilePath: {1} \n\t evalOrTestFilePath: {2}\n'.format(executionMode, trainFilePath, evalOrTestFilePath))

    return executionMode,trainFilePath,evalOrTestFilePath


# Parse the training file and returns a list of sentences, each sentence is a list of (word,POS)
# Returns trainData: list of sentences, each sentence is a list of word, each word is (Token,POS-tag)
#
# [--------------------------------------- trainData ---------------------------------------]
# [ [sentence-1]...[ (word-1,POS-Tag)(word-2,POS-Tag)...(word-n,POS-Tag)  ]...[sentence-n]  ]
#                  [--------------------- sentence k ---------------------]
#
#       e.g. trainData[5][4][0] - the token in sentence 5 word 4
#            trainData[5][4][1] - the tag of the in sentence 5 word 4  
def ParseTaggedFile(trainFilePath):
    trainData = []

    trainFile = codecs.open(trainFilePath,"r","utf-8")                  # Open the train file
    trainSentences = re.split(".(?=\.\t|\?\t|\!\t)",trainFile.read())   # Split the train file into sentences

    currentSentence = []

    # Handle the first sentence
    trainRows = trainSentences[0].split("\n")       # Split the first sentence into row (each row represent a word/token and its labels)
    for row in trainRows:                           # For each row
        columns = row.split("\t")                   # Split the row into columns (each column represent a word/token or a label)
        if len(columns) >= 4:
            currentSentence.append( (columns[1],columns[3]) )      # (columns[1] = token) , (columns[3] = POS)

    # For each sentence (except the first)
    for sentence in trainSentences[1:]:   
        trainRows = sentence.split("\n")            # Split the sentence into row (each row represent a word/token and its labels)
    
        # The first row is the punctuation at the end of the last sentence
        columns = trainRows[0].split("\t")          # Split the row into columns (each column represent a word/token or a label)
        if len(columns) >= 4:
              currentSentence.append( (columns[0],columns[2]) )    # (columns[0] = token) , (columns[2] = POS)
        
        trainData.append(currentSentence)           # Push current sentence
        currentSentence = []                        # Reset current sentence

        # For each row (except the first)
        for row in trainRows[1:]:
            columns = row.split("\t")               # Split the row into columns (each column represent a word/token or a label)
            if len(columns) >= 4:
              currentSentence.append( (columns[1],columns[3]) )    # (columns[1] = token) , (columns[3] = POS)
    
    trainData.append(currentSentence)          # push last sentence

    # replace all empty POS with 'clitic'
    for i in range( len(trainData) ):
        for j in range( len(trainData[i]) ):
            if trainData[i][j][1] == '':
                trainData[i][j] = (trainData[i][j][0],'clitic')

    return trainData 


# parse the testing file 
# returns testData: list of sentences, each sentence is a list of tokens
# testData[0][1] = 'dog'  -> the second token of the first sentence is dog
def ParseTestFile(evalOrTestFilePath):
    
    testData = []
    trainFile = codecs.open(evalOrTestFilePath,"r","utf-8")     # Open the test file
    trainSentences = trainFile.read().split('\n')               # split the data into sentences list           
    for sentence in trainSentences:                             
        testData.append(sentence.split())                       # split the sentence into tokens list

    return testData


# Replace all the tokens that appear once to uniformToken
# Return tokenDic: a dictionary, the keys are tokens and the values are number of appearances
#   e.g. tokenDic['Dog'] = 5 -> there are 5 appearances of the token 'Dog' in the training corpus
# Return tagDic - a dictionary, the keys are POS/tags and the values are number of appearances
#   e.g. tagDic['adverb'] = 5 -> there are 5 appearances of the tag 'adverb' in the training corpus
def BindAllSingleTokens(trainData,uniformToken):
    
    # Count token appearances
    tokenDic = Counter()
    tagDic = Counter()        
    for sentence in trainData:
        for word in sentence:
            tokenDic.update( [word[0]] )
            tagDic.update( [word[1]] )

    # List all the tokens with single appearance
    appearOnceList = []
    for token,val in tokenDic.items():
        if val == 1:
            appearOnceList.append(token)

    # Replace all the tokens that appear once
    for i in range( len(trainData) ):
        for j in range( len(trainData[i]) ):
            if trainData[i][j][0] in appearOnceList:
                trainData[i][j] = (uniformToken,trainData[i][j][1])

    # Update tokenDic after the replacements
    tokenDic[uniformToken] = len(appearOnceList)
    for token in appearOnceList:
        tokenDic.pop(token)

    return trainData,tokenDic,tagDic


# Calculate the probability that a sentence will start with a specific tag
# returns piDic: dictionary, keys are tags, values are the probability that a sentence will start with this tag
#   e.g. piDic['adverb'] = 0.5 -> half of the sentences starts with the tag 'adverb'               
#                             -> the probability that a sentence will start with a 'adverb' is 0.5
def CalculatePi(trainData,tagDic):
    
    # Count tag appearances at the beginning of a sentence
    openTagCounter = Counter()
    for sentence in trainData:
        if len(sentence) >= 1:
            firstWord = sentence[0]
            openTagCounter.update( [firstWord[1]] )
    
    # Calculate pi for each tag
    piDic = dict()
    SentencesCount = len(trainData)
    for tag,tagCount in openTagCounter.items():
        piDic[tag] = tagCount / SentencesCount
  
    # Init all the tags that never starts a sentence
    for tag in tagDic:
        if not (tag in piDic):
            piDic[tag] = 0

    return piDic


# Calculate the probability of a tag: given the previous tag
# returns tagTransitionProbDic: a dictionary were the key are preceding Tag, 
#           values are dictionary the keys are following Tag and the values are Transition Probability
#   e.g. tagTransitionProbDic['adverb']['noun'] = 0.5 
#                   -> half of the tags that comes after 'adverb' are 'noun'
#                   -> the probability of a tag 'noun' given the previous tag was 'adverb' is 0.5
def TagTransitionProbabilities(trainData,tagDic):
    
    # Create empty dictionary
    tagTransitionProbDic = dict()
    for tag1 in tagDic:
        tagTransitionProbDic[tag1] = dict()
        for tag2 in tagDic:
            tagTransitionProbDic[tag1][tag2] = 0
    
    # Update the dictionary with the counts
    for i in range( len(trainData) ):               # loop all sentences in train data
        for j in range( len(trainData[i])-1 ):      # loop all words in sentence
            precedingTag = trainData[i][j][1]       # current word
            followingTag = trainData[i][j+1][1]     # next word
            tagTransitionProbDic[precedingTag][followingTag] = tagTransitionProbDic[precedingTag][followingTag] + 1 
    
    # Update the dictionary with the probabilities
    for tag1 in tagTransitionProbDic:
        for tag2 in tagTransitionProbDic:
            tagTransitionProbDic[tag1][tag2] = tagTransitionProbDic[tag1][tag2] / tagDic[tag1]
                              
    return tagTransitionProbDic


# Calculate the probability of a token: given it's tag
# returns wordLikelihoodProbDic: a dictionary the key are preceding Tag, values are also a dictionary
#            were the keys are tokens and the values are Probability of the token given the tag
#   e.g. wordLikelihoodProbDic['adverb']['dog'] = 0.3
#                   -> the probability of a token 'dog' given it's tagged 'adverb' is 0.3       
def WordLikelihoodProbabilities(trainData,tokenDic,tagDic):
    
    # Create empty dictionary
    wordLikelihoodProbDic = dict()
    for tag in tagDic:
        wordLikelihoodProbDic[tag] = dict()
        for token in tokenDic:
            wordLikelihoodProbDic[tag][token] = 0
    
    # Update the dictionary with the counts
    for i in range( len(trainData) ):               # loop all sentences in train data
        for j in range( len(trainData[i]) ):        # loop all words in sentence
            currentToken = trainData[i][j][0]
            currentTag = trainData[i][j][1]
            wordLikelihoodProbDic[currentTag][currentToken] = wordLikelihoodProbDic[currentTag][currentToken]+ 1

    # Update the dictionary with the probabilities
    for tag in tagDic:
        for token in tokenDic:
            wordLikelihoodProbDic[tag][token] = wordLikelihoodProbDic[tag][token] / tagDic[tag]

    return wordLikelihoodProbDic


# Viterby algorithm 
# input markovModel = (tokenDic,tagDic,piDic,tagTransitionProbDic,wordLikelihoodProbDic) 
# return tags - a list of tags, as the size of the input sentence 
#               the tag of the i word in the sentence is the i elemnet in tags
#   e.g. tags[0] = 'adverb' -> the tag of the first word is adverb
#        tags[4] = 'noun' -> the tag of the fifth token is noun  
def RunViterbyAlg(sentence,markovModel):
    if len(sentence) == 0:
        return []

    # parse the markov model
    tokenDic = markovModel[0]
    tagDic = markovModel[1]
    piDic = markovModel[2]
    tagTransitionProbDic =  markovModel[3]
    wordLikelihoodProbDic = markovModel[4]
        
    # Initiate empty matrix
    emptyProb = 0
    emptyBacktrace = 'emptyTag'
    sentenceLen = len(sentence)
    viterbyMatrix = []
    for i in range(sentenceLen):
        viterbyMatrix.append(dict())
        for tag in tagDic:
            viterbyMatrix[i][tag] = (emptyProb,emptyBacktrace)

    # Calculate time 0 (first token)
    for tag in tagDic:
        piProb = piDic[tag]
        if sentence[0] in tokenDic:
            wordLikelihoodProb = wordLikelihoodProbDic[tag][sentence[0]]
        else:
            wordLikelihoodProb = wordLikelihoodProbDic[tag]["Kukiritza"]
        viterbyMatrix[0][tag] = ( piProb * wordLikelihoodProb , tag )

    # Fill in the matrix 
    for i in range(1,sentenceLen):                      # for each time
        for tag in tagDic:                              # go over all tags
            viterbyMatrix[i][tag] = (-100,'emptyTag')   # init prob
            
            # calc word Likelihood Probability
            if sentence[i] in tokenDic:
                wordLikelihoodProb = wordLikelihoodProbDic[tag][sentence[i]]
            else:
                wordLikelihoodProb = wordLikelihoodProbDic[tag]["Kukiritza"]
            
            # go over all tag in previous time
            for previousTag in tagDic:
                previousTagProb = viterbyMatrix[i-1][previousTag][0]            # the probability og the tag in previous time 
                transitionProb = tagTransitionProbDic[previousTag][tag]         # transition probabilty from previous tag to current tag
                prob = previousTagProb * transitionProb * wordLikelihoodProb    # current probabilty using specific previous tag 
                if prob > viterbyMatrix[i][tag][0]:
                    viterbyMatrix[i][tag] = (prob,previousTag)                  # save the max prob
    
    # find the max tag prob in the last column of the viterby matrix
    maxProb = -1
    maxTag = 'emptyTag'               
    for tag in tagDic:
        currentProb = viterbyMatrix[sentenceLen-1][tag][0]
        if currentProb > maxProb:
            maxProb = currentProb
            maxTag = tag           

    # append the tags using backtrace 
    tags = []
    tags.append(maxTag)
    for i in range(sentenceLen-1,0,-1):
        maxTag = viterbyMatrix[i][maxTag][1]
        tags.append(maxTag)
    tags.reverse()      # appended backwards (last tag first)
                      
    return tags
    

# evaluate the markov model using the Viterby algorithm
# returns modelAccuracy - (tagged correctly) / (all tags)
#         confusionMatrix - dictionary the keys are given tags the values are dictionay 
#                           that the key are true tags and the values are count
#   e.g.  confusionMatrix['adverb']['noun'] = 5  -> 5 tokens with a real tag of 'noun' tagged as 'adverb'                           
def EvaluateMarkovModel(evaluationData,markovModel):
    
    # extract token list and tag list from the evaluation file
    EvaluationData_Tokens = []
    EvaluationData_Tags = []
    for taggedSentence in  evaluationData:
        tokens = []
        taggs = [] 
        for word in taggedSentence:
            tokens.append(word[0])
            taggs.append(word[1])
        EvaluationData_Tokens.append(tokens)
        EvaluationData_Tags.append(taggs)

    # initialize the confusion matrix
    tagDic = markovModel[1]
    confusionMatrix = dict()
    for assumeTag in tagDic:
        confusionMatrix[assumeTag] = dict()
        for knownTag in tagDic:
            confusionMatrix[assumeTag][knownTag] = 0;

    # count success/failure in tagging the tokens
    successCount = 0
    failureCount = 0
    for i in range( len(EvaluationData_Tokens) ):
        sentence = EvaluationData_Tokens[i]                 # list of tokens
        knownTags = EvaluationData_Tags[i]                  # list on known tags
        assumeTags = RunViterbyAlg(sentence,markovModel)    # list of assume tags
        for i in range( len(knownTags) ):
            if knownTags[i] == assumeTags[i]:
                successCount = successCount + 1             
            else:
                failureCount = failureCount + 1 
                confusionMatrix[assumeTags[i]][knownTags[i]] = confusionMatrix[assumeTags[i]][knownTags[i]] + 1
           
    modelAccuracy = successCount / (successCount+failureCount)
    return modelAccuracy,confusionMatrix 


# writes the confusion matrix into "conf_matrix.txt"
def WriteConfusionMatrix(confusionMatrix):
    
    # open the output file
    outFile = codecs.open("conf_matrix.txt", "w", "utf-8")
    
    # write the columns headers
    outFile.write( '{0:18s}'.format("") )
    outFile.write('\t')
    for column in confusionMatrix:
        outFile.write( '{0:18s}'.format(column) )
        outFile.write('\t')
    outFile.write('\n')

    # write the rows
    for row,columns in confusionMatrix.items():
        outFile.write( '{0:18s}'.format(row) )
        outFile.write('\t')
        for column,value in columns.items():
            if value == 0:
                value_string = ""
            else:
                value_string = str(value)
            outFile.write( '{0:18s}'.format(value_string) )      
            #outFile.write( '{0:18s}'.format(column+value_string) )    # for debug, make sure the value consists with column header     
            outFile.write('\t')
        outFile.write('\n')

    outFile.close()
    return 0



print("---------------------- HW4 - Hidden Markov model ----------------------\n")  

# get Command Line Arguments
StartTime = time.clock()
executionMode,trainFilePath,evalOrTestFilePath = GetCommandLineArguments()
print("GetCommandLineArguments (sec):\t\t" ,time.clock() - StartTime)

# parse the training file
StartTime = time.clock()
trainData = ParseTaggedFile(trainFilePath)
print("ParseTaggedFile(trainingFile) (sec):\t" ,time.clock() - StartTime)

# replace single tokens with 'Kukiritza' + get 2 dictionaries - all tokens, all tags
StartTime = time.clock()
trainData,tokenDic,tagDic = BindAllSingleTokens(trainData,"Kukiritza")
print("BindAllSingleTokens() (sec):\t\t" ,time.clock() - StartTime)

# calculate the probability that a sentence will start with a specific tag
StartTime = time.clock()
piDic = CalculatePi(trainData,tagDic)
print("CalculatePi() (sec):\t\t\t" ,time.clock() - StartTime)

# calculate the probability of a tag: given the previous tag
StartTime = time.clock()
tagTransitionProbDic = TagTransitionProbabilities(trainData,tagDic)
print("TagTransitionProbabilities() (sec):\t" ,time.clock() - StartTime)

# calculate the probability of a token: given it's tag
StartTime = time.clock()
wordLikelihoodProbDic = WordLikelihoodProbabilities(trainData,tokenDic,tagDic)
print("WordLikelihoodProbabilities() (sec):\t" ,time.clock() - StartTime)

# build the markov model according to the training file
markovModel = (tokenDic,tagDic,piDic,tagTransitionProbDic,wordLikelihoodProbDic)

if (executionMode == '-v'):     # evaluation mode
    
    # parse the gold file (tagged by human) 
    StartTime = time.clock()
    evaluationData = ParseTaggedFile(evalOrTestFilePath)
    print("ParseTaggedFile(evaluationFile) (sec):\t" ,time.clock() - StartTime)

    # evaluate the markov model using the gold file
    StartTime = time.clock()
    modelAccuracy,confusionMatrix = EvaluateMarkovModel(evaluationData,markovModel)
    print("EvaluateMarkovModel() (sec):\t\t" ,time.clock() - StartTime)
    
    # writes the confusion matrix into "conf_matrix.txt" 
    StartTime = time.clock()
    WriteConfusionMatrix(confusionMatrix)
    print("PrintConfusionMatrix() (sec):\t\t" ,time.clock() - StartTime)

    # results
    print("\nmodel Accuracy is: ",modelAccuracy,"%")
    print("for error analysis see the confusion matrix in conf_matrix.txt\n")

elif(executionMode == '-t'):    # testing mode
    
    # parse the test file 
    StartTime = time.clock()
    testingData = ParseTestFile(evalOrTestFilePath)
    print("ParseTestFile() (sec):\t\t\t" ,time.clock() - StartTime)

    # tag the test file using the markov model
    #TODO

    print('testing mode')
else:
    sys.exit("\nWrong input. Please check your command line arguments \nTo run hmm.py in evaluation mode run: \n\t hmm.py -v --train TRAINING_FILE.txt --eval EVALUATION_FILE.txt \nTo run hmm.py in testing mode run: \n\t hmm.py -t --train TRAINING_FILE.txt --test TESTING_FILE.txt")






outputFile = codecs.open("OutputFile.txt", "w", "utf-8")        # for debug only !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
for sentence in trainData:
    if len(sentence) >= 1:
        for word in sentence:
            outputFile.writelines(word[0]+ " ")
        outputFile.write(os.linesep)

print("---------------------- HW4 - Hidden Markov model ----------------------\n")  
