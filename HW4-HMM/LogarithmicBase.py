import sys, os, time, codecs, math,re
from collections import Counter

# Calculate the probability that a sentence will start with a specific tag
# returns piDic: dictionary, keys are tags, values are the probability that a sentence will start with this tag
#   e.g. piDic['adverb'] = 0.5 -> half of the sentences starts with the tag 'adverb'               
#                             -> the probability that a sentence will start with a 'adverb' is 0.5
def LogarithmicBase_CalculatePi(trainData,tagDic):
    
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
        if (tagCount / SentencesCount) == 0:
            piDic[tag] = math.log(1e-50)
        else:
            piDic[tag] = math.log(tagCount / SentencesCount)
  
    # Init all the tags that never starts a sentence
    for tag in tagDic:
        if not (tag in piDic):
            piDic[tag] = math.log(1e-50)

    return piDic


# Calculate the probability of a tag: given the previous tag
# returns tagTransitionProbDic: a dictionary were the key are preceding Tag, 
#           values are dictionary were the keys are following Tag and the values are Transition Probability
#   e.g. tagTransitionProbDic['adverb']['noun'] = 0.5 
#                   -> half of the tags that comes after 'adverb' are 'noun'
#                   -> the probability of a tag 'noun' given the previous tag was 'adverb' is 0.5
def LogarithmicBase_TagTransitionProbabilities(trainData,tagDic):
    
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
            if (tagTransitionProbDic[tag1][tag2] / tagDic[tag1]) == 0:
                tagTransitionProbDic[tag1][tag2] = math.log(1e-50)
            else:
                tagTransitionProbDic[tag1][tag2] = math.log(tagTransitionProbDic[tag1][tag2] / tagDic[tag1])
            
                              
    return tagTransitionProbDic


# Calculate the probability of a token: given it's tag
# returns wordLikelihoodProbDic: a dictionary were the key are preceding Tag, values are also a dictionary
#            were the keys are tokens and the values are Probability of the token given the tag
#   e.g. wordLikelihoodProbDic['adverb']['dog'] = 0.3
#                   -> the probability of a token 'dog' given it's tagged 'adverb' is 0.3       
def LogarithmicBase_WordLikelihoodProbabilities(trainData,tokenDic,tagDic):
    
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
            if (wordLikelihoodProbDic[tag][token] / tagDic[tag]) == 0:
                wordLikelihoodProbDic[tag][token] = math.log(1e-50)
            else:
                wordLikelihoodProbDic[tag][token] = math.log(wordLikelihoodProbDic[tag][token] / tagDic[tag])
            
    return wordLikelihoodProbDic


# Viterby algorithm 
# input markovModel = (tokenDic,tagDic,piDic,tagTransitionProbDic,wordLikelihoodProbDic) 
# return tags - a list of tags, as the size of the input sentence 
#               the tag of the i word in the sentence is the i elemnet in tags
#   e.g. tags[0] = 'adverb' -> the tag of the first word is adverb
#        tags[4] = 'noun' -> the tag of the fifth token is noun  
def LogarithmicBase_RunViterbyAlg(sentence,markovModel):
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
        viterbyMatrix[0][tag] = ( piProb + wordLikelihoodProb , tag )

    # Fill in the matrix 
    for i in range(1,sentenceLen):                      # for each time
        for tag in tagDic:                              # go over all tags
            viterbyMatrix[i][tag] = (-1e1000,'emptyTag')   # init prob
            
            # calc word Likelihood Probability
            if sentence[i] in tokenDic:
                wordLikelihoodProb = wordLikelihoodProbDic[tag][sentence[i]]
            else:
                wordLikelihoodProb = wordLikelihoodProbDic[tag]["Kukiritza"]
            
            # go over all tag in previous time
            for previousTag in tagDic:
                previousTagProb = viterbyMatrix[i-1][previousTag][0]            # the probability og the tag in previous time 
                transitionProb = tagTransitionProbDic[previousTag][tag]         # transition probabilty from previous tag to current tag
                prob = previousTagProb + transitionProb + wordLikelihoodProb    # current probabilty using specific previous tag 
                if prob > viterbyMatrix[i][tag][0]:
                    viterbyMatrix[i][tag] = (prob,previousTag)                  # save the max prob
    
    # find the max tag prob in the last column of the viterby matrix
    maxProb = -1e1000
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
def LogarithmicBase_EvaluateMarkovModel(evaluationData,markovModel):
    
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

    # count success/failure in tagging the tokens
    successCount = 0
    failureCount = 0
    for i in range( len(EvaluationData_Tokens) ):
        sentence = EvaluationData_Tokens[i]                 # list of tokens
        knownTags = EvaluationData_Tags[i]                  # list on known tags
        assumeTags = LogarithmicBase_RunViterbyAlg(sentence,markovModel)    # list of assume tags
        
        for i in range( len(knownTags) ):
            if knownTags[i] == assumeTags[i]:
                successCount = successCount + 1             
            else:
                failureCount = failureCount + 1 
           
    modelAccuracy = successCount / (successCount+failureCount)
    return modelAccuracy 





# *********************************************************************************************************************************
# *********************************************************************************************************************************
#                   Testing          Testing              Testing          Testing             Testing          Testing
# *********************************************************************************************************************************
# *********************************************************************************************************************************

#import LogarithmicBase

#StartTime = time.clock()
#piDic = LogarithmicBase.LogarithmicBase_CalculatePi(trainData,tagDic)
#print("LogarithmicBase_CalculatePi() (sec):\t\t\t" ,time.clock() - StartTime)

#StartTime = time.clock()
#tagTransitionProbDic = LogarithmicBase.LogarithmicBase_TagTransitionProbabilities(trainData,tagDic)
#print("LogarithmicBase_TagTransitionProbabilities() (sec):\t" ,time.clock() - StartTime)

#StartTime = time.clock()
#wordLikelihoodProbDic = LogarithmicBase.LogarithmicBase_WordLikelihoodProbabilities(trainData,tokenDic,tagDic)
#print("LogarithmicBase_WordLikelihoodProbabilities() (sec):\t" ,time.clock() - StartTime)

#markovModel = (tokenDic,tagDic,piDic,tagTransitionProbDic,wordLikelihoodProbDic)

#if (executionMode == '-v'):
    
#    StartTime = time.clock()
#    evaluationData = ParseTaggedFile(evalOrTestFilePath)
#    print("ParseTaggedFile(evaluationFile) (sec):\t\t\t" ,time.clock() - StartTime)

#    StartTime = time.clock()
#    modelAccuracy = LogarithmicBase.LogarithmicBase_EvaluateMarkovModel(evaluationData,markovModel)
#    print("LogarithmicBase_EvaluateMarkovModel() (sec):\t\t" ,time.clock() - StartTime)

#    print("\nLogarithmic-base model Accuracy is: ",modelAccuracy,"%\n")

#elif(executionMode == '-t'):
#    print('testing mode')
#else:
#    sys.exit("\nWrong input. Please check your command line arguments \nTo run hmm.py in evaluation mode run: \n\t hmm.py -v --train TRAINING_FILE.txt --eval EVALUATION_FILE.txt \nTo run hmm.py in testing mode run: \n\t hmm.py -t --train TRAINING_FILE.txt --test TESTING_FILE.txt")
#sys.stdin.read(1)


