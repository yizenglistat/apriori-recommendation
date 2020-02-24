Running Python

Python is an interpreted high-level programming language for general-purpose programming. It’s design philosophy emphasizes code readability using significant whitespace. Python features a dynamic type system and automatic memory management. Here is a demonstration of running Python using the job scheduler.

1. First, launch a Python virtual environment by running the commands:
`module load python3/anaconda/5.2.0
conda create --prefix=/work/username/python-environment 
source activate python-environment`
The submission script included in this repository launches the Python virtual environment when run.

2. Create a Python script. This repository provides a simple script, <i>test.py</i>, which demonstrates some of Python’s basic features.

3. Prepare the submission script, which is the script that is submitted to the Slurm scheduler as a job in order to run the Python script. This repository provides the script <i>job.sh</i> as an example.

4. Submit the job using:
`sbatch job.sh`

5. Examine the results.
