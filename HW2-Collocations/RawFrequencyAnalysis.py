
import sys, os, codecs, re, time

# Raw Frequency analysis
# input: txtFilesList - texts to analyze
#        RF_Raw_outStream / RF_Select_outStream - output files
def RawFrequencyAnalysis(txtFilesList,RF_Raw_outStream,RF_Select_outStream):
    
    # Analysis each text  
    for f in txtFilesList:
        print("Raw Frequency analysis " + f + " :")
    
    # open the input file
    inputFileStream  = codecs.open(f,"r","utf-8")
    
    return 'Done'