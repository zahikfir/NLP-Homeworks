
import sys, os, codecs, re, time

# PMI analysis
# input: txtFilesList - texts to analyze
#        PMI_Raw_outStream / PMI_Select_outStream - output files
def PmiAnalysis(txtFilesList,PMI_Raw_outStream,PMI_Select_outStream,collocationsFreqs,tokensFreqs):
    
    # Analysis each text  
    for f in txtFilesList:
        print("PMI analysis " + f + " :")
           
        # open the input file
        inputFileStream  = codecs.open(f,"r","utf-8")



        # get the number of tokens in all the corpus
        numOfTokens = sum(tokensFreqs.values())
    
    return 'Done'