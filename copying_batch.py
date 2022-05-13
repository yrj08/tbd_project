# This file makes the individual batch job submission files that each submits a portion of the tasks for a given reflectivity configuration.
# Ruijia Yang, version 5 (March 28, 2022).

# Inputting method does not work.
#print('Input outer cryostat reflectivity: ')
#oc_ref = input()
#print('Input stainless steel reflectivity: ')
#st_ref = input()

# This section should be improved such that the below info can be changed by input, or YAML card, or whatever method of inputting that is superior to modifying this code.
oc_ref = "60" # Outer cryostat reflectivity value
st_ref = '40' # Stainless steel reflectivity value
total_nb_files = 10

# Reads in the sample / virgin / template batch submission file.
my_file = open("batch_sim_template.sh", "r")
file_contents = my_file.readlines()

# Ideally, the below function should be removed from this file and imported from elsewhere because it is duplicated in two other files.
def output_suffix(curr_index, max_nb_files):
    """
    Generates the string needed to save multi-part files. For example,
    saving file 9 of 302 would generate suffix "009".
    """
    if (len(str(curr_index)) < len(str(max_nb_files))):
        return '0'*(len(str(max_nb_files)) - len(str(curr_index))) + str(curr_index)
    else:
        return str(curr_index)
    
# Part of the name of YAML file (without prefix) that will be imported
yaml_name = "OD_OC" + str(oc_ref) + "_ST" + str(st_ref) + "_v4_"

#output_file = open('batch_sim_OC' + str(oc_ref) + '_ST' + str(st_ref) + '_all.sh','w')

line_05_new = "#SBATCH --job-name=RJRF" + str(oc_ref) + str(st_ref) + '\n'
line_06_new = "#SBATCH --output=batchOut-OC" + str(oc_ref) + "-ST" + str(st_ref) + "/output-OC" + str(oc_ref) + "-ST" + str(st_ref) + "-%j.txt" + '\n'
line_07_new = "#SBATCH --error=batchOut-OC" + str(oc_ref) + "-ST" + str(st_ref) + "/err-output-OC" + str(oc_ref) + "-ST" + str(st_ref) + "-%j.txt" + '\n'
line_19_new = "OUTDIR='/gpfs/slac/staas/fs1/g/exo/exo_data8/exo_data/users/yangrj/chromasim/chroma-simulation/batchOut-OC" + str(oc_ref) + "-ST" + str(st_ref) + "'\n"

#for j in file_contents[0:4]:
#    output_file.write(j)

#output_file.write(line_05_new)
#output_file.write(line_06_new)
#output_file.write(line_07_new)

#for r in file_contents[7:18]:
#    output_file.write(r)

#output_file.write(line_19_new)

#for p in file_contents[19:20]:
#    output_file.write(p)

for i in range(total_nb_files):
    curr_yaml_file = output_suffix(i,total_nb_files-1) # -1 because indexed from 0...
    
    line_21_new = "singularity exec --nv -B /gpfs ../Chroma.sif python ./RunSim.py -y Yaml/OD/" + yaml_name + curr_yaml_file + ".yaml\n"
    
    # Writes the new YAML cards.
    output_file = open('batch_sim_OC' + str(oc_ref) + '_ST' + str(st_ref) + '_' + curr_yaml_file + '.sh','w')

    for r in file_contents[0:4]:
        output_file.write(r)

    output_file.write(line_05_new)
    output_file.write(line_06_new)
    output_file.write(line_07_new)

    for j in file_contents[7:18]:
        output_file.write(j)

    output_file.write(line_19_new)

    for p in file_contents[19:20]:
        output_file.write(p)

    output_file.write(line_21_new)

    for m in file_contents[21:]:
        output_file.write(m)
