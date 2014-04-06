#********************** NLP **********************#
# H.W 2
# Haim Shalelashvily    200832780
# Zahi Kfir             200681476
#********************** NLP **********************#

import sys, os, codecs, re, time

#get the command line argument
if len(sys.argv) < 3: sys.exit("Please enter a data directory path and an output folder path")
currentDir = sys.argv[1]
outputDir = sys.argv[2]
print("The data folder is: " + currentDir)
print("The output folder is: " + outputDir)

# get all the txt file paths from the given data directory
txtFilesList = [ os.path.join(currentDir, f) for f in os.listdir(currentDir) if (os.path.isfile(os.path.join(currentDir, f)) & str(f).endswith(".txt"))]

# unsure that that the output directory don't exist and create it
if not os.path.exists(outputDir):
        os.makedirs(outputDir)
    
# Create the output files for Raw Frequency analysis
RF_Raw_outStream = codecs.open(os.path.join(outputDir, "RawFrequency_raw.txt"), "w", "utf-8")
RF_Select_outStream = codecs.open(os.path.join(outputDir, "RawFrequency_select.txt"), "w", "utf-8")

# Create the output files for t-test analysis
tTest_Raw_outStream = codecs.open(os.path.join(outputDir, "tTest_raw.txt"), "w", "utf-8")
tTest_Select_outStream = codecs.open(os.path.join(outputDir, "tTest_select.txt"), "w", "utf-8")

# Create the output files for PMI analysis
PMI_Raw_outStream = codecs.open(os.path.join(outputDir, "PMI_raw.txt"), "w", "utf-8")
PMI_Select_outStream = codecs.open(os.path.join(outputDir, "PMI_select.txt"), "w", "utf-8")

from collections import Counter

# Run Raw Frequency analysis
StartTime = time.clock()
import RawFrequencyAnalysis
Collocations_CountedDictionary = RawFrequencyAnalysis.RawFrequencyAnalysis(txtFilesList,RF_Raw_outStream,RF_Select_outStream)
RawFrequencyTime = time.clock() - StartTime

# Run t-test analysis
StartTime = time.clock()
import tTestAnalysis
tokensFreqs = tTestAnalysis.tTestAnalysis(txtFilesList,tTest_Raw_outStream,tTest_Select_outStream, Collocations_CountedDictionary)
tTestTime = time.clock() - StartTime

# Run PMI analysis
StartTime = time.clock()
import PmiAnalysis
PmiAnalysis.PmiAnalysis(txtFilesList,PMI_Raw_outStream,PMI_Select_outStream,Collocations_CountedDictionary,tokensFreqs)
PmiTime = time.clock() - StartTime


print("\nRaw Frequency analysis time (sec):\t"  ,RawFrequencyTime)
print("t-test analysis time (sec):\t\t"         ,tTestTime)
print("PMI analysis time (sec):\t\t"            ,PmiTime,'\n')





