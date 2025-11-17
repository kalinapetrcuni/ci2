# A05
This directory contains my solution of the task A05.

## Functionality:
The main script `cdxml2sdf.py` takes input cdxml files and an optional sdf output file specification from commandline arguments.
It compiles all the molecules from input cdxml files into one output sdf and finds the most similar molecules according to Tanimoto reporting the cdxml files they originated from and their similarity value to stdout.

## Running the script (on Windows)

Clone this repository:
`git clone https://github.com/kalinapetrcuni/ci2.git`

Create a Python venv virtual enviroment:
`python -m venv <name_of_your_enviroment>`

Activate the enviroment:
`<path_to_your_enviroment>\Scripts\activate.bat`

Install required packages:
`pip install -r requirements.txt`

Run the script:
Navigate into the `A05` directory within the repository.
`python cdxml2sdf.py <input_file1>.cdxml <output>.sdf`
There can be multiple input files specified (bash style wildcards are supported). The output specification is optional (default:`cdxml2sdf.sdf`).

e.g. `python cdxml2sdf.py *.cdxml` treats all cdxml files in the directory as input and writes to the default output file
