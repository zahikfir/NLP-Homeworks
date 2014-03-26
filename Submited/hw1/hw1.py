#********************** NLP **********************#
# H.W 1
# Haim Shalelashvily    200832780
# Zahi Kfir             200681476
#********************** NLP **********************#

import sys, os, codecs, re, time

# replace every linefid symbol with closeRowLineFid symbols (support multiple text editors)
def ReplaceLFwithCRLF(text):
    # most text have only line fid symbol - change it to closeRowLineFid symbol to support multiple text editors
    text = str(text).replace("\n","\r\n")
    # if we had already a closeLine symbol we will no have two closeLines symbols togther. Remove one 
    return str(text).replace("\r\r","\r")

# split a text to sentences using the given delimiters list
def SplitTextToSentences(text, delimiters):
    # replace all the line fid characters to CloseRowLineFid symbols
    text = ReplaceLFwithCRLF(text)

    # get an iterator to all the occurances of the delimiters and their concataneted regular expressions , also the one that ends with double quotes
    ReResult = re.finditer("[" + ''.join(delimiters) + "][" + ''.join(delimiters) + "]*(\")*",text)

    # add new line fid after every occurance
    SentencesList = []
    LastIndex = 0;
    for iter in ReResult:
        # get the index of the end of the regular expression
        currentEndingIndex = iter.regs[0][1] 
        # check if we found a fraction. format : digit*.digit*
        if (text[currentEndingIndex-1]=="." and currentEndingIndex>1 and text[currentEndingIndex].isdigit() and text[currentEndingIndex-2].isdigit()):
            # in this case we don't need to add a line fid , we just found a number
            continue
        # check if we found a fullstop mark inside a ward. format : alpha.alpha
        if (text[currentEndingIndex-1]=="." and currentEndingIndex>1 and text[currentEndingIndex].isalpha() and text[currentEndingIndex-2].isalpha()):
            # in this case we don't need to add a line fid
            continue
        # add the current sentences to the sentences list
        SentencesList.append(text[LastIndex:currentEndingIndex])
        # update the last handled index
        LastIndex = currentEndingIndex

    # add the last sentence if available
    SentencesList.append(text[LastIndex:])
    # concatenate all the sentences by adding the CloseRowLineFid between them
    text = "\r\n".join(SentencesList)
    # return an array of non empty sentences ( Remove also the old closeLineLineFid symbols)
    return [str(sentence) for sentence in text.split("\r\n") if ((not str(sentence).isspace()) and len(sentence) > 0)]


def SeparateTokens(text):   
    # Always add spaces before and after this tokens
    SimpleSeparators = ["." , "!" , "?" , "," , ":" , ";" , '<' , '>' , '@' , '#', '$' , '%' , '^' , '&' , '*' , '(' , ')' , '+', '=', '[' , ']' , '{' , '}' , "/" , "\\" , '_' , '~',"-","'" ,'"' ]

    # Add spaces before and after this tokens only when not between 2 letters (???"? ?'?? ??-?????)
    SpecialSeparators = ["-","'" , '"']
    
    # Add spaces before and after this tokens only when not between 2 Digits (1,000,000 5.2)
    SpecialDigitSeparators = [".",",","/"]

    # Holds separated tokens
    TokonsList = []

    # The last char index that was checked
    LastCheckedIndex = 0;

    # Check the first character
    if (text[0] in SimpleSeparators):
        if text[1] != ' ': 
            TokonsList.append(text[0])             
            LastCheckedIndex = 1

    # loop each character,Except the first and last character, searching for separator tokens
    Index = 1;
    StartTime = time.clock()
    while Index < (len(text)-1):
        if not( (text[Index] in SpecialSeparators) and  (text[Index-1].isalpha()) and (text[Index+1].isalpha()) ):    # leave ' " - when in a word
            if not( (text[Index] in SpecialDigitSeparators) and  (text[Index-1].isdigit()) and (text[Index+1].isdigit()) ): # leave . , when in a digit
                if text[Index] in SimpleSeparators:
                    if (text[Index-1] != ' ') and (not(text[Index-1] in SimpleSeparators)):
                        TokonsList.append(text[LastCheckedIndex:Index])                   
                        LastCheckedIndex = Index
                    if text[Index+1] != ' ': 
                        TokonsList.append(text[LastCheckedIndex:Index+1])             
                        LastCheckedIndex = Index+1
        Index = Index+1
 
    # Check the last character
    if (text[-1] in SimpleSeparators) and text[-2] != ' ':
        TokonsList.append(text[LastCheckedIndex:-1])    
        TokonsList.append(text[-1])             
    else:
        TokonsList.append(text[LastCheckedIndex:])
    
    print("\t\t Splited in ",time.clock() - StartTime," sec")
    return " ".join(TokonsList)



#get the command line argument
if len(sys.argv) < 2: sys.exit("Please enter a data directory path")
currentDir = sys.argv[1]
print("The data folder is: " + currentDir)


# Section 1:
# get all the txt file paths from the given data directory
txtFilesList = [ os.path.join(currentDir, f) for f in os.listdir(currentDir) if (os.path.isfile(os.path.join(currentDir, f)) & str(f).endswith(".txt"))]

# set the list of line ending delimiters
lineEndingDelimiters = [".","!","?"]

# seperate each text to sentences 
for f in txtFilesList:
    print("Seperating " + f + " to sentences")
    
    # open the input file and create an output file
    inputFileStream  = codecs.open(f,"r","utf-8")
    outputFileStream = codecs.open(f[0:(f.rfind(".txt"))] + "_sentences.txt" , "w", "utf-8")

    #read the text and split it by the line ending delimiters
    listOfSentences = SplitTextToSentences(inputFileStream.read(), lineEndingDelimiters)
    outputFileStream.writelines(("%s\r\n" % l for l in listOfSentences))
    outputFileStream.close()


# section 2:
txtFilesList = [ os.path.join(currentDir, f) for f in os.listdir(currentDir) if (os.path.isfile(os.path.join(currentDir, f)) & str(f).endswith("_sentences.txt"))]

print("Seperating tokens:" ) 
for f in txtFilesList:
    print("\t Processing " + f) 
    StartTime = time.clock()

    # open the input file and create an output file
    inputFileStream  = codecs.open(f,"r","utf-8")
    outputFileStream = codecs.open(f[0:(f.rfind("_sentences.txt"))] + ".out.txt" , "w", "utf-8")

    #read the text and seperate tokens
    outputFileStream.writelines((SeparateTokens(inputFileStream.read())))
    outputFileStream.close()

    print("\t\t Done in ",time.clock() - StartTime," sec")

# section 3:
# get all the txt file paths from the given data directory
txtFilesList = [ os.path.join(currentDir, f) for f in os.listdir(currentDir) if (os.path.isfile(os.path.join(currentDir, f)) & str(f).endswith(".out.txt"))]

# class for creating a counted dictionary
from collections import Counter
globalFreqs = Counter()

for f in txtFilesList:
    print("Creating a frequency list of file :  " + f)
    
    # open the input file
    inputFileStream  = codecs.open(f,"r","utf-8")
    
    # add the dictionary of words of the current text file to the global freq dictionary
    globalFreqs.update(Counter(inputFileStream.read().split()))

# sort the dictionary from high freq to low
globalFreqs = globalFreqs.most_common()

# output the freqs table to the output file
outputFileStream = codecs.open(currentDir + "\\freqlist.txt" , "w", "utf-8")
outputFileStream.writelines(("%15d\t%15s\t%15d \r\n" % (idx + 1, val[0], val[1]) for idx, val in enumerate(globalFreqs)))
outputFileStream.close()

