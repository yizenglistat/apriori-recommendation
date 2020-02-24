#!/bin/sh
#SBATCH -o pyjob%j.out
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -p defq
#SBATCH --exclude=node[174-238]

# creates a python virtual environment 
module load python3/anaconda/5.2.0
#conda create -n python-environment python-essentials python-base
#source activate python-environment

# run python script

python3 apriori.py browsingdata.txt 100 1000

# exit the virtual environment
#source deactivate
