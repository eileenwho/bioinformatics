import glob
import os

#starting very specific will generalize when I have time

#works in the current directory
#run in terminal
#assumes format is >defline
#sequence on one line
#takes every defline and sequence where the species name (text after carrot) matches one of the search terms
#  and copies them into a new file with a similar name
def open_files(dir_path, species_to_copy):
    for file in glob.glob(os.path.join(dir_path, '*.fas')):
        print("opening" + file)
        copy_seq_to_new(file, species_to_copy)

def copy_seq_to_new(file, species_to_copy):

    #create new file base name
    protein_name = os.path.splitext(file)[0].split("_")[-1]
    new_file_name='Analysis13_'+protein_name+'.fas'
    new_file_path=os.path.dirname(file)
    new_file_path=os.path.join(new_file_path, new_file_name)
    #later make this an input and generalize

    #go thru original file and copy over anything that's in species_to_copy


    #this opens the new file in read mode and the old file in append mode
    with open(new_file_path, 'w+') as new_file, open(file, 'r') as old_file:
            #maybe should do for line in file
        current_line_sequence_to_copy=False
        for current_line in old_file:
            if '>' in current_line:
                #species_name=current_line.replace('>','')
                species_name=current_line.strip('>').strip()
                #print(species_name)
                if species_name in species_to_copy:
                    print("a species was found!")
                    print(species_name)
                    new_file.write(current_line)
                    current_line_sequence_to_copy=True
            elif current_line_sequence_to_copy:
                new_file.write(current_line)
                current_line_sequence_to_copy=False





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

    species_to_copy=set(['Ehrlichia_canis', 'Anaplasma_phagocytophilum', 'Wolbachia_endosymbiont_of_Drosophila', 'Rickettsia_typhi','Candidatus_Pelagibacter',
                         'Pelagibaca_bermudensis', 'Parvularcula_bermudensis','Methylobacterium_radiotolerans', 'Caulobacter_segnis',
                         'Rhodospirillum_centenum', 'Magnetococcus_marinus', #end of alphaproteobacteria
                         'Ignavibacterium_album', 'Melioribacter_roseus', #end of ignavibacteria
                         'Chloroherpeton_thalassium', 'Chlorobaculum_parvum', 'Chlorobium_tepidum','Prosthecochloris_aestuarii' #end of chlorobi
                         ])

    open_files(os.getcwd(), species_to_copy)
    print('finished')