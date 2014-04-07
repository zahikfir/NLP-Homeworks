
import sys, os, codecs, re, time

# Raw Frequency analysis
# input: txtFilesList - texts to analyze
#        RF_Raw_outStream / RF_Select_outStream - output files
def RawFrequencyAnalysis(txtFilesList,RF_Raw_outStream,RF_Select_outStream):
    
    from collections import Counter         # Class for creating a counted dictionary
    tokensFreqs = Counter()                 # For token counting 
    collocationsFreqs = Counter()           # For collocation counting
    
    # Analyze each text  
    for f in txtFilesList:
        print("Raw Frequency analysis " + f + " :")
       
        # open the input file
        inputFileStream  = codecs.open(f,"r","utf-8")
        inputFile = inputFileStream.read()
        inputFile = inputFile.lower()                   # when using english we want "Open minded" to be equal to "open minded"
              
        # Count all collocation
        f_Sentences = inputFile.split(os.linesep)       # Split the text to sentences, (No collocation crosses two sentences)   
        for Sentence in f_Sentences:                    # Analyze each sentence separately 
            TokenList = Sentence.split()                # Split the sentence into tokens
            for Itr in range(0,len(TokenList)-1):       # Add all the sequential collocations to the dictionary 
                collocationsFreqs.update( [ TokenList[Itr] + " " + TokenList[Itr+1] ])
        
        tokensFreqs.update(Counter(inputFile.split()))  # Count all tokens
        inputFileStream.close()                         # close input file 
    
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
    
    return (collocationsFreqs,tokensFreqs)
