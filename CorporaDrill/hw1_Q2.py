
import sys, os, codecs,time

currentDir = sys.argv[1]

def SeparateTokens(text):   
    # Always add spaces before and after this tokens
    SimpleSeparators = ["." , "!" , "?" , "," , ":" , ";" , '<' , '>' , '@' , '#', '$' , '%' , '^' , '&' , '*' , '(' , ')' , '+', '=', '[' , ']' , '{' , '}' , "/" , "\\" , '_' , '~',"-","'" ,'"' ]

    # Add spaces before and after this tokens only when not between 2 letters (???"? ?'?? ??-?????)
    SpecialSeparators = ["-","'" , '"']
    
    # Add spaces before and after this tokens only when not between 2 Digits (1,000,000 5.2)
    SpecialDigitSeparators = [".",","]

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

    print("\t\t Done in ",time.clock() - StartTime," sec")


