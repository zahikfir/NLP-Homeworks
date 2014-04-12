
import sys, os, codecs, re, time, math, operator

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

# Input: list of input text streams 'txtFilesList'
# Output: 2 counted dictionaries: collocations and tokens 
def CountTokensAndCollocations(txtFilesList):
    StartTime = time.clock()

    UninterestingTokens = ["." , "!" , "?" , "," , ":" , ";" , '<' , '>' , '@' , '#', '$' , '%' , '^' , '&' , '*' , '(' , ')' , '+', '=', '[' , ']' , '{' , '}' , "/" , "\\" , '_' , '~',"-","'" ,'"' ]

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
                if not( ContainSign(TokenList[Itr]) or ContainSign(TokenList[Itr+1]) ):
                    if not( ContainsDigit(TokenList[Itr]) or ContainsDigit(TokenList[Itr+1]) ):
                        if not ( (len(TokenList[Itr]) < 2) or (len(TokenList[Itr+1]) < 2) ):
                            collocationsFreqs.update( [ TokenList[Itr] + " " + TokenList[Itr+1] ])
                
        inputFileStream.close()                         # close input file

    print("Run CountTokensAndCollocations() (sec):\t\t" ,time.clock() - StartTime)
    return (collocationsFreqs,tokensFreqs)