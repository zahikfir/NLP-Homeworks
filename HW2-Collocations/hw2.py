#********************** NLP **********************#
# H.W 2
# Haim Shalelashvily    200832780
# Zahi Kfir             200681476
#********************** NLP **********************#

import sys, os, codecs, re, time, math, operator
from collections import Counter

# Input: list of input text streams 'txtFilesList'
# Output: 2 counted dictionaries: collocations and tokens 
def CountTokensAndCollocations(txtFilesList):
    StartTime = time.clock()

    from collections import Counter         # Class for creating a counted dictionary
    tokensFreqs = Counter()                 # For token counting 
    collocationsFreqs = Counter()           # For collocation counting
    
    # Analyze each text  
    for f in txtFilesList:     
        # open the input file
        inputFileStream  = codecs.open(f,"r","utf-8")
        inputFile = inputFileStream.read()
        inputFile = inputFile.lower()                   # when using english we want "Open minded" to be equal to "open minded"
              
        tokensFreqs.update(Counter(inputFile.split()))  # Count all tokens

        # Count all collocation
        f_Sentences = inputFile.split(os.linesep)       # Split the text to sentences, (No collocation crosses two sentences)   
        for Sentence in f_Sentences:                    # Analyze each sentence separately 
            TokenList = Sentence.split()                # Split the sentence into tokens
            for Itr in range(0,len(TokenList)-1):       # Add all the sequential collocations to the dictionary 
                collocationsFreqs.update( [ TokenList[Itr] + " " + TokenList[Itr+1] ])
                
        inputFileStream.close()                         # close input file
    print("Run CountTokensAndCollocations() (sec):\t\t" ,time.clock() - StartTime)
    return (collocationsFreqs,tokensFreqs)

# Get the command line argument
if len(sys.argv) < 3: sys.exit("Please enter a data directory path and an output folder path")
currentDir = sys.argv[1]
outputDir = sys.argv[2]
print("The data folder is: " + currentDir)
print("The output folder is: " + outputDir)

# Get all the txt file paths from the given data directory
txtFilesList = [ os.path.join(currentDir, f) for f in os.listdir(currentDir) if (os.path.isfile(os.path.join(currentDir, f)) & str(f).endswith(".txt"))]

# Ensure that that the output directory exists (create if necessary)
if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    
# Create the output files (OFile) 
RfTop100_OFile = codecs.open(os.path.join(outputDir, "RawFrequency_raw.txt"), "w", "utf-8")                 # Raw Frequency top 100
Rf20Appearances_OFile = codecs.open(os.path.join(outputDir, "RawFrequency_select.txt"), "w", "utf-8")       # Raw exactly 20 appearances
tTestTop100_OFile = codecs.open(os.path.join(outputDir, "tTest_raw.txt"), "w", "utf-8")                     # t-test top 100
tTest20Appearances_OFile = codecs.open(os.path.join(outputDir, "tTest_select.txt"), "w", "utf-8")           # t-test exactly 20 appearances
PmiTop100_OFile = codecs.open(os.path.join(outputDir, "PMI_raw.txt"), "w", "utf-8")                         # PMI top 100
Pmi20Appearances_OFile = codecs.open(os.path.join(outputDir, "PMI_select.txt"), "w", "utf-8")               # PMI exactly 20 appearances

# Count tokens and collocations
(collocationsFreqs,tokensFreqs) = CountTokensAndCollocations(txtFilesList)



# Run Raw Frequency analysis
import RawFrequencyAnalysis
RawFrequencyAnalysis.RawFrequencyAnalysis(RfTop100_OFile,Rf20Appearances_OFile,collocationsFreqs,tokensFreqs)

# Run t-test analysis
import tTestAnalysis
tokensFreqs = tTestAnalysis.tTestAnalysis(tTestTop100_OFile,tTest20Appearances_OFile,collocationsFreqs,tokensFreqs)

# Run PMI analysis
import PmiAnalysis
PmiAnalysis.PmiAnalysis(PmiTop100_OFile,Pmi20Appearances_OFile,collocationsFreqs,tokensFreqs)


sys.stdin.read(1)


