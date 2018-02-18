import glob
import os


#TODO
#remove redundant code
#better comments
#add README/ internal README
#come up with a better name extractCopyProteinSeq
#WOULD LIKE TODO
#speed it up possibly if the time doesn't come from the blasting process
#add option to only do blast or only do copying over?
# leave in ribo protein list so that's an extra level of flexibility

#add output file for if sequences are a lot longer
#to do checking, make a another file that's copied in from the first blast results
#save 3 top typical lines
#if copied in
#or do both at the same time
#if copied in line not within # for length
#calc closeness of genome with different cutoffs of front or end cutting off by a certain #
#hmm 1 problem is a subst or deletion would throw things off
#so maybe check against first 10 or last 10 of references
#and if neither work just cut off from the end

#anything for if it's too short?

#make sure to be clear what inputs this wants and what it outputs aka where things are

#i guess first things is if if it's significantly different
#can print in terminal "note:" __ "has a sequence that is ___ longer than the first sequence in the file
#would have to save that elsewhere don't think you can read an append file

#or a thing where you check to see if this genome is already in the file b/c that would handle some errors

######################################################
## BLAST proteins against reference database
######################################################

def round1(dir_path,database, protein_list_file):



    f = open(protein_list_file, 'r')
    for line in f:
        protein_list = line.rstrip().split('\t')

    #create new directory named (current directory)_BLAST eg Analysis0_BLAST
    new_dir_name=os.path.split(dir_path)[1]+'_BLAST' #TODO could maybe use os.path.basename(path) but make sure it doesn't get messed up with running on unix
    new_dir_path=os.path.join(dir_path,new_dir_name)
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)

    database_path = os.path.join(dir_path, database)
    #figure out db_head from first file in db
    database_files= os.listdir(database_path)
    first_file=database_files[0]
    split=first_file.split('_')
    file_head=''
    for i in range(len(split)-1):
        file_head = file_head+ split[i] +'_'
#TODO there's definitely a better way to do this

    db_head=os.path.join(database,file_head)

    for genome_path in glob.glob(os.path.join(dir_path, '*.fna')):
        run_blast(genome_path, dir_path,new_dir_path,db_head,protein_list)


def run_blast(genome_path,dir_path,new_dir_path,db_head,protein_list):
    genome_file=os.path.split(genome_path)[1]
    genome_name=genome_file.split('.')[0]


    output_dir=os.path.join(new_dir_path,genome_name)


    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    #create error directory and file in new file
    error_dir=os.path.join(output_dir,'error')
    if not os.path.exists(error_dir):
        os.makedirs(error_dir)
    #create no_hits file
    missed = open(os.path.join(output_dir,'no_hits.txt'), 'w')
    missed.write('ribosomal_protein\tGenome\thits\n')


    #blast Clostridia.faa/your reference file to delta gene database
    output_head = os.path.join(output_dir,'round_1_')
    for n in range(1,len(protein_list)+1):
        #call blast database
        db = db_head + str(n)

        # open writing files
        txtout = open(output_head + str(n) + '.txt', 'w')
        fastaout = open(output_head + str(n) + '.faa', 'w')
        # Blast each genome against db
        blastFile = 'tempBlast.txt'
        d = {}
        os.system('blastx.exe -db ' + db + ' -query ' + genome_file + ' -evalue 1e-10 -outfmt 2 -out ' + blastFile)
        bf = open(blastFile, 'r')
        mySeq = ''
        hits = ''
        #copy blast results into a .faa file and info into a text file
        try:
            for l in bf:
                if 'Query_' in l:
                    t = l.split('  ')
                    h=genome_name+'_'+t[0]
                    mySeq += t[2]
                    hits += h
            #record in text file
            txtout.write(genome_name + '\t' + hits + '\n')
            #if there is a result copy into fasta file
            if len(mySeq) > 0:
                fastaout.write('>' + h + '\n' + mySeq + '\n')
            #if there is no result
            else:
                fastaout.write('>' + genome_name + '\n')
                missed.write(str(n) + '\t' + genome_name + '\t\n')
        except:
            # txtout.write(genome_path + '\t\n')
            txtout.write(genome_name + '\t\n')
        bf.close()
        fastaout.close()
        txtout.close()

    missed.close()

######################################################
## copy BLAST results into individual gene files
######################################################

#have existing fasta files for each ribosomal protein (1 thru 30), in old_dir
#also have to_add_dir with ncbi blast results single gene in each fasta file
#those genes need to be copied on to the end of the larger fasta files
#take each of the round_1_1.faa in folder_2, stick it in the correct file in folder 1
#file name format old is Analysis#_L1.fas
#file name format new is round_1_1.faa


#to add file will refer to the new files with single gene sequences to be copied
#old file refers to the existing original file with several gene sequences that the single gene sequences from the new files will be appended to
def copy_all_blast(dir_path, old_dir_name, protein_list_file):


    #create protein key
    f = open(protein_list_file, 'r')
    for line in f:
        protein_list = line.rstrip().split('\t')
    protein_key={}
    for i,protein_name in enumerate(protein_list):
        protein_key[i+1]=protein_name


    old_dir_path=os.path.join(dir_path, old_dir_name)
    to_add_dir_name = os.path.split(dir_path)[1] + '_BLAST'
    to_add_dir_path = os.path.join(dir_path, to_add_dir_name)

    #this goes through all the .faa files in the to_add_dir and its subdirectories
    for file in glob.glob(os.path.join(to_add_dir_path,'*','*.faa')):
        read_write_new_gene(file, old_dir_path,protein_key)


def read_write_new_gene(newFilePath,oldFilesDirPath, protein_key):
#this section sets up the old file path for the appropriate protein's file
    #get last number off of the new file's name (format round_#_#.faa) to figure out what old file to add it to
    #this splits the path and takes the root so the file extension is gone, then splits that by underscore and takes the last bit
    new_protein_number=os.path.splitext(newFilePath)[0].split("_")[-1]
    #use protein key dictionary to figure out what old file to add the new gene sequence to
    old_protein_name = protein_key[int(new_protein_number)]
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

def trim_query(defline): #go from Oscillatoria_acuminata_Query_1 to Oscillatoria_acuminata
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

    print("Running in terminal")
    import sys
    import argparse
    import os
    import re
    import time
    import glob
    import os
    # from Bio import SeqIO


    parser = argparse.ArgumentParser(description="All")
    parser.add_argument("-db", "--database", action="store", default=False,
                        help="give the name of the directory with the reference proteins to be blasted against")
    parser.add_argument("-pl", "--plist", action="store", default=False,
                        help="give the name of the text file containing the names of all the proteins including .txt")

    parser.add_argument("-of", "--oldFileName", action = "store", default = False, help="give the name of the directory containing the existing gene sequence files to be added to.")
    args = parser.parse_args()

    #run BLAST search against reference database to pull out individual ribo proteins from genome files
    round1(os.getcwd(), args.database, args.plist)
    # round1(os.getcwd(),"Clostridia_Ribo_db", "30_Arch_RiboProteins.txt")

    #copy blast results into existing individual gene files
    # copy_all_blast(os.getcwd(),"Analysis11_30genefiles","30_Arch_RiboProteins.txt")
    copy_all_blast(os.getcwd(), args.oldFileName, args.plist)

    #check which ones are weird lengths?

    #also add an argument for if you want to trim the deflines?
    print('finished')


