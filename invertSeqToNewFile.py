import glob
import os

#starting very specific will generalize when I have time

#works in the current directory
#run in terminal
#assumes format is >defline
#sequence on a variable # of lines
#takes every defline and sequence that doesn't contain the search term and copies them into a new file with a similar name
def open_files(dir_path, search):
    for file in glob.glob(os.path.join(dir_path, '*.fasta')):
        print("opening" + file)
        copy_seq_to_new(file, search)

def copy_seq_to_new(file, search):

    #create new file base name
    new_file_path=os.path.splitext(file)[0]+'_output.fasta'
    #later make this an input and generalize

    #go thru original file and copy over anything that's in species_to_copy


    #this opens the new file in read mode and the old file in append mode
    with open(new_file_path, 'w+') as new_file, open(file, 'r') as old_file:
            #maybe should do for line in file
        current_line_sequence_to_copy=False
        for current_line in old_file:
            if '>' in current_line:
                #make this a not case sensitive search with .lower()
                if search.lower() not in current_line.lower():
                    new_file.write(current_line)
                    current_line_sequence_to_copy=True
                else:
                    current_line_sequence_to_copy=False
            elif current_line_sequence_to_copy:
                new_file.write(current_line)





if __name__ == '__main__':
    print("Running in terminal")
    import sys
    import argparse
    import os
    import re
    import time

    # parser = argparse.ArgumentParser(description="All")
    # parser.add_argument("-o", "--oldDirectoryName", action = "store", default = False, help="give the name of the directory containing the existing gene sequence files to be added to.")
    # args = parser.parse_args()

    search='Bin'
    open_files(os.getcwd(), search)
    print('finished')
