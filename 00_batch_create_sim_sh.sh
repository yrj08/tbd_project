#!/bin/bash

#BATCH --partition=shared
#
#SBATCH --job-name=copybatch

conda init bash

python copying_batch.py
