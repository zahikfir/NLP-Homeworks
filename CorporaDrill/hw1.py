import sys, os, codecs, re

# replace every linefid symbol with closeRowLineFid symbols (support multiple text editors)
def ReplaceLFwithCRLF(text):
    return str(text).replace("\n","\r\n")

# split a text to sentences using the given delimiters list
def SplitTextToSentences(text, delimiters):
    
    text = ReplaceLFwithCRLF(text)

    # get an iterator to all the occurances of the delimiters and their concataneted regular expressions , also the one that ends with double quates
    ReResult = re.finditer("[" + ''.join(delimiters) + "][" + ''.join(delimiters) + "]*(\")*",text)

    # add new line fid after every occurance
    SentencesList = []
    LastIndex = 0;
    for iter in ReResult:

        currentEndingIndex = iter.regs[0][1] 
        # check for a number from format : digits.digits
        if (text[currentEndingIndex-1]=="." and currentEndingIndex>1 and text[currentEndingIndex].isdigit() and text[currentEndingIndex-2].isdigit()):
            # in this case we don't need to add a lie fid
            continue
        SentencesList.append(text[LastIndex:currentEndingIndex])
        LastIndex = currentEndingIndex

    text = "\r\n".join(SentencesList)
   
    # return an array of non empty sentences
    return [str(sentence) for sentence in text.split("\r\n") if ((not str(sentence).isspace()) and len(sentence) > 0)]

#get the command line argument
if len(sys.argv) < 2: sys.exit("Please enter a data directory path")
currentDir = sys.argv[1]
print("The data folder is: " + currentDir)

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
    splitedText = SplitTextToSentences(inputFileStream.read(), lineEndingDelimiters)
    outputFileStream.writelines(("%s\r\n" % l for l in splitedText))

# do section 2
import hw1_Q2

# do section 3
import hw1_Q3