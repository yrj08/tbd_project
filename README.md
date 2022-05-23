# tbd_project

Repository containing all files for nEXO

## Brief overview

I run OD simulations in two steps: first the photons are simulated, then the analysis is run. Out of memory considerations, the first step is to separate the million muon CSV file (```millionMuon.csv```) into many smaller files. The justification is as the current code parse through the entire CSV file regardless of the number of muons to be simulated, this causes memory issues.

My fix is to split the CSV file into more manageable parts randomly, into predetermined files. When the simulation is ran, it will not end up going through all 330000 muons in the big file. The idea is this should not have too much of an impact on the randomness of the final simulation while being doable.

## Workflow

### 1) Separate ```millionMuon.csv``` into smaller parts

blah blah


### 2) Generation of "simulation" YAML cards (Mostly ```YAML/OD``` folder).

Each individual simulation needs its own YAML card. This YAML card will later be referenced by its corresponding batch job, which will be run. The below scripts/files are useful for such a task:

x

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
- Line 21: ```singularity exec --nv -B /gpfs ../../../../Chroma.sif python ./RunSim.py -y Yaml/OD/OD_OC00_ST00.yaml``` The actual command. Calls YAML cards named ```Yaml/OD/OD_OCxx_STyy_v4_zz.yaml```, where ```xx``` is the OC reflectivity value, ```yy``` is the ST reflectivity value, and ```zz``` is the index of the YAML card. The generation of those YAML cards are outlined in the section above.

##### ```copying_batch.py```

Makes the individual batch job submission files that each submits a portion of the tasks for a given reflectivity configuration.

**Input**: OC and ST reflectivity values. _Note_: input method is to be improved: currently the two variables are hard-coded at the beginning of the file, with the modification of those two lines necessary each time a new value is desired. There must be a better way, but ```input()``` function didn't do the trick.

**Dependencies**: ```batch_sim_template.sh``` is required as a template to create the ```.sh``` files.

**Output files**: ```batch_sim_OCxx_STyy_zz.sh``` where ```xx```, ```yy``` are OC/ST reflectivity values, and ```zz``` again the index of the output files.

**Modified lines**: 5, 6, 7, 19, 21 as outlined in the previous section.

##### ```00_batch_create_sim_sh.sh```

Simply runs ```copying_batch.py```. Kind of an unnecessary file.

##### ```single_batch_maker.py```

Makes a batch job that runs all individual batch job files of a given reflectivity configuration. Useful for big number of files.

**Input**: OC refl. value, ST refl. value, number of files. Note: similar to the above, the OC/ST refl. value input methods may need improvement. Also number of file is the total number of batch files, thus it is important to not modify the indices to have gaps. The ```copying_batch.py``` should make sure the output files are consetively indexed.

**Output**: one big ```.sh``` file named ```batch_sim_OCxx_STyy_all.sh``` where similar to the above ```xx``` and ```yy``` are OC and ST refl. values respectively. This single .sh file can simply be run by a ```sbatch``` command.

### 3) Generation of "Analysis" batch job / YAML cards.
4) more?


