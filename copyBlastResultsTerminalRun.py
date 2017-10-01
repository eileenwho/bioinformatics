#to use this script:
#stick the script in the same directory containing the directory for the existing files and the directory with new files to be added
#cd to that directory and enter the command:
# $ python copyBlastResultsTerminalRun.py -of existing_files_directory_name -nf new_files_directory_name


#goal
#have existing fasta files for each ribosomal protein (1 thru 30), in folder_1
#also have folder_2 with ncbi blast results single gene in each fasta file
#those genes need to be copied on to the end of the larger fasta files
#take each of the round_1_1.faa in folder_2, stick it in the correct file in folder 1
#file name format old is Analysis#_L1.fas
#file name format new is round_1_1.faa


import glob
import os

#new file will refer to the new files with single gene sequences to be copied
#old file refers to the existing original file with several gene sequences that the single gene sequences from the new files will be appended to
def open_dir_fix(dirPath, oldFilesDirectory, newFilesDirectory, protein_key):
    newFilesDirPath=dirPath+"/"+newFilesDirectory
    oldFilesDirPath=dirPath+"/"+oldFilesDirectory
    #this goes through all the .faa files in the directory of new files
    for file in glob.glob(os.path.join(newFilesDirPath, '*.faa')):
        read_write_new_gene(file, oldFilesDirPath,protein_key)

def read_write_new_gene(newFilePath,oldFilesDirPath, protein_key):
#this section sets up the old file path for the appropriate protein's file
    #get last number off of the new file's name (format round_#_#.faa) to figure out what old file to add it to
    #this splits the path and takes the root so the file extension is gone, then splits that by underscore and takes the last bit
    new_protein_number=os.path.splitext(newFilePath)[0].split("_")[-1]
    #use protein key dictionary to figure out what old file to add the new gene sequence to
    old_protein_name = protein_key[new_protein_number]
    #initialize oldFilePath
    oldFilePath=oldFilesDirPath
    #loop through .fas files in old files directory to find the correct protein file to add the sequence to
    for file in glob.glob(os.path.join(oldFilesDirPath, '*.fas')):
        filePathRoot= os.path.splitext(file)[0]
        file_protein_name=filePathRoot.split("_")[-1]
        if old_protein_name==(file_protein_name) or old_protein_name==(file_protein_name):
            oldFilePath=file
            break

    #this opens the new file in read mode and the old file in append mode
    with open(newFilePath, 'r') as newFile, open(oldFilePath, 'a') as oldFile:
        #read from new file
        sequence=newFile.readlines()
        #if the gene file is not blank
        if len(sequence)!=1:
            #trim off _Query_# from end of defline
            defline_query_trimmed=trim_query(sequence[0])
            #append to old file
            oldFile.write(defline_query_trimmed)
            oldFile.write(sequence[1])
        else:
            print("note: "+ newFilePath +" is blank")

def trim_query(defline):
    defline_split = defline.split("_")
    defline_query_trimmed = ""
    for section in defline_split:
        if section == "Query":
            #this gets rid of a trailing "_" and adds a newline to the end of the defline so the format will be correct
            defline_query_trimmed=defline_query_trimmed[0:-1]
            defline_query_trimmed += "\n"
            break
        else:
            defline_query_trimmed += section
            defline_query_trimmed += "_"
    return defline_query_trimmed

if __name__ == '__main__':
    protein_key={'1':'L1', '2':'L2', '3':'L3','4':'L4','5':'L5','6':'L6','7':'L10','8':'L13','9':'L14','10':'L15',
                 '11':'L18','12':'L22','13':'L23','14':'L24','15':'L29','16':'S2','17':'S3','18':'S4','19':'S5','20':'S7',
                 '21':'S8','22':'S9','23':'S10','24':'S11','25':'S12','26':'S13','27':'S14','28':'S15','29':'S17','30':'S19'}
    print("Running in terminal")
    import sys
    import argparse
    import os
    import re
    import time
    parser = argparse.ArgumentParser(description="All")
    parser.add_argument("-of", "--oldFileName", action = "store", default = False, help="give the name of the directory containing the existing gene sequence files to be added to.")
    parser.add_argument("-nf", "--newFileName", action= "store", default=False,help="give the name of the directory containing the new gene sequences to add to the existing gene sequence files.")

    args = parser.parse_args()
    open_dir_fix(os.getcwd(),args.oldFileName, args.newFileName, protein_key)
    print('finished')