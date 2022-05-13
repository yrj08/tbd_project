import os

# This file makes the individual batch job submission files that each submits a portion of the tasks for a given reflectivity configuration.

# This section should be improved such that the below info can be changed by input, or YAML card, or whatever method of inputting that is superior to modifying this code.
oc_ref = "60" # Outer cryostat reflectivity value
st_ref = "40" # Stainless steel reflectivity value
#list_job_IDs = [2296173, 2296174, 2296284, 2296285, 2296287, 2296289, 2296290, 2296292, 2296293, 2296294] # 00/00
#list_job_IDs = [2296298, 2296299, 2296300, 2296301, 2296302, 2296303, 2296304, 2296305, 2296306, 2296307] # 40/40
#list_job_IDs = [2301143, 2301144, 2301145, 2301146, 2301147, 2301148, 2301149, 2301150, 2301151, 2301152] # 60/60
#list_job_IDs = [2301509, 2301510, 2301511, 2301512, 2301513, 2301514, 2301515, 2301516, 2301517, 2301518] # 99/99
#list_job_IDs = [2336740, 2336741, 2336742, 2336743, 2336744, 2336745, 2336746, 2336747, 2336748, 2336749] # 00/99
#list_job_IDs = [2336753, 2336754, 2336756, 2336758, 2336760, 2336762, 2336764, 2336766, 2336768, 2336770] # 40/60
list_job_IDs = [2336755, 2336757, 2336759, 2336761, 2336763, 2336765, 2336767, 2336769, 2336771, 2336772] # 60/40
list_hd5_files = []
# [chromasim]/batchOut-OC40-ST40/output-OC40-ST40-2296298.txt
for jobID in list_job_IDs:
    curr_job_file = "/gpfs/slac/staas/fs1/g/exo/exo_data8/exo_data/users/yangrj/chromasim/chroma-simulation/batchOut-OC"+ str(oc_ref) + "-ST" + str(st_ref) + "/output-OC" + str(oc_ref) + "-ST" + str(st_ref) + "-" + str(jobID) + ".txt"
    #print('output_file_is', curr_job_file)
    curr_result_file = open(curr_job_file, "r")
    curr_result_file_contents = curr_result_file.readlines()
    curr_result_output_hd5_string = curr_result_file_contents[-3][13:-1]
    list_hd5_files.append(curr_result_output_hd5_string)

#print(str(list_hd5_files))

directory_output = '/gpfs/slac/staas/fs1/g/exo/exo_data8/exo_data/users/yangrj/chromasim/chroma-simulation/Output/OD_2021/Refl_OC' + str(oc_ref) + '_ST' + str(st_ref)
#list_hd5_files = next(os.walk(directory_output), (None, None, []))[2]  # [] if no file

# Reads in the sample / virgin / template batch submission file.
my_file = open("Anal_Yaml_Template.yml", "r")
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
yaml_name = "Anal_OD_OC" + str(oc_ref) + "_ST" + str(st_ref) + "_v4"

#output_file = open('batch_sim_OC' + str(oc_ref) + '_ST' + str(st_ref) + '_all.sh','w')

line_10_new = "Files: " + str(list_hd5_files)  + ' # TOTAL NUMBER OF FILES: ' + str(len(list_hd5_files)) + '\n'
line_11_new = "OutputFile: '/gpfs/slac/staas/fs1/g/exo/exo_data8/exo_data/users/yangrj/chromasim/chroma-simulation/AnalOutput/Result_Anal_OC" + str(oc_ref) + "_ST" + str(st_ref) + "_v4.txt'\n"

#line_07_new = "#SBATCH --error=batchOut-OC" + str(oc_ref) + "-ST" + str(st_ref) + "/err-output-OC" + str(oc_ref) + "-ST" + str(st_ref) + "-%j.txt" + '\n'
#line_19_new = "OUTDIR='/gpfs/slac/staas/fs1/g/exo/exo_data8/exo_data/users/yangrj/chromasim/chroma-simulation/batchOut-OC" + str(oc_ref) + "-ST" + str(st_ref) + "'\n"

output_file = open('Anal_Yaml_OC' + str(oc_ref) + '_ST' + str(st_ref) + '_v4.yml','w')

for j in file_contents[0:9]:
    output_file.write(j)

output_file.write(line_10_new)
output_file.write(line_11_new)
#output_file.write(line_07_new)

for r in file_contents[11:]:
    output_file.write(r)

#output_file.write(line_19_new)

#for p in file_contents[19:20]:
#    output_file.write(p)

#for i in range(total_nb_files):
#    curr_yaml_file = output_suffix(i,total_nb_files-1) # -1 because indexed from 0...
    
#    line_21_new = "singularity exec --nv -B /gpfs ../Chroma.sif python ./RunSim.py -y Yaml/OD/" + yaml_name + curr_yaml_file + ".yaml\n"
    
#    # Writes the new YAML cards.
#    output_file = open('batch_sim_OC' + str(oc_ref) + '_ST' + str(st_ref) + '_' + curr_yaml_file + '.sh','w')

#    for r in file_contents[0:4]:
#        output_file.write(r)

#    output_file.write(line_05_new)
#    output_file.write(line_06_new)
#    output_file.write(line_07_new)

#    for j in file_contents[7:18]:
#        output_file.write(j)

#    output_file.write(line_19_new)

#    for p in file_contents[19:20]:
#        output_file.write(p)

#    output_file.write(line_21_new)

#    for m in file_contents[21:]:
#        output_file.write(m)

output_file.close()
