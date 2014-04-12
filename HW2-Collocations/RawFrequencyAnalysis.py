
import sys, os, codecs, re, time, math, operator

# Raw Frequency analysis
# input: txtFilesList - texts to analyze
#        RfTop100_OFile / Rf20Appearances_OFile - output files
def RawFrequencyAnalysis(RfTop100_OFile,Rf20Appearances_OFile,collocationsFreqs,tokensFreqs):
    StartTime = time.clock()

    NumOfTokens = sum(tokensFreqs.values())  # Total number of tokens in all the texts
   
    collocationsFreqs = sorted(collocationsFreqs.items(),key=operator.itemgetter(0))    # Alphabetically sort
    collocationsFreqs = sorted(collocationsFreqs, key=lambda tup: tup[1],reverse=True)  # Sort by count
    
    # Output the top 100 Raw Frequency scores into RawFrequency_raw.txt file
    Top100Collocations = collocationsFreqs[0:100]    # Get the top 100 collocations
    RfTop100_OFile.writelines((("%15d\t%30s\t%f " + os.linesep) % (idx + 1, val[0], val[1]*1000/NumOfTokens ) for idx, val in enumerate(Top100Collocations)))
    RfTop100_OFile.close() 
    
    # List the collocations with exactly 20 appearances
    TwentyAppearances = []
    for (Key,Value) in collocationsFreqs:
        if Value == 20:
            TwentyAppearances.append((Key,Value))

    # Output the collocations with exactly 20 appearances with their Raw Frequency score into RawFrequency_select.txt file
    Rf20Appearances_OFile.writelines((("%15d\t%30s\t%f " + os.linesep) % (idx + 1, val[0], val[1]*1000/NumOfTokens ) for idx, val in enumerate(TwentyAppearances)))
    Rf20Appearances_OFile.close()
    
    print("RawFrequencyAnalysis() (sec):\t\t" ,time.clock() - StartTime)
    return (time.clock() - StartTime)
