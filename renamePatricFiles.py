import os

#when you download multiple sequences from patric, it downloads as a zipped directory PATRIC_Export
#with 1 subdirectory for each genome
#and genomes are named by PATRIC acession# so you have sthg like PATRIC_Export/65479.3/65479.3.fna
#this script when placed in PATRIC_Export and run, will rename the file to genus_species_strain.fna and put the file in the enclosing PATRIC_Export directory

def rename_files(working_dir):
    for root, dirs, files in os.walk(working_dir):
        for file_name in files:
            print(file_name)
            if os.path.splitext(file_name)[1]=='.fna':
                with open(os.path.join(root, file_name), "r") as genome_file:
                    first_line=genome_file.readline()
                    #>NC_000914   Rhizobium sp. NGR234 plasmid pNGR234a, complete sequence.   [Sinorhizobium fredii NGR234 | 394.7]
                    # want to get to Sinorhizobium_fredii_NGR234
                    name=""
                    copy=False
                    #yup this is clunky but it works
                    for c in first_line:
                        if copy:
                            if c is '|':
                                name=name[0:-1] #gets rid of trailing '_'
                                copy=False
                            elif c is '.': #personally don't want _sp._ in file names
                                pass
                            elif c is ':': #: messes with things
                                pass
                            elif c is ' ':
                                name += '_'
                            else:
                                name +=c
                        elif c is '[':
                            copy=True
                        else:
                            pass
                    if name:
                        name += ".fna"
                    else:
                        name="error.txt"

                    print(name)
                    source=os.path.join(root, file_name)
                    dest=os.path.join(working_dir, name)
                    #want to move it out of the subdirectory into the enclosing directory
                    os.rename(source, dest)

if __name__ == '__main__':
    rename_files(os.getcwd())