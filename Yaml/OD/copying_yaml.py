import random

#print('Input outer cryostat reflectivity: ')
#oc_ref = input()

#print('Input stainless steel reflectivity: ')
#st_ref = input()

oc_ref = "60"
st_ref = "40"
total_nb_files = 10
muon_files = 347
muon_per_file = 1000
muon_file_base = "millionMuons_" + str(muon_per_file) + "_part_"

# Reads in the input YAML file.
my_file = open("OD_Yaml_Template.yaml", "r") #open("OD_Yaml_Template.yaml", "r")
file_contents = my_file.readlines()

# Generate a list of random muon files to use.
random_list = random.sample(range(muon_files), total_nb_files)

def output_suffix(curr_index, max_nb_files):
    """
    Generates the string needed to save multi-part files. For example,
    saving file 9 of 302 would generate suffix "009".
    """
    if (len(str(curr_index)) < len(str(max_nb_files))):
        return '0'*(len(str(max_nb_files)) - len(str(curr_index))) + str(curr_index)
    else:
        return str(curr_index)
    
curr_count = 0

line_38_new = "  NumberOfPhotons: " + str(muon_per_file) + "                      # number of photons per event\n"

for i in random_list:
    i_suffix = output_suffix(i,muon_files-1)
    
    new_optical_properties = 'OptProp_OC' + str(oc_ref) + '_ST' + str(st_ref) + '.yaml'
    new_muon_file = muon_file_base + i_suffix + '.csv'
    
    line_12_new = "  OpticalProperties: '/gpfs/slac/staas/fs1/g/exo/exo_data8/exo_data/users/yangrj/chromasim/chroma-simulation/Yaml/OD/" + new_optical_properties + "' # Location of YAML card that contains optical properties\n"
    line_37_new = "  Generator: MuonInput='/gpfs/slac/staas/fs1/g/exo/exo_data8/exo_data/users/yangrj/chromasim/chroma-simulation/Data/OD/" + new_muon_file + "' #Beam, -Z #Flashlight, 1.0                # Where and how the photons are generated - to add muon stuff here\n"
    line_44_new = "  OutputPath: '/gpfs/slac/staas/fs1/g/exo/exo_data8/exo_data/users/yangrj/chromasim/chroma-simulation/Output/OD_2021/Refl_OC" + str(oc_ref) + "_ST" + str(st_ref) + "/' # Location where simulation data is saved\n" 
    line_45_new = "  OutputFilename: OD_Refl_OC" + str(oc_ref) + "_ST" + str(st_ref) + "_v4                 # Additional string variable to name current study\n"

    curr_output_id = output_suffix(curr_count, total_nb_files-1)
    
    # Writes the new YAML card.
    output_file = open('OD_OC' + str(oc_ref) + '_ST' + str(st_ref) + '_v4_' + curr_output_id + '.yaml','w')

    for j in file_contents[0:11]:
        output_file.write(j)
    output_file.write(line_12_new)
    for k in file_contents[12:36]:
        output_file.write(k)
    output_file.write(line_37_new)
    output_file.write(line_38_new)
    for m in file_contents[38:43]:
        output_file.write(m)
    output_file.write(line_44_new)
    output_file.write(line_45_new)
    for n in file_contents[45:]:
        output_file.write(n)
        
    curr_count += 1
