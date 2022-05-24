"""
Created on Fri Mar 25 21:26:17 2022
@author: Ruijia Yang
"""

# This is intended for a stopgap measure, while the analysis file array error is being figured out.
# For the moment, simulations will save all variables to be able to run the analysis codes.

# This file aims to split the "millionMuons.csv" into many smaller files, each containing 100 muons,
# selected at random. No two files will share common muons. It performs the following:

# 1. It peruses through the big muon file, and randomly assign muons to different files, such that
# each files has 100 random muons drawn without replacement.

# 2. It outputs the muon files, as millionMuons_split100_##.csv

number_muon_file = 1000

import pandas as pd
import random
import math

# Imports the big muon file
muon_input_csv = pd.read_csv('millionMuons.csv', sep=",", header=0)

# List of valid muon ID's
list_muon_ids = list(muon_input_csv['Muon#'].to_numpy())

# Reshuffle the list in random order
random.shuffle(list_muon_ids)

# Number of full 100-muon files that can be made. It cannot deal with  input files less than 100
# muons and I won't be writing codes for it since this is supposed to be a temporary code.
number_complete_files = math.floor(len(list_muon_ids)/number_muon_file)

def output_suffix(curr_index, max_nb_files):
    """
    Generates the string needed to save multi-part files. For example,
    saving file 9 of 302 would generate suffix "009".
    """
    if (len(str(curr_index)) < len(str(max_nb_files))):
        return '0'*(len(str(max_nb_files)) - len(str(curr_index))) + str(curr_index)
    else:
        return str(curr_index)
    
# Generates the individual files and save them
for j in range(number_complete_files):
    list_taken_ids = list_muon_ids[j*number_muon_file:j*number_muon_file+number_muon_file]
    output_muon_file = muon_input_csv[muon_input_csv['Muon#'].isin(list_taken_ids)]
    output_muon_file.to_csv('millionMuons_' + str(number_muon_file) + '_part_' + output_suffix(j, number_complete_files) + '.csv',index=False)
