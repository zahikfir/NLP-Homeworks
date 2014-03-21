import sys, os

#get the command line argument
if len(sys.argv) < 2: sys.exit("Please enter a data directory path")
currentDir = sys.argv[1]
print("The data folder is: " + currentDir + "\n")

# get all the txt file paths from the given data directory
txtFilesList = [ os.path.join(currentDir, f) for f in os.listdir(currentDir) if (os.path.isfile(os.path.join(currentDir, f)) & str(f).endswith(".txt"))]

# seperate the text to sentences 
for f in txtFilesList:
    print("Start working on file : " + f + "\n")
    inputFileStream  = open(f,'r')
    outputFileStream = open(f[0:(f.rfind(".txt"))] + "_sentences.txt" , 'w')