# This file makes the batch job that runs all batch job files.

oc_ref = "60"
st_ref = '40'
nb_files = 10

def output_suffix(curr_index, max_nb_files):
    """
    Generates the string needed to save multi-part files. For example,
    saving file 9 of 302 would generate suffix "009".
    """
    if (len(str(curr_index)) < len(str(max_nb_files))):
        return '0'*(len(str(max_nb_files)) - len(str(curr_index))) + str(curr_index)
    else:
        return str(curr_index)
    
yaml_name = "batch_sim_OC" + str(oc_ref) + "_ST" + str(st_ref) + "_" #"OD_OC00_ST00_v4_"
firstline = "#!/bin/bash\n"

output_file = open('batch_sim_OC' + str(oc_ref) + "_ST" + str(st_ref) + '_all.sh', 'w')
output_file.write(firstline)
output_file.write('\n')

for i in range(nb_files):
    curr_yaml_file = output_suffix(i,nb_files-1)
    
    line_output = "sbatch " + yaml_name + curr_yaml_file + ".sh\n"
    
    output_file.write(line_output)

output_file.close()
