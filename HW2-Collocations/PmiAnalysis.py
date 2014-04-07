
import sys, os, codecs, re, time, math, operator

# PMI analysis
# input: txtFilesList - texts to analyze
#        PMI_Raw_outStream / PMI_Select_outStream - output files
def PmiAnalysis(PMI_Raw_outStream,PMI_Select_outStream,collocationsFreqs,tokensFreqs):
    StartTime = time.clock()

    # Get the number of tokens in all the corpus
    numOfTokens = sum(tokensFreqs.values())
     
    # For each colocation - give it a pmi and put it in a dictionary
    PmiScoreDic = dict()
    for collocation in collocationsFreqs:
        
        # Get the frequencies and set the probabilities
        collocProb = collocationsFreqs[collocation] / numOfTokens
        word1Prob  = tokensFreqs[collocation.split()[0]] / numOfTokens
        word2Prob  = tokensFreqs[collocation.split()[1]] / numOfTokens

        # calculate the PMI score
        PmiScore = math.log2(collocProb / (word1Prob * word2Prob))

        # Push the PMI score 
        PmiScoreDic[collocation] = PmiScore

    # Get the top 100 PMI scores collocations
    Top100Collocations = sorted(PmiScoreDic.items(), key=operator.itemgetter(1),reverse=True)[0:100]
       
    # Output the top 100 PMI scores into PMI_raw.txt file
    PMI_Raw_outStream.writelines((("%15d\t%30s\t%f " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(Top100Collocations)))
    PMI_Raw_outStream.close()
    
    # List the collocations with exactly 20 appearances
    TwentyAppearances = []
    for Key, Value in collocationsFreqs.items():
        if Value == 20:
            TwentyAppearances.append((Key,PmiScoreDic[Key]))  

    # Sort the collocations with exactly 20 appearances by the PMI score
    TwentyAppearances.sort(key=operator.itemgetter(1),reverse= True)

    # Output the collocations with exactly 20 appearances with their PMI score into PMI_select.txt file
    PMI_Select_outStream.writelines((("%15d\t%30s\t%f " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(TwentyAppearances)))
    PMI_Select_outStream.close()
    
    print("PmiAnalysis() (sec):\t\t" ,time.clock() - StartTime)
    return 'Done'