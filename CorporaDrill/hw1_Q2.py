
import sys, os, codecs,time

currentDir = sys.argv[1]

def SeparateTokens1(text, Tokens):
    SeperatedText = str(text)
    Index = 0;
    while Index < (len(SeperatedText)):
        if SeperatedText[Index] in Tokens:
            if Index-1 >= 0:
                if SeperatedText[Index-1] != ' ':
                    SeperatedText = SeperatedText[:Index] + ' ' + SeperatedText[Index:]
                    Index = Index+1
            if Index+1 < len(SeperatedText):
                if SeperatedText[Index+1] != ' ': 
                    SeperatedText = SeperatedText[:Index+1] + ' ' + SeperatedText[Index+1:]
                    Index = Index+1
        Index = Index+1
    return SeperatedText


def SeparateTokens2(text, Tokens):
    FindIndexesStartTime = time.clock()
    SpacesIndexList = []
    Index = 0;
    while Index < (len(text)):
        if text[Index] in Tokens:
            if Index-1 >= 0:
                if text[Index-1] != ' ':
                    SpacesIndexList.append(Index)
            if Index+1 < len(text):
                if text[Index+1] != ' ': 
                    SpacesIndexList.append(Index+1)                  
        Index = Index+1
    print("\t\t Found Indexes in ",time.clock() - StartTime," sec")

    LastIndex = 0;
    SeperatedText = ""
    for i in SpacesIndexList:
        SeperatedText = SeperatedText + text[LastIndex:i] + ' '
        LastIndex = i
    SeperatedText = SeperatedText + text[LastIndex:]

    return SeperatedText


Tokens = [".","!","?",",",":",";","'",'"']

txtFilesList = [ os.path.join(currentDir, f) for f in os.listdir(currentDir) if (os.path.isfile(os.path.join(currentDir, f)) & str(f).endswith("_sentences.txt"))]

print("Seperating tokens in using SeparateTokens1:" ) 
for f in txtFilesList:
    print("\t Processing " + f) 
    StartTime = time.clock()

    # open the input file and create an output file
    inputFileStream  = codecs.open(f,"r","utf-8")
    outputFileStream = codecs.open(f[0:(f.rfind("_sentences.txt"))] + ".out.txt" , "w", "utf-8")

    #read the text and seperate tokens
    outputFileStream.writelines((SeparateTokens1(inputFileStream.read(), Tokens)))

    print("\t\t Done in ",time.clock() - StartTime," sec")


print("Seperating tokens in using SeparateTokens2:" ) 
for f in txtFilesList:
    print("\t Processing " + f) 
    StartTime = time.clock()

    # open the input file and create an output file
    inputFileStream  = codecs.open(f,"r","utf-8")
    outputFileStream = codecs.open(f[0:(f.rfind("_sentences.txt"))] + ".out.txt" , "w", "utf-8")

    #read the text and seperate tokens
    outputFileStream.writelines((SeparateTokens2(inputFileStream.read(), Tokens)))

    print("\t\t Done in ",time.clock() - StartTime," sec")