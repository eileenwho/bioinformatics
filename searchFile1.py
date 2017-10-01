

#note: this doesn't differentiate between already created output files and the original files, so make sure that the folder doesn't have any output files already in it
import glob
import os

def search_dir(dirPath, searchTerms):
    for file in glob.glob(os.path.join(dirPath, '*.faa')): #searches .faa files in the given directory
       search_file(file, searchTerms,dirPath)

def search_file(filename, searchTerms,dirPath): #filename is the file you're looking at, searchTerms is an array of the terms you're looking for
    file=open(filename, "r") #this opens the file

    filename_root=os.path.splitext(filename)[0]
    filename_name=os.path.basename(filename_root)

    newDir = filename_root+"_output"
    if not os.path.exists(newDir): #create new directory for output
        os.makedirs(newDir)

    lineNumber=0 #to keep track of line number accurately
    for i, line in enumerate(file): #loop thru lines in the file
        lineNumber +=1
        if ">" in line:
            found_string=""
            for term in searchTerms: #checks if any search terms are in the line
                if str.lower(term) in str.lower(line): #to account for uppercase in header
                    found_string += "_"
                    found_string +=term
            if found_string:
                outputName = newDir+"\\"+filename_name + found_string + "_line" + str(lineNumber) + ".faa" #create name for output file
                outputFile = open(outputName,"w") #open new output file
                outputFile.write(line) #write the first line of block to output file
                currentLine= file.readline() #advances pointer to next line and set currentLine to that new line
                lineNumber+=1
                while currentLine != "\n": #loop thru lines in block of annotated genome until new line
                    outputFile.write(currentLine) #writes currentLine to output file
                    lineNumber+=1
                    currentLine= file.readline() #advances pointer to next line and sets currentLine to that
                outputFile.close()

    file.close()

if __name__ == '__main__':
        searchTerms = ['nitrate', 'nitrite', 'sulfite']
        #search_file('SA_7.faa', searchTerms)
        #search_dir("C:/Users/Eileen/Documents/2017 spring UROP/python_search_test", searchTerms)
        searchTerms0417 = ['sulfite', 'desulfoviridin','nitrite', 'nitrate','nitrous','methane','coenzyme','heterodisulfide','nitrogenase','nifH','nifD','nifK','nifB','nifE']
        searchTermsChloroflexi=['sulfite','desulfoviridin','dissimilatory','dsr']

