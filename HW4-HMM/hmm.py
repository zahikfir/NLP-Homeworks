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
    
    print('\nStart Program. \n\t Execution mode: {0} \n\t trainFilePath: {1} \n\t evalOrTestFilePath: {2}\n'.format(executionMode, trainFilePath, evalOrTestFilePath))

    return executionMode,trainFilePath,evalOrTestFilePath


# Parse the training file and returns a list of sentences, each sentence is a list of (word,POS)
def ParseTrainingFile(trainFilePath):
    returnVariable = []

    trainFile = codecs.open(trainFilePath,"r","utf-8")              # Open the train file
    trainSentences = re.split(".(?=\.\t|\?\t|\!\t)",trainFile.read())     # Split the train file into sentences

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
        
        returnVariable.append(currentSentence)      # Push current sentence
        currentSentence = []                        # Reset current sentence

        # For each row (except the first)
        for row in trainRows[1:]:
            columns = row.split("\t")               # Split the row into columns (each column represent a word/token or a label)
            if len(columns) >= 4:
              currentSentence.append( (columns[1],columns[3]) )    # (columns[1] = token) , (columns[3] = POS)
    
    returnVariable.append(currentSentence)          # push last sentence

    # replace all empty POS with 'clitic'
    for i in range( len(returnVariable) ):
        for j in range( len(returnVariable[i]) ):
            if returnVariable[i][j][1] == '':
                returnVariable[i][j] = (returnVariable[i][j][0],'clitic')

    return returnVariable 


# Replace all the tokens that appear once to uniformToken
# Return tokenDic - all tokens and their count
# Return tagDic - all pos tags and their count
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
def RunViterbyAlg(sentence,tokenDic,tagDic,piDic,tagTransitionProbDic,wordLikelihoodProbDic):
    
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
    



# Get Command Line Arguments
executionMode,trainFilePath,evalOrTestFilePath = GetCommandLineArguments()

StartTime = time.clock()
trainData = ParseTrainingFile(trainFilePath)
print("ParseTrainingFile() (sec):\t\t" ,time.clock() - StartTime)

StartTime = time.clock()
trainData,tokenDic,tagDic = BindAllSingleTokens(trainData,"Kukiritza")
print("BindAllSingleTokens()(sec):\t\t" ,time.clock() - StartTime)

StartTime = time.clock()
piDic = CalculatePi(trainData,tagDic)
print("CalculatePi()(sec):\t\t\t" ,time.clock() - StartTime)

StartTime = time.clock()
tagTransitionProbDic = TagTransitionProbabilities(trainData,tagDic)
print("TagTransitionProbabilities()(sec):\t" ,time.clock() - StartTime)

StartTime = time.clock()
wordLikelihoodProbDic = WordLikelihoodProbabilities(trainData,tokenDic,tagDic)
print("WordLikelihoodProbabilities()(sec):\t" ,time.clock() - StartTime)

sentence = ['zk1','zk2','zk3','zk4']
StartTime = time.clock()
tags = RunViterbyAlg(sentence,tokenDic,tagDic,piDic,tagTransitionProbDic,wordLikelihoodProbDic)
print("RunViterbyAlg()(sec):\t" ,time.clock() - StartTime)


outputFile = codecs.open("OutputFile.txt", "w", "utf-8")        # for debug only !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
for sentence in trainData:
    if len(sentence) >= 1:
        for word in sentence:
            outputFile.writelines(word[0]+ " ")
        outputFile.write(os.linesep)

print("\nHW4 - Hidden Markov model\n") 

