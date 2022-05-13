#!/bin/bash

#BATCH --partition=shared
#
#SBATCH --job-name=Anal0000
#SBATCH --output=Anal_batchOut-OC00-ST00/AnalOut-OC00-ST00-%j.txt
#SBATCH --error=Anal_batchOut-OC00-ST00/err-AnalOut-OC00-ST00-%j.txt
#
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem-per-cpu=8g
#
#SBATCH --time=1:00:00
#
#SBATCH --gpus 1 

date
startTime=$(date +"%s")

OUTDIR='/gpfs/slac/staas/fs1/g/exo/exo_data8/exo_data/users/yangrj/chromasim/chroma-simulation/Anal_batchOut-OC00-ST00/'

CHROMADIR='/gpfs/slac/staas/fs1/g/exo/exo_data8/exo_data/users/yangrj/chromasim/chroma-simulation' 

cd $CHROMADIR

conda init bash

source activate chroma

#runs the analysis functions on the h5 file requested, currently set up to run in the chromasimulation home direcory, not from this folder. 
python Analysis/ODAnalysis/ODLightMap.py -y Yaml/OD/Anal_OC00_ST00.yml

endTime=$(date +"%s")
echo "Analysis complete, total run time:"
date -u -d "0 $endTime seconds - $startTime seconds" +"%H:%M:%S"
