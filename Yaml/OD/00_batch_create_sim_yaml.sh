#!/bin/bash

#BATCH --partition=shared
#
#SBATCH --job-name=splitmuon

conda init bash

python copying_yaml.py
