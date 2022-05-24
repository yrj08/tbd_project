# tbd_project

Repository containing all files for nEXO

## Brief overview

I run OD simulations in two steps: first the photons are simulated, then the analysis is run. Out of memory considerations, the first step is to separate the million muon CSV file (```millionMuon.csv```) into many smaller files. The justification is as the current code parse through the entire CSV file regardless of the number of muons to be simulated, this causes memory issues.

My fix is to split the CSV file into more manageable parts randomly, into predetermined files. When the simulation is ran, it will not end up going through all 330000 muons in the big file. The idea is this should not have too much of an impact on the randomness of the final simulation while being doable.

## Workflow

### 1) Separation of ```millionMuon.csv``` into smaller parts (```Data/OD``` folder).

##### ```Data/OD/Splitting_Muon_File.py```

Splits the "millionMuons.csv" into many smaller files, each containing 100 muons, selected at random. No two files will share common muons. It 1) peruses through the big muon file, and randomly assign muons to different files, such that each files has 100 random muons drawn without replacement 2) It outputs the muon files, as ```millionMuons_split100_##.csv```.

**Output**: many many small csv files that is more manageable to use

##### ```Data/OD/batch_splitting_muon.sh```

Basically a batch script to run the above python script.

### 2) Generation of "simulation" YAML cards (```YAML/OD``` folder).

Each individual simulation needs its own YAML card. This YAML card will later be referenced by its corresponding batch job, which will be run. The below scripts/files are useful for such a task:

##### ```Yaml/OD/OD_Yaml_Template.yaml```

YAML card specifying the details of the simulation (reflectivity, surfaces, whatnot). Is duplicated and modified by ```Yaml/OD/copying_yaml.py```.

##### ```Yaml/OD/copying_yaml.py```

Modifies the template YAML card above. 

**Input**: OC / ST refl. value; Total number of muon files wanted, total number of muon files (all files result of splitting the millionMuon.csv), and muons per split csv file. As outlined above, this is currently hard coded.

**Lines modified**: 12 (optical properties), 37 (generator, i.e. source muon file), 38 (Number of photons), 44 (output path), 45 (output file name) to return many files named ```OD_OCxx_STyy_v4_zz.yaml```.

##### ```Yaml/OD/00_batch_create_sim_yaml.sh```

Runs the above ```copying_yaml.py``` script. Use of this is optional

### 3) Generation of "simulation" batch files.

The below create batch files which refer to YAML cards outlined above.

#### Relevant files

##### ```batch_sim_template.sh``` 

Template ```.sh``` file to be modified for each simulation

Notable lines that will be modified by ```copying_batch.py```, outlined here for clarity:
- Line 5: ```#SBATCH --job-name=RJRF0000``` The name of the job, 0000 means OC 0% and ST 0%, will be automatically modified depending on the input in ```copying_batch.py``` 
- Line 6: ```#SBATCH --output=batchOut/output-OC00_ST00-%j.txt``` The output ```txt``` file location, can be changed at your own leisure I suppose
- Line 7: ```#SBATCH --error=batchOut/err-output-OC00-ST00-%j.txt``` Error output file location, »
- Line 19: ```OUTDIR='/gpfs/slac/staas/fs1/g/exo/exo_data8/exo_data/users/yangrj/chromasim/chroma-simulation/Yaml/OD/OD_OC00_ST00/batchOut/'``` The output directory, »
- Line 21: ```singularity exec --nv -B /gpfs ../../../../Chroma.sif python ./RunSim.py -y Yaml/OD/OD_OC00_ST00.yaml``` The actual command. Calls YAML cards named ```Yaml/OD/OD_OCxx_STyy_v4_zz.yaml```, where ```xx``` is the OC reflectivity value, ```yy``` is the ST reflectivity value, and ```zz``` is the index of the YAML card. The generation of those YAML cards are outlined in the section above. The YAML cards in ```Yaml/OD``` folder are also needed. This is explained further down the page.

##### ```copying_batch.py```

Makes the individual batch job submission files that each submits a portion of the tasks for a given reflectivity configuration.

**Input**: OC and ST reflectivity values. _Note_: input method is to be improved: currently the two variables are hard-coded at the beginning of the file, with the modification of those two lines necessary each time a new value is desired. There must be a better way, but ```input()``` function didn't do the trick.

**Dependencies**: ```batch_sim_template.sh``` is required as a template to create the ```.sh``` files.

**Output files**: ```batch_sim_OCxx_STyy_zz.sh``` where ```xx```, ```yy``` are OC/ST reflectivity values, and ```zz``` again the index of the output files.

**Modified lines**: 5, 6, 7, 19, 21 as outlined in the previous section.

##### ```00_batch_create_sim_sh.sh```

Simply runs ```copying_batch.py``` above. Kind of an unnecessary file.

##### ```single_batch_maker.py```

Makes a batch job that runs all individual batch job files of a given reflectivity configuration. Useful for big number of files.

**Input**: OC refl. value, ST refl. value, number of files. Note: similar to the above, the OC/ST refl. value input methods may need improvement. Also number of file is the total number of batch files, thus it is important to not modify the indices to have gaps. The ```copying_batch.py``` should make sure the output files are consetively indexed.

**Output**: one big ```.sh``` file named ```batch_sim_OCxx_STyy_all.sh``` where similar to the above ```xx``` and ```yy``` are OC and ST refl. values respectively. This single .sh file can simply be run by a ```sbatch``` command.

##### ```00_batch_make_master_batch.sh```

Simply runs ```single_batch_maker.py``` described above. May also be rather pointless.

### 4) Generation of "Analysis" YAML cards (```Yaml/OD``` folder)

##### ```Yaml/OD/Anal_Yaml_Template.yml``` 

Template YAML card that will be copied and modified to run analysis scripts.

##### ```Yaml/OD/copying_anal_yaml.py```

Python script to generate analysis YAML cards. 

**Input** hard-coded into the code for the moment: a list of job IDs that we want to analyze. Very important to not get mixed up... also make sure the save file names are consistent.

Changes lines 10-11 of the YAML template above: 
- Line 10: list of files (depends on the list of Job IDs);
- Line 11: output file location/path.

### 5) Generation of "Analysis" batch job files.

##### ```batch_Anal_template.sh```

Template ```.sh``` file to be modified for each analysis.

Notable lines that will be modified by ```copying_Anal_batch.py```, outlined here for clarity:
- Line 5: ```#SBATCH --job-name=Anal0000``` The name of the job, 0000 means OC 0% and ST 0%, will be automatically modified depending on the input in ```copying_batch.py``` 
- Line 6: ```#SBATCH --output=Anal_batchOut-OC00-ST00/AnalOut-OC00-ST00-%j.txt``` The output ```txt``` file location, can be changed at your own leisure I suppose
- Line 7: ```#SBATCH --error=Anal_batchOut-OC00-ST00/err-AnalOut-OC00-ST00-%j.txt``` Error output file location, »
- Line 20: ```OUTDIR='/gpfs/slac/staas/fs1/g/exo/exo_data8/exo_data/users/yangrj/chromasim/chroma-simulation/Anal_batchOut-OC00-ST00/'``` The output directory, »
- Line 31: ```python Analysis/ODAnalysis/ODLightMap.py -y Yaml/OD/Anal_OC00_ST00.yml``` The actual command.

##### ```copying_Anal_batch.py```

Makes the individual analysis batch job submission files for a given reflectivity configuration.

**Input**: OC and ST refl. values. See note above for remark on possible input method improvement.

**Dependencies**: ```batch_Anal_template.sh``` is required as a template to create the ```.sh``` files.

**Output file**: ```batch_Anal_OCxx_STyy_v4.sh``` where ```xx```, ```yy``` are OC/ST reflectivity values

**Modified lines**: 5, 6, 7, 20, 31, as outlined above

### Main modifications needed:
- Better input method: 
- 1) the OC/ST refl. values need a better input method rather than being hard-coded into the scripts. The value need to be consistent for all files with them coded in.
- 2) when running the analysis, the list of job IDs need to be manually put in due to the way the files are output (by appending job ID into the file name). There may be a better fix.
- There are lots of commented out garbage codes (my had habit!) that should be taken out or simplified.
