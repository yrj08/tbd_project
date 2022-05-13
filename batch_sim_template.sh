#!/bin/bash

#BATCH --partition=shared
#
#SBATCH --job-name=RJRF0000
#SBATCH --output=batchOut/output-OC00_ST00-%j.txt
#SBATCH --error=batchOut/err-output-OC00-ST00-%j.txt
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem-per-cpu=12g
#
#SBATCH --time=2-00:00:00
#
#SBATCH --gpus=geforce_rtx_2080_ti:1 
date
startTime=$(date +"%s")

OUTDIR='/gpfs/slac/staas/fs1/g/exo/exo_data8/exo_data/users/yangrj/chromasim/chroma-simulation/Yaml/OD/OD_OC00_ST00/batchOut/'

singularity exec --nv -B /gpfs ../../../../Chroma.sif python ./RunSim.py -y Yaml/OD/OD_OC00_ST00.yaml
endTime=$(date +"%s")
echo "Simulation complete, total run time:"
date -u -d "0 $endTime seconds - $startTime seconds" +"%H:%M:%S"
