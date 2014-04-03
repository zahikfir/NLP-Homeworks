#********************** NLP **********************#
# H.W 2
# Haim Shalelashvily    200832780
# Zahi Kfir             200681476
#********************** NLP **********************#

import sys, os, codecs, re, time

#get the command line argument
if len(sys.argv) < 2: sys.exit("Please enter a data directory path")
currentDir = sys.argv[1]
outputDir = sys.argv[2]
print("The data folder is: " + currentDir)
print("The output folder is: " + outputDir)

# get all the txt file paths from the given data directory
txtFilesList = [ os.path.join(currentDir, f) for f in os.listdir(currentDir) if (os.path.isfile(os.path.join(currentDir, f)) & str(f).endswith(".txt"))]


# Make sure the output directory path ends with '\'
if not(outputDir[-1] == '\\'):
    outputDir = outputDir + '\\'
    
# Create the output files for Raw Frequency analysis
RF_Raw_outStream = codecs.open(outputDir + "RawFrequency_raw.txt", "w", "utf-8")
RF_Select_outStream = codecs.open(outputDir + "RawFrequency_select.txt", "w", "utf-8")

# Create the output files for t-test analysis
tTest_Raw_outStream = codecs.open(outputDir + "tTest_raw.txt" , "w", "utf-8")
tTest_Select_outStream = codecs.open(outputDir + "tTest_select.txt" , "w", "utf-8")

# Create the output files for PMI analysis
PMI_Raw_outStream = codecs.open(outputDir + "PMI_raw.txt" , "w", "utf-8")
PMI_Select_outStream = codecs.open(outputDir + "PMI_select.txt" , "w", "utf-8")

# Run Raw Frequency analysis
import RawFrequencyAnalysis
RawFrequencyAnalysis.RawFrequencyAnalysis(txtFilesList,RF_Raw_outStream,RF_Select_outStream)

# Run t-test analysis
import tTestAnalysis
tTestAnalysis.tTestAnalysis(txtFilesList,tTest_Raw_outStream,tTest_Select_outStream)

# Run PMI analysis
import PmiAnalysis
PmiAnalysis.PmiAnalysis(txtFilesList,PMI_Raw_outStream,PMI_Select_outStream)







