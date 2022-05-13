#!/bin/bash

#BATCH --partition=shared
#
#SBATCH --job-name=copybatch

source activate chroma

python single_batch_maker.py
