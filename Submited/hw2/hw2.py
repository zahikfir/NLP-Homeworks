#********************** NLP **********************#
# H.W 2
# Haim Shalelashvily    200832780
# Zahi Kfir             200681476
#********************** NLP **********************#

import sys, os, codecs, re, time, math, operator
from collections import Counter

# When true - Filtering some UN-interesting collocations
#ImprovementsMode = True;  
ImprovementsMode = False;


# Input: list of input text streams 'txtFilesList'
# Output: 2 counted dictionaries: collocations and tokens 
def CountTokensAndCollocations(txtFilesList):
    StartTime = time.clock()

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
        f_Sentences = inputFile.split('\n')       # Split the text to sentences, (No collocation crosses two sentences)   
        for Sentence in f_Sentences:                    # Analyze each sentence separately 
            TokenList = Sentence.split()                # Split the sentence into tokens
            for Itr in range(0,len(TokenList)-1):       # Add all the sequential collocations to the dictionary 
                collocationsFreqs.update( [ TokenList[Itr] + " " + TokenList[Itr+1] ])
                
        inputFileStream.close()                         # close input file

    print("CountTokensAndCollocations() (sec):\t" ,time.clock() - StartTime)
    return (collocationsFreqs,tokensFreqs)


# Write the Raw Frequency analysis into the output files
# input: txtFilesList - texts to analyze
#        RfTop100_OFile / Rf20Appearances_OFile - output files
def RawFrequencyAnalysis(RfTop100_OFile,Rf20Appearances_OFile,collocationsFreqs,tokensFreqs):
    StartTime = time.clock()

    NumOfTokens = sum(tokensFreqs.values())  # Total number of tokens in all the texts
   
    # List Top 100 Raw Frequency scores
    Top100Collocations = sorted(collocationsFreqs.items(),key=operator.itemgetter(0))       # Alphabetically sort
    Top100Collocations = sorted(Top100Collocations, key=lambda tup: tup[1],reverse=True)    # Sort by count
    Top100Collocations = Top100Collocations[0:100]                                          # Get only top 100 collocations
    
    # Output the top 100 Raw Frequency scores into RawFrequency_raw.txt file
    RfTop100_OFile.writelines((("%15d\t%30s\t%.2f " + os.linesep) % (idx + 1, val[0], val[1]*1000/NumOfTokens ) for idx, val in enumerate(Top100Collocations)))
    RfTop100_OFile.close() 
    
    # List the collocations with exactly 20 appearances
    TwentyAppearances = []
    for (Key,Value) in collocationsFreqs.items():
        if Value == 20:
            TwentyAppearances.append((Key,Value))
    TwentyAppearances.sort(key=operator.itemgetter(0))                  # Alphabetically sort
    TwentyAppearances.sort(key=operator.itemgetter(1),reverse= True)    # Sort by count
    
    # Output the collocations with exactly 20 appearances with their Raw Frequency score into RawFrequency_select.txt file
    Rf20Appearances_OFile.writelines((("%15d\t%30s\t%.2f " + os.linesep) % (idx + 1, val[0], val[1]*1000/NumOfTokens ) for idx, val in enumerate(TwentyAppearances)))
    Rf20Appearances_OFile.close()
    
    print("RawFrequencyAnalysis() (sec):\t\t" ,time.clock() - StartTime)
    return (time.clock() - StartTime)


# Write the t-test analysis into the output files
# input: txtFilesList - texts to analyze
#        tTestTop100_OFile / tTest20Appearances_OFile - output files
def tTestAnalysis(tTestTop100_OFile,tTest20Appearances_OFile,collocationsFreqs,tokensFreqs):
    StartTime = time.clock()

    numOfTokens = sum(tokensFreqs.values())  # Total number of tokens in all the texts

    # for each colocation - give it a t-score and put it in a dictionary
    tScoreDic = dict()
    for collocation in collocationsFreqs:
        
        # get the frequencies and set the probabilities
        collocProb = collocationsFreqs[collocation] / numOfTokens
        word1Prob  = tokensFreqs[collocation.split()[0]] / numOfTokens
        word2Prob  = tokensFreqs[collocation.split()[1]] / numOfTokens

        # calculate the statistics
        meanOfDistributation = word1Prob * word2Prob

        # set the tscore
        if not collocProb == 0 : tScoreDic[collocation] = (collocProb - meanOfDistributation) / (math.sqrt(collocProb / numOfTokens))

    # List Top 100 t-test scores
    Top100Collocations = sorted(tScoreDic.items(),key=operator.itemgetter(0))               # Alphabetically sort
    Top100Collocations = sorted(Top100Collocations, key=lambda tup: tup[1],reverse=True)    # Sort by count
    Top100Collocations = Top100Collocations[0:100]                                          # Get only top 100 collocations

    # Output the top 100 tTest scores into tTest_raw.txt file
    tTestTop100_OFile.writelines((("%15d\t%30s\t%.2f " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(Top100Collocations)))
    tTestTop100_OFile.close() 
    
    # List the collocations with exactly 20 appearances
    TwentyAppearances = []
    for Key, Value in collocationsFreqs.items():
        if Value == 20:
            TwentyAppearances.append((Key,tScoreDic[Key]))
    TwentyAppearances.sort(key=operator.itemgetter(0))                  # Alphabetically sort
    TwentyAppearances.sort(key=operator.itemgetter(1),reverse= True)    # Sort by count

    # Output the collocations with exactly 20 appearances with their tTest score into tTest_select.txt file
    tTest20Appearances_OFile.writelines((("%15d\t%30s\t%.2f " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(TwentyAppearances)))
    tTest20Appearances_OFile.close()

    print("tTestAnalysis() (sec):\t\t\t" ,time.clock() - StartTime)
    return time.clock() - StartTime
   

# Write the PMI analysis into the output files
# input: txtFilesList - texts to analyze
#        PmiTop100_OFile / Pmi20Appearances_OFile - output files
def PmiAnalysis(PmiTop100_OFile,Pmi20Appearances_OFile,collocationsFreqs,tokensFreqs):
    StartTime = time.clock()

    numOfTokens = sum(tokensFreqs.values())  # Total number of tokens in all the texts

    # For each colocation - give it a pmi and put it in a dictionary
    PmiScoreDic = dict()
    for collocation in collocationsFreqs: 
        # Get the frequencies and set the probabilities
        collocProb = collocationsFreqs[collocation] / numOfTokens
        word1Prob  = tokensFreqs[collocation.split()[0]] / numOfTokens
        word2Prob  = tokensFreqs[collocation.split()[1]] / numOfTokens

        PmiScore = math.log2(collocProb / (word1Prob * word2Prob))  # calculate the PMI score
        PmiScoreDic[collocation] = PmiScore                         # Push the PMI score 

    # List Top 100 PMI scores
    Top100Collocations = sorted(PmiScoreDic.items(),key=operator.itemgetter(0))             # Alphabetically sort
    Top100Collocations = sorted(Top100Collocations, key=lambda tup: tup[1],reverse=True)    # Sort by count
    Top100Collocations = Top100Collocations[0:100]                                          # Get only top 100 collocations
    
    # Output the top 100 PMI scores into PMI_raw.txt file
    PmiTop100_OFile.writelines((("%15d\t%30s\t%.2f " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(Top100Collocations)))
    PmiTop100_OFile.close()
    
    # List the collocations with exactly 20 appearances
    TwentyAppearances = []
    for Key,Value in collocationsFreqs.items():
        if Value == 20:
            TwentyAppearances.append((Key,PmiScoreDic[Key]))    
    TwentyAppearances.sort(key=operator.itemgetter(0))                  # Alphabetically sort
    TwentyAppearances.sort(key=operator.itemgetter(1),reverse= True)    # Sort by count

    # Output the collocations with exactly 20 appearances with their PMI score into PMI_select.txt file
    Pmi20Appearances_OFile.writelines((("%15d\t%30s\t%.2f " + os.linesep) % (idx + 1, val[0], val[1] ) for idx, val in enumerate(TwentyAppearances)))
    Pmi20Appearances_OFile.close()
    
    print("PmiAnalysis() (sec):\t\t\t" ,time.clock() - StartTime)
    return time.clock() - StartTime


# Input: String 
# Output: True if string contains a digit
def ContainsDigit(InputString):
    for char in InputString:
        if char.isdigit():
            return True
    return False


# Input: String 
# Output: True if string contains a sign different than:  " ' .
def ContainSign(InputString):
    SpecialSign = [".","'",'"','-']
    for char in InputString:
        if not( char.isalpha() or (char in SpecialSign) ) :
            return True
    return False


# As CountTokensAndCollocations() + Filtering some UN-interesting collocations 
# Filtering: 
#   1. collocations that one or more token contains a sign.         e.g. Dog(
#   2. collocations that one or more token contains a number.       e.g. since 1989
#   3. collocations that one or more token length is less then 2.   e.g. since - 
def CountTokensAndCollocations_Improved(txtFilesList):
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
                # Filter tokens that contains a sign
                if not( ContainSign(TokenList[Itr]) or ContainSign(TokenList[Itr+1]) ):
                    # Filter tokens that contains a digit
                    if not( ContainsDigit(TokenList[Itr]) or ContainsDigit(TokenList[Itr+1]) ):
                        # Filter tokens with length < 2
                        if not ( (len(TokenList[Itr]) < 2) or (len(TokenList[Itr+1]) < 2) ):
                            collocationsFreqs.update( [ TokenList[Itr] + " " + TokenList[Itr+1] ])
                
        inputFileStream.close()                         # close input file

    print("CountTokensAndCollocations_Improved() (sec):\t\t" ,time.clock() - StartTime)
    return (collocationsFreqs,tokensFreqs)



StartTime = time.clock()

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
if not(ImprovementsMode):
    (collocationsFreqs,tokensFreqs) = CountTokensAndCollocations(txtFilesList)
else:
    (collocationsFreqs,tokensFreqs) = CountTokensAndCollocations_Improved(txtFilesList)
 
# Print the Raw-frequency/T-Test/PMI score into the output files
RawFrequencyAnalysis(RfTop100_OFile,Rf20Appearances_OFile,collocationsFreqs,tokensFreqs)    # Raw Frequency 
tTestAnalysis(tTestTop100_OFile,tTest20Appearances_OFile,collocationsFreqs,tokensFreqs)     # t-test 
if not(ImprovementsMode):
    PmiAnalysis(PmiTop100_OFile,Pmi20Appearances_OFile,collocationsFreqs,tokensFreqs)       # PMI 
else:
    # Remove the collocations with less than 4 appearances
    ToRemove = []
    for (Key,Value) in collocationsFreqs.items():
        if Value < 4:
            ToRemove.append(Key)
    for Key in ToRemove:
        collocationsFreqs.pop(Key)
    PmiAnalysis(PmiTop100_OFile,Pmi20Appearances_OFile,collocationsFreqs,tokensFreqs)       # PMI   

print("Total Time (sec):\t\t\t" ,time.clock() - StartTime)