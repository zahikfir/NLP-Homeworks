
import sys, os, codecs, re, time, math, operator

# t-test analysis
# input: txtFilesList - texts to analyze
#        tTestTop100_OFile / tTest20Appearances_OFile - output files
def tTestAnalysis(tTestTop100_OFile,tTest20Appearances_OFile,collocationsFreqs,tokensFreqs):
    StartTime = time.clock()

    numOfTokens = sum(tokensFreqs.values())  # Total number of tokens in all the texts

    # for each colocation - give it a t-score and put it in a dictionary
    tScoreDic = dict()
    for collocation in collocationsFreqs:
        
        # get the frequencies and set the probabilities
        collocProb = collocationsFreqs[collocation] / numOfTokens
        word1Prob  = tokensFreqs[collocation.split()[0]] / numOfTokens
        word2Prob  = tokensFreqs[collocation.split()[1]] / numOfTokens

        # calculate the statistics
        meanOfDistributation = word1Prob * word2Prob

        # set the tscore
        if not collocProb == 0 : tScoreDic[collocation] = (collocProb - meanOfDistributation) / (math.sqrt(collocProb / numOfTokens))

    # List Top 100 t-test scores
    Top100Collocations = sorted(tScoreDic.items(),key=operator.itemgetter(0))               # Alphabetically sort
    Top100Collocations = sorted(Top100Collocations, key=lambda tup: tup[1],reverse=True)    # Sort by count
    Top100Collocations = Top100Collocations[0:100]                                          # Get only top 100 collocations

    # Output the top 100 tTest scores into tTest_raw.txt file
    tTestTop100_OFile.writelines((("%15d\t%30s\t%.2f " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(Top100Collocations)))
    tTestTop100_OFile.close() 
    
    # List the collocations with exactly 20 appearances
    TwentyAppearances = []
    for Key, Value in collocationsFreqs.items():
        if Value == 20:
            TwentyAppearances.append((Key,tScoreDic[Key]))
    TwentyAppearances.sort(key=operator.itemgetter(0))                  # Alphabetically sort
    TwentyAppearances.sort(key=operator.itemgetter(1),reverse= True)    # Sort by count

    # Output the collocations with exactly 20 appearances with their tTest score into tTest_select.txt file
    tTest20Appearances_OFile.writelines((("%15d\t%30s\t%.2f " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(TwentyAppearances)))
    tTest20Appearances_OFile.close()

    print("tTestAnalysis() (sec):\t\t" ,time.clock() - StartTime)
    return time.clock() - StartTime
    