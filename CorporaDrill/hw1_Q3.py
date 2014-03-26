import sys, os, codecs

#get the command line argument
if len(sys.argv) < 2: sys.exit("Please enter a data directory path")
currentDir = sys.argv[1]

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
    