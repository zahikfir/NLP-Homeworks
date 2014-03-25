import sys, os, codecs

#get the command line argument
if len(sys.argv) < 2: sys.exit("Please enter a data directory path")
currentDir = sys.argv[1]
print("The data folder is: " + currentDir)

# get all the txt file paths from the given data directory
txtFilesList = [ os.path.join(currentDir, f) for f in os.listdir(currentDir) if (os.path.isfile(os.path.join(currentDir, f)) & str(f).endswith(".out.txt"))]

# seperate each text to sentences 
for f in txtFilesList:
    print("Creating a frequency list of file :  " + f)
    
    # open the input file and create an output file
    inputFileStream  = codecs.open(f,"r","utf-8")
    outputFileStream = codecs.open(f[0:(f.rfind(".txt"))] + "_freq.txt" , "w", "utf-8")
    
    # class for creating a counted dictionary
    from collections import Counter
    
    # create a dictionary of words sorted from the most common one to the last common one
    freqs = Counter(inputFileStream.read().split()).most_common()
    
    # output the freqs table to the output file
    outputFileStream.writelines("Freq           Token          Rank\r\n")
    outputFileStream.writelines(("%15d%15s%15d \r\n" % (idx + 1, val[0], val[1]) for idx, val in enumerate(freqs)))
    