#goal is create script so that the input files will be rewritten so another program can parse it properly
# will be used on many files
# strip read_id
# replace all _ with .
# replace everything after second 1 w/ #id
# strip everything up to 1st pipe, get rid of pipes
# >11531113|DCO_LOIH_Av4v5--J672black_Av4v5|1
# to > DCO.LOIH.Av4v5--J672black_Av4v5. (counter)

import glob
import os


def open_dir_fix(dirPath):
    for file in glob.glob(os.path.join(dirPath, '*.fasta')):
       fix_file2(file)

def fix_file2(fileName):
# open input file, open output file
    fileNameRoot = os.path.splitext(fileName)[0]
    with open(fileName, 'r') as file, open(fileNameRoot+"_fix.fasta", 'w') as fileFix:
#set counter to 0
        counter = 0
# loop thru lines in the file
        for line in file:
# if you find a carrot
            if ">" in line:
#increment counter
                counter +=1
#write fixed line to file
                fileFix.write(changeLine(line)+str(counter))
            else:
                fileFix.write(line)

def changeLine(line):
    #>11531113|DCO_LOIH_Av4v5--J672black_Av4v5|1
    # to > DCO.LOIH.Av4v5--J672black_Av4v5. (counter)
    fixed_line=">"
    first_pipe = False
    second_pipe=False
    for c in line:
        if c is "|" and not first_pipe:
            first_pipe=True
        elif c is "|":
            second_pipe=True
        elif first_pipe and not second_pipe:
            if c is "_":
                fixed_line += "."
            else:
                fixed_line +=c
    fixed_line += "."
    return fixed_line

if __name__ == '__main__':
    #print(changeLine(">11531113|DCO_LOIH_Av4v5--J672black_Av4v5|1"))
    open_dir_fix("C:/Users/Eileen/Documents/2017 spring UROP/rename_file")