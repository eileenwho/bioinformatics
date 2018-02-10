

#make a new directory for output files
import glob
import os

def search_dir(dirPath, searchTerms):
    for file in glob.glob(os.path.join(dirPath, '*.faa')):
       search_file(file, searchTerms,dirPath)

def search_file(filename, searchTerms,dirPath): #filename is the file you're looking at, searchTerms is an array of the terms you're looking for
    # load 1 file
    file=open(filename, "r") #this opens the file
    print("1"+os.getcwd())
    filename_root=os.path.splitext(filename)[0]

    newDir = filename_root+"_output"
    print("2" + os.getcwd())
    if not os.path.exists(newDir):
        os.makedirs(newDir)
    os.chdir(newDir)
    print("3" + os.getcwd())
    #see what it does when there is a directory
    #this still doesn't write the new files to the new directories but new directories are created

    for i, line in enumerate(file): #loop thru lines in the file
        if ">" in line:
            for term in searchTerms:
                if term in line:
                    print(term + ' found: line ' +str(i+1))
                    outputName=newDir+"_"+term+"_line"+str(i+1)+".faa" #create name for output file
                    print("5" + os.getcwd())
                    print(outputName)
                    #with newDir it does C:/Users/Eileen/Documents/2017 spring UROP/python_search_test\SURF_1_output_nitrate_line11420.faa
                    #with filename_root it does C:/Users/Eileen/Documents/2017 spring UROP/python_search_test\SA_8_nitrite_line35129.faa
                    outputFile = open(outputName,"w") #open new output file
                    outputFile.write(line) #write the first line of block to output file
                    currentLine= file.readline() #advances pointer to next line and set currentLine to that new line
                    while currentLine != "\n": #loop thru lines in block of annotated genome until new line
                        outputFile.write(currentLine) #writes currentLine to output file
                        currentLine= file.readline() #advances pointer to next line and sets currentLine to that
                    outputFile.close()

    print("6" + os.getcwd())
    os.chdir(dirPath)
    print("7" + os.getcwd())
    file.close()

if __name__ == '__main__':
        searchTerms = ['nitrate', 'nitrite', 'sulfite']
        #search_file('SA_7.faa', searchTerms)
        #search_dir("C:/Users/Eileen/PycharmProjects/2017 spring UROP", searchTerms)
        search_dir("C:/Users/Eileen/Documents/2017 spring UROP/python_search_test", searchTerms)