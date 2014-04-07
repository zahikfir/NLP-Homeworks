
import sys, os, codecs, math, operator, time

# t-test analysis
# input: txtFilesList - texts to analyze
#        tTestTop100 / tTest20Appearances - output files
def tTestAnalysis(tTestTop100,tTest20Appearances,collocationsFreqs,tokensFreqs):
    StartTime = time.clock()
  
    # get the number of tokens in all the corpus
    numOfTokens = sum(tokensFreqs.values())

    # for each colocation - give it a t-score and put it in a dictionary
    tScoreDic = dict()
    for collocation in collocationsFreqs:
        
        # get the frequencies and set the probabilities
        collocProb = collocationsFreqs[collocation] / numOfTokens
        word1Prob  = tokensFreqs[collocation.split()[0]] / numOfTokens
        word2Prob  = tokensFreqs[collocation.split()[1]] / numOfTokens

        # calculate the statistics
        meanOfDistributation = word1Prob * word2Prob
        sampleVariance = (meanOfDistributation) * (1 - meanOfDistributation)
        sampleMean = collocProb * (1 - collocProb)

        # set the tscore
        if not sampleVariance == 0 : tScoreDic[collocation] = (math.fabs(sampleVariance - meanOfDistributation)) / (math.sqrt(sampleVariance / numOfTokens))

    # Get the top 100 collocations
    Top100Collocations = sorted(tScoreDic.items(), key=operator.itemgetter(1),reverse=True)[0:100]

    # Output the top 100 tTest scores into tTest_raw.txt file
    tTestTop100.writelines((("%15d\t%30s\t%f " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(Top100Collocations)))
    tTestTop100.close() 
    
    # List the collocations with exactly 20 appearances
    TwentyAppearances = []
    for Key, Value in collocationsFreqs.items():
        if Value == 20:
            TwentyAppearances.append((Key,tScoreDic[Key]))

    # Sort the collocations with exactly 20 appearances by the T-test score
    TwentyAppearances.sort(key=operator.itemgetter(1),reverse= True)

    # Output the collocations with exactly 20 appearances with their tTest score into tTest_select.txt file
    tTest20Appearances.writelines((("%15d\t%30s\t%f " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(TwentyAppearances)))
    tTest20Appearances.close()

    print("tTestAnalysis() (sec):\t\t" ,time.clock() - StartTime)
    return tokensFreqs
    