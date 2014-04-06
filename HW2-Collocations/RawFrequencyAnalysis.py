
import sys, os, codecs, re, time

# Raw Frequency analysis
# input: txtFilesList - texts to analyze
#        RF_Raw_outStream / RF_Select_outStream - output files
def RawFrequencyAnalysis(txtFilesList,RF_Raw_outStream,RF_Select_outStream):
    
    # Analysis each text  
    for f in txtFilesList:
        print("Raw Frequency analysis " + f + " :")

        # Creating a counted dictionary
        from collections import Counter
        Collocations_CountedDictionary = Counter()
        
        # open the input file
        inputFileStream  = codecs.open(f,"r","utf-8")
        inputFile = inputFileStream.read()
        inputFile = inputFile.lower()       # when using english we want "Open minded" to be equal to "open minded"

        # Split the text to sentences, (No collocation crosses two sentences)
        f_Sentences = inputFile.split(os.linesep)

        # close input file 
        inputFileStream.close()

        # Analyze each sentence separately 
        for Sentence in f_Sentences: 
            
            # Split the sentence into tokens
            TokenList = Sentence.split()    

            # Add all the sequential collocations to the dictionary 
            for Itr in range(0,len(TokenList)-1):
                Collocations_CountedDictionary.update( [ TokenList[Itr] + " " + TokenList[Itr+1] ])
   
    # Get the top 100 collocations
    Top100Collocations = Collocations_CountedDictionary.most_common(100)

    # Output the top 100 Raw Frequency scores into RawFrequency_raw.txt file
    RF_Raw_outStream.writelines((("%15d\t%30s\t%f " + os.linesep) % (idx + 1, val[0], val[1]*1000/len(Collocations_CountedDictionary) ) for idx, val in enumerate(Top100Collocations)))
    RF_Raw_outStream.close() 
    
    # List the collocations with exactly 20 appearances
    TwentyAppearances = []
    for Key, Value in Collocations_CountedDictionary.items():
        if Value == 20:
            TwentyAppearances.append((Key,Value))

    # Output the collocations with exactly 20 appearances with their Raw Frequency score into RawFrequency_select.txt file
    RF_Select_outStream.writelines((("%15d\t%30s\t%f " + os.linesep) % (idx + 1, val[0], val[1]*1000/len(Collocations_CountedDictionary) ) for idx, val in enumerate(TwentyAppearances)))
    RF_Select_outStream.close()


    # TODO
    # .most_common(100) is random when equally appear  (sort it Alpha-Beth)
    
    return Collocations_CountedDictionary
