
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
        f_Sentences = inputFile.split('\r\n')
        
        # Analyze each sentence separately 
        for Sentence in f_Sentences: 
            
            # Split the sentence into tokens
            TokenList = Sentence.split()    

            # Add all the sequential collocations to the dictionary 
            for Itr in range(0,len(TokenList)-1):
                Collocations_CountedDictionary.update( [ TokenList[Itr] + " " + TokenList[Itr+1] ])
   
    # Sort the dictionary
    Collocations_CountedDictionary = Collocations_CountedDictionary.most_common()

    return 'Done'
