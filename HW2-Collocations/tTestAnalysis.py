
import sys, os, codecs, re, time

# t-test analysis
# input: txtFilesList - texts to analyze
#        tTest_Raw_outStream / tTest_Select_outStream - output files
def tTestAnalysis(txtFilesList,tTest_Raw_outStream,tTest_Select_outStream):
    
    # Analysis each text  
    for f in txtFilesList:
        print("t-test analysis " + f + " :")
    
    # open the input file
    inputFileStream  = codecs.open(f,"r","utf-8")
    
    return 'Done'