#goal is create script so that the input files will be rewritten so another program can parse it properly
# will be used on many files
# the other program looks for sequential identifiers
#input files have header line that doesn't have numerical unique identifier taht the program wants
#but does have > 15 character unique identifier
#try to append underscore # sequential (aka _1, _2, _3)
#if possible go before -- 1_H7B etc

import glob
import os


def open_dir_fix(dirPath):
    for file in glob.glob(os.path.join(dirPath, '*.fasta')):
       fix_file(file)

def fix_file(fileName):
# open input file, open output file
    fileNameRoot = os.path.splitext(fileName)[0]
    with open(fileName, 'r') as file, open(fileNameRoot+"_fix.fasta", 'w') as fileFix:
#set counter to 0
        counter = 0
# loop thru lines in the file
        for line in file:
# if you find a carrot
            if ">" in line:
                #print(line)
#increment counter
                counter +=1
#write line with counter to output file
                fileFix.write(line+"_"+str(counter))
            else:
                fileFix.write(line)

if __name__ == '__main__':
    open_dir_fix("C:/Users/Eileen/Documents/2017 spring UROP/rename_file")