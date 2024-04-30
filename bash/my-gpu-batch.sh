#!/bin/bash

# Tell the system the resources you need. Adjust the numbers according to your need, e.g.
#SBATCH --gres=gpu:1 --cpus-per-task=4 --mail-type=ALL

# If you use Anaconda, initialize it
. ~/anaconda3/etc/profile.d/conda.sh
conda activate unicorn

# cd to your desired directory and execute your program, e.g.
cd ~/unicorn
cuda=0 config=sn_big/chair.yml tag=chair_big_eval ./scripts/pipeline.sh