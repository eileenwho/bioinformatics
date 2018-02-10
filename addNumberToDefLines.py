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
                line_edit=line[1:]
                fileFix.write(">"+str(counter)+line_edit)
            else:
                fileFix.write(line)

if __name__ == '__main__':
    #open_dir_fix("C:/Users/Eileen/Documents/2017 spring UROP/rename_file")
    open_dir_fix("C:/Users/Eileen/Documents/2017 spring summer UROP with Lily in EAPS/script_test_file")