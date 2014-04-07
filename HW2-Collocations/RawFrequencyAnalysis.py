
import sys, os, codecs, re, time, math, operator

# Raw Frequency analysis
# input: txtFilesList - texts to analyze
#        RawFrequencyTop100 / RawFrequency20Appearances - output files
def RawFrequencyAnalysis(RawFrequencyTop100,RawFrequency20Appearances,collocationsFreqs,tokensFreqs):
    StartTime = time.clock()
   
    # get the number of tokens in all the corpus
    NumOfTokens = sum(tokensFreqs.values())

    # Output the top 100 Raw Frequency scores into RawFrequency_raw.txt file
    Top100Collocations = collocationsFreqs.most_common(100)    # Get the top 100 collocations
    RawFrequencyTop100.writelines((("%15d\t%30s\t%f " + os.linesep) % (idx + 1, val[0], val[1]*1000/NumOfTokens ) for idx, val in enumerate(Top100Collocations)))
    RawFrequencyTop100.close() 
    
    # List the collocations with exactly 20 appearances
    TwentyAppearances = []
    for Key, Value in collocationsFreqs.items():
        if Value == 20:
            TwentyAppearances.append((Key,Value))

    # Output the collocations with exactly 20 appearances with their Raw Frequency score into RawFrequency_select.txt file
    RawFrequency20Appearances.writelines((("%15d\t%30s\t%f " + os.linesep) % (idx + 1, val[0], val[1]*1000/NumOfTokens ) for idx, val in enumerate(TwentyAppearances)))
    RawFrequency20Appearances.close()

    # TODO
    # .most_common(100) is random when equally appear  (sort it Alpha-Beth)
    
    print("RawFrequencyAnalysis() (sec):\t\t" ,time.clock() - StartTime)
    return (collocationsFreqs,tokensFreqs)
