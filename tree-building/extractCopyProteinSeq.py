#TODO currently untested
#TODO where should i put my imports anyway
import glob
import os


#To use this script
#cd to folder containing:
# A. all whole genome files (nucleotide) that you want to pull out the protein sequences from eg Leptolyngbya_frigida_ULC18.fna or XAN_12.fna
# B. text file with list of names of proteins separated by whitespace
# C. reference database directory with the proteins sequences to be blasted against, file names should have _# at end, eg 'Clostridia_Ribo_1', in same order as in text file
# D. directory containing existing files for each protein with sequences for previously blasted sequences eg Analysis0_L23.fas

#in terminal run command $python extractCopyProteinSeq.py -db database_directory_name -pl protein_list_text_file -of existing_gene_sequences_directory
# -db refers to C, -pl refers to B, -of refers to D
#i recommend using nohup b/c this takes a while to run
#will result in: directory called cwd_BLAST with blast results for each protein and each result being appended on to the correct protein file in the existing gene sequences directory
#you will still need to manually check for any sequences that are significantly longer than the rest
#the input files should be .fna full genome, nucleotide sequences, unannotated b/c this code runs blastx (nucleotide to amino acid).
# If you have the amino acid sequences, you should change blastx to blastp in the code, and with "for genome_path in glob.glob(os.path.join(dir_path, '*.fna')):" change .fna to the correct file extension

def extract_copy_all(dir_path,database,protein_list_file, old_dir_name):
    f = open(protein_list_file, 'r')
    for line in f:
        protein_list = line.rstrip().split('\t')

    #create text file that will temporarily store blastx ouput
    blast_file=open("tempBlast.txt", "w+")
    blast_file.close()

    #TODO SEE IF THIS WHOLE THING IS NECESSARY also rename db_head possibly
    database_path = os.path.join(dir_path, database)
    #figure out db_head from first file in db
    database_files= os.listdir(database_path)
    first_file=database_files[0]
    split=first_file.split('_')
    file_head='_'.join(split[:len(split)-1])
    db_head=os.path.join(database,file_head)

    old_dir_path=os.path.join(dir_path,old_dir_name)
    old_dir_files= os.listdir(old_dir_path)
    first_file=old_dir_files[0]
    split=first_file.split('_')
    file_head='_'.join(split[:len(split)-1])
    old_dir_head=os.path.join(old_dir_name,file_head)


    #loop through all the genome files in the current working directory
    for genome_path in glob.glob(os.path.join(dir_path, '*.fna')):
        print("blasting " + genome_path)
        extract_copy(genome_path,dir_path,db_head,protein_list,old_dir_head)
    #print to terminal
        #some inner function

#innerfunction
    #get genome file path
    #make output file named genome_output which will record: the sequence that was written, the file written to, any errors that occur

    #for every protein
    #open the relevant file in old_dir_files

    #do the blast search, putting it into tempBLAST

    #look into this a bit more, what does that file look like when there's no result?

    #copy relevant information into the correct old_dir_files file and the output file
    #if no result, write no result in output file and do nothing in the old_dir_files file

    #either close everything or do the with thing at the beginning
    # this opens the new file in read mode and the old file in append mode
    #with open(new_file_path, 'w+') as new_file, open(file, 'r') as old_file:
def extract_copy(genome_path,dir_path,db_head,protein_list,old_dir_head):

    #get genome name and file from file path
    genome_file=os.path.split(genome_path)[1]
    genome_name=genome_file.split('.')[0]

    output_file=open(genome_name+"_output.txt", 'w')


    for n in range(1,len(protein_list)+1):
        protein_name=protein_list[n-1]
        #this is specific to file naming syntax we have
        db = db_head + '_' + str(n)
        blast_file_name='tempBlast.txt'
        os.system('blastx.exe -db ' + db + ' -query ' + genome_file + ' -evalue 1e-10 -outfmt 2 -out ' + blast_file_name)

        old_file_path=old_dir_head+'_'+protein_name+'.fas'
        with open(old_file_path, 'w') as old_file, open(blast_file_name, 'r') as blast_file:
            sequence = ''
            for line in blast_file:
                #for now put everything from tempBlast into output file until I decide what's important to note
                output_file.write(line)

                if 'Query_' in line:
                    sequence+=line.split()
            if len(sequence) > 0:
                old_file.write('>'+genome_name+'\n' + mySeq + '\n')
                output_file.write('\n'+"sequence written to" +old_file_path+'\n')
            else:
                output_file.write('\n'+"no hits so no sequence written to" +old_file_path+'\n')

    output_file.close()


# blast outputs a decent amount of data, but the relevant part is formatted like this
# top lines are from the genome we queried, bottom lines are what it matches up to in the reference database sequence
#
# Query_1  3392087  MSRSLKKGPFVADHLLSKIEALNASGKKDVIKTWSRASTIIPDMLGHTIAVHNGRQHVPV  3392266
# 0        1        MARSLKKGPFADKSLLNKVDAMNEAGDKSVIKTWSRRSTIFPSFVGHTIAVHDGRKHVPV  60
#
# Query_1  3392267  YINEQMVGHKLGEFAPTRTFRGHAKGDKKS  3392356
# 0        61       YVTEDMVGHKLGEFVATRTFRGHKKTEKKT  90




if __name__ == '__main__':

    print("Running in terminal")
    #TODO do these need to be here?
    import sys
    import argparse
    import os
    import re
    import time
    import glob



    parser = argparse.ArgumentParser(description="All")
    parser.add_argument("-db", "--database", action="store", default=False,
                        help="give the name of the directory with the reference proteins to be blasted against")
    parser.add_argument("-pl", "--plist", action="store", default=False,
                        help="give the name of the text file containing the names of all the proteins including .txt")

    parser.add_argument("-od", "--oldDirectoryName", action = "store", default = False, help="give the name of the directory containing the existing gene sequence files to be added to.")
    args = parser.parse_args()

    extract_copy_all(os.getcwd(),args.database,args.plist,args.oldDirectoryName)


    print('finished')


