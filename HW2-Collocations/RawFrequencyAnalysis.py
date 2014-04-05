
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
        inputFile = inputFileStream.read()
        
        # Split the text to sentences, (No collocation crosses two sentences)
        f_Sentences = inputFile.split('\r\n')
        
        for Sentence in f_Sentences:
            TokenList = Sentence.split()

        #for Sentence in f_Sentences:
        #    RF_Raw_outStream.write(Sentence)
        #    RF_Raw_outStream.write("\r\n")

        #RF_Raw_outStream.write("*********************************************************************")
        #RF_Raw_outStream.write("\r\n")

    RF_Raw_outStream.close();

    return 'Done'
