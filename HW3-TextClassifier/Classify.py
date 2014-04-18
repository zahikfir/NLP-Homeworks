#********************** NLP **********************#
# H.W 3
# Haim Shalelashvily    200832780
# Zahi Kfir             200681476
#********************** NLP **********************#

import sys, os, time
StartTime = time.clock()

# Return the execution mod and the appropriate command arguments
def GetCommandLineArguments():
    try:
        # Get the command line argument
        if len(sys.argv) < 2: sys.exit("Please enter an execution mode: -e for evaluation or -c for classification")
        executionMode = sys.argv[1]

        # if execution mode is evaluation
        if (executionMode == '-e'):
            if len(sys.argv) < 4: sys.exit("To run classify.py in evaluation mode run the command: classify.py -e -training FolderWithInputFiles")
            InputFilesFolder = sys.argv[sys.argv.index("-training") + 1]
            TestsFilesFolder = None
        # else if we are in classify mode
        elif (executionMode == '-c'):
            if len(sys.argv) < 6: sys.exit("To run classify.py in classify mode, run the command: classify.py -c -training FolderWithInputFiles -test FolderWithTestFiles")
            InputFilesFolder = sys.argv[sys.argv.index("-training") + 1]
            TestsFilesFolder = sys.argv[sys.argv.index("-test") + 1]
        # wrong execution mode
        else: sys.exit("Please enter an execution mode: -e for evaluation or -c for classification")
    
    # if one of the option parameters is missing
    except: sys.exit("Wrong input. Please check your command line arguments")
    
    print('Start Program. Execution mode: {0}, InputFolder: {1}, TestFolder: {2}'.format(executionMode, InputFilesFolder, TestsFilesFolder))

    return executionMode,InputFilesFolder,TestsFilesFolder
    
# parse the command line arguments
executionMode,InputFilesFolder,TestsFilesFolder = GetCommandLineArguments()

print("Total Time (sec):\t\t\t" ,time.clock() - StartTime)