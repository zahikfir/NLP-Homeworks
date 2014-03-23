
import sys, os, codecs,time

currentDir = sys.argv[1]

def SeparateTokens(text, Tokens):
    TokonsList = []
    LastIndex = 0;
    Index = 0;

    StartTime = time.clock()
    while Index < (len(text)):
        if text[Index] in Tokens:
            if Index-1 >= 0:
                if text[Index-1] != ' ':
                    TokonsList.append(text[LastIndex:Index])                   
                    LastIndex = Index
            if Index+1 < len(text):
                if text[Index+1] != ' ': 
                    TokonsList.append(text[LastIndex:Index+1])             
                    LastIndex = Index+1
        Index = Index+1
    print("\t\t Splited in ",time.clock() - StartTime," sec")
    TokonsList.append(text[LastIndex:])                
    return " ".join(TokonsList)


Tokens = ["." , "!" , "?" , "," , ":" , ";" ,"'" , '"' , '<' , '>' , '@' , '#', '$' , '%' , '^' , '&' , '*' , '(' , ')' , '+', '=', '[' , ']' , '{' , '}' , "/" , "\\" , '_' , '~' ]

txtFilesList = [ os.path.join(currentDir, f) for f in os.listdir(currentDir) if (os.path.isfile(os.path.join(currentDir, f)) & str(f).endswith("_sentences.txt"))]

print("Seperating tokens:" ) 
for f in txtFilesList:
    print("\t Processing " + f) 
    StartTime = time.clock()

    # open the input file and create an output file
    inputFileStream  = codecs.open(f,"r","utf-8")
    outputFileStream = codecs.open(f[0:(f.rfind("_sentences.txt"))] + ".out.txt" , "w", "utf-8")

    #read the text and seperate tokens
    outputFileStream.writelines((SeparateTokens(inputFileStream.read(), Tokens)))

    print("\t\t Done in ",time.clock() - StartTime," sec")


