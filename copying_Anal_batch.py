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
#total_nb_files = 10

# Reads in the sample / virgin / template batch submission file.
my_file = open("batch_Anal_template.sh", "r")
file_contents = my_file.readlines()

# Part of the name of YAML file (without prefix) that will be imported
yaml_name = "Anal_Yaml_OC" + str(oc_ref) + "_ST" + str(st_ref) + "_v4"

# batch_Anal_OC00_ST00_v4

output_file = open('batch_Anal_OC' + str(oc_ref) + '_ST' + str(st_ref) + '_v4.sh','w')

line_05_new = "#SBATCH --job-name=RJAN" + str(oc_ref) + str(st_ref) + '\n'
line_06_new = "#SBATCH --output=Anal_batchOut-OC" + str(oc_ref) + "-ST" + str(st_ref) + "/AnalOut-OC" + str(oc_ref) + "-ST" + str(st_ref) + "-%j.txt" + '\n'
line_07_new = "#SBATCH --error=Anal_batchOut-OC" + str(oc_ref) + "-ST" + str(st_ref) + "/err-AnalOut-OC" + str(oc_ref) + "-ST" + str(st_ref) + "-%j.txt" + '\n'
line_20_new = "OUTDIR='/gpfs/slac/staas/fs1/g/exo/exo_data8/exo_data/users/yangrj/chromasim/chroma-simulation/Anal_batchOut-OC" + str(oc_ref) + "-ST" + str(st_ref) + "'\n"

for j in file_contents[0:4]:
    output_file.write(j)

output_file.write(line_05_new)
output_file.write(line_06_new)
output_file.write(line_07_new)

for r in file_contents[7:19]:
    output_file.write(r)

output_file.write(line_20_new)

for p in file_contents[20:30]:
    output_file.write(p)

#for i in range(total_nb_files):
#    curr_yaml_file = output_suffix(i,total_nb_files-1) # -1 because indexed from 0...
    
line_31_new = "python Analysis/ODAnalysis/ODLightMap.py -y Yaml/OD/" + yaml_name + ".yml\n"
 
# Anal_Yaml_OC00_ST00_v4.yml
   
#    # Writes the new YAML cards.
#    output_file = open('batch_Anal_OC' + str(oc_ref) + '_ST' + str(st_ref) + '_' + curr_yaml_file + '.sh','w')

#    for r in file_contents[0:4]:
#        output_file.write(r)

#    output_file.write(line_05_new)
#    output_file.write(line_06_new)
#    output_file.write(line_07_new)

#    for j in file_contents[7:19]:
#        output_file.write(j)

#    output_file.write(line_20_new)

#    for p in file_contents[20:30]:
#        output_file.write(p)

output_file.write(line_31_new)

#    for m in file_contents[31:]:
#        output_file.write(m)

output_file.close()
