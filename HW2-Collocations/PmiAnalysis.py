
import sys, os, codecs, re, time, math, operator

# PMI analysis
# input: txtFilesList - texts to analyze
#        PmiTop100_OFile / Pmi20Appearances_OFile - output files
def PmiAnalysis(PmiTop100_OFile,Pmi20Appearances_OFile,collocationsFreqs,tokensFreqs):
    StartTime = time.clock()

    numOfTokens = sum(tokensFreqs.values())  # Total number of tokens in all the texts

    # For each colocation - give it a pmi and put it in a dictionary
    PmiScoreDic = dict()
    for collocation in collocationsFreqs: 
        # Get the frequencies and set the probabilities
        collocProb = collocationsFreqs[collocation] / numOfTokens
        word1Prob  = tokensFreqs[collocation.split()[0]] / numOfTokens
        word2Prob  = tokensFreqs[collocation.split()[1]] / numOfTokens

        PmiScore = math.log2(collocProb / (word1Prob * word2Prob))  # calculate the PMI score
        PmiScoreDic[collocation] = PmiScore                         # Push the PMI score 

    # List Top 100 PMI scores
    Top100Collocations = sorted(PmiScoreDic.items(),key=operator.itemgetter(0))             # Alphabetically sort
    Top100Collocations = sorted(Top100Collocations, key=lambda tup: tup[1],reverse=True)    # Sort by count
    Top100Collocations = Top100Collocations[0:100]                                          # Get only top 100 collocations
    
    # Output the top 100 PMI scores into PMI_raw.txt file
    PmiTop100_OFile.writelines((("%15d\t%30s\t%.10f " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(Top100Collocations)))
    PmiTop100_OFile.close()
    
    # List the collocations with exactly 20 appearances
    TwentyAppearances = []
    for Key,Value in collocationsFreqs.items():
        if Value == 20:
            TwentyAppearances.append((Key,PmiScoreDic[Key]))    
    TwentyAppearances.sort(key=operator.itemgetter(0))                  # Alphabetically sort
    TwentyAppearances.sort(key=operator.itemgetter(1),reverse= True)    # Sort by count

    # Output the collocations with exactly 20 appearances with their PMI score into PMI_select.txt file
    Pmi20Appearances_OFile.writelines((("%15d\t%30s\t%.10f " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(TwentyAppearances)))
    Pmi20Appearances_OFile.close()
    
    print("PmiAnalysis() (sec):\t\t" ,time.clock() - StartTime)
    return time.clock() - StartTime