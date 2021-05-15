# codebook-engine

separate --source sample2.MOV --model rev_a0.7_b1.2.json --out

to run this program follow these steps:


add the test video files into the assets folder, also please remove all spaces from the file name.

create a python virtual environment and activate it
    and install dependencies with 'pip3 install -r requirements.txt'

else
    install opencv with 'pip3 install opencv-python'

run the program with python3 src/main.py

if the program doesnt run, check codebook_engine.py and change the file it's looking for you your asset file.
