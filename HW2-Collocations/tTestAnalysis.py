
import sys, os, codecs, math, operator

# t-test analysis
# input: txtFilesList - texts to analyze
#        tTest_Raw_outStream / tTest_Select_outStream - output files
def tTestAnalysis(txtFilesList,tTest_Raw_outStream,tTest_Select_outStream, collocationsFreqs):
    
    # class for creating a counted dictionary
    from collections import Counter
    tokensFreqs = Counter()

    # Analysis each text  
    for f in txtFilesList:
        print("t-test analysis " + f + " :")

        # open the input file
        inputFileStream  = codecs.open(f,"r","utf-8")

        # update the dictionary of tokens of the current text file to the global freq dictionary
        tokensFreqs.update(Counter(inputFileStream.read().split()))
    
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
    Top100Collocations = sorted(tScoreDic.items(), key=operator.itemgetter(1))[0:100]

    # Output the top 100 tTest scores into tTest_raw.txt file
    tTest_Raw_outStream.writelines((("%15d\t%30s\t%f " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(Top100Collocations)))
    tTest_Raw_outStream.close() 
    
    # List the collocations with exactly 20 appearances
    TwentyAppearances = []
    for Key, Value in collocationsFreqs.items():
        if Value == 20:
            TwentyAppearances.append((Key,tScoreDic[Key]))

    # Output the collocations with exactly 20 appearances with their tTest score into tTest_select.txt file
    tTest_Select_outStream.writelines((("%15d\t%30s\t%f " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(TwentyAppearances)))
    tTest_Select_outStream.close()

    return 'Done'
    