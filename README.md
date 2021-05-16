# codebook-engine

## Overview and a few notes
This program was built and run on windows using the linux subsystem as a shell. 
All commands are linux specific and may not work on powershell or other types of shell applications.

## Install python, pip, and python virtual environment on your system
install python3, venv, and pip using the following command:
    `sudo apt install python3 python3-pip python3-venv`

## Navigate to the project directory
You should now navigate to the root folder of the project 
    called `codebook-engine`
    this folder should contain the following
       * `assets/`
       * `models/`
       * `output/`
       * `src/`
       * `.gitignore`
       * `README.md`
       * `requirements.txt`

## Create a python virtual environment, activate it, and install dependencies
Create a virtual environment (called venv) with the following command:
    `python3 -m venv venv`
Activate the virtual environment using the following command:
    `source venv/bin/activate`
Install project dependencies using the following command:
    `pip install -r requirements.txt`

## Add required assets
Please move the required data into the directory 
    `/codebook-engine/assets/`
If the video filename contains spaces, please rename the file to something without spaces.
My program can't handle them and it was not a high enough prority for me to address that problem.

NOTE: the data I provided to you are the exact same video files you provided, I just renamed them.


## Run the program
run the program with the following command:
    `python3 src/main.py`

## Train a model

## Perform a background subtraction

### Example separate command:
`separate --source sample2.MOV --model rev_a0.7_b1.2.json --out`

## Models

## Output files
