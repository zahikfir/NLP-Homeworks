import sys, os, codecs

# split a text to sentences using the given delimiters list
def SplitTextToSentences(text, delimiters):
    
    # for each delimiter in the delimiters list
    for delimiter in delimiters:
        # replace every occurance of the delimiter with a line ending char
        text = str(text).replace(delimiter, delimiter + "\r\n")
   
    # return an arrat of sentences
    return text.split("\r\n")

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
    outputFileStream.writelines(("%s\r\n" % l for l in SplitTextToSentences(inputFileStream.read(), lineEndingDelimiters)))