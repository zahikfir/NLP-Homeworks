
import sys, os, codecs, re, time

# Raw Frequency analysis
# input: txtFilesList - texts to analyze
#        RF_Raw_outStream / RF_Select_outStream - output files
def RawFrequencyAnalysis(RF_Raw_outStream,RF_Select_outStream,collocationsFreqs,tokensFreqs):
    StartTime = time.clock()
   
    # get the number of tokens in all the corpus
    NumOfTokens = sum(tokensFreqs.values())

    # Output the top 100 Raw Frequency scores into RawFrequency_raw.txt file
    Top100Collocations = collocationsFreqs.most_common(100)    # Get the top 100 collocations
    RF_Raw_outStream.writelines((("%15d\t%30s\t%f " + os.linesep) % (idx + 1, val[0], val[1]*1000/NumOfTokens ) for idx, val in enumerate(Top100Collocations)))
    RF_Raw_outStream.close() 
    
    # List the collocations with exactly 20 appearances
    TwentyAppearances = []
    for Key, Value in collocationsFreqs.items():
        if Value == 20:
            TwentyAppearances.append((Key,Value))

    # Output the collocations with exactly 20 appearances with their Raw Frequency score into RawFrequency_select.txt file
    RF_Select_outStream.writelines((("%15d\t%30s\t%f " + os.linesep) % (idx + 1, val[0], val[1]*1000/NumOfTokens ) for idx, val in enumerate(TwentyAppearances)))
    RF_Select_outStream.close()

    # TODO
    # .most_common(100) is random when equally appear  (sort it Alpha-Beth)
    
    print("RawFrequencyAnalysis() (sec):\t\t" ,time.clock() - StartTime)
    return (collocationsFreqs,tokensFreqs)
