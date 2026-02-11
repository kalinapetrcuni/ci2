# A08
This directory contains work related to assignment A08.
It houses a web application using Python Flask to search molecules by SMILES in the Chembl database.

The application as is is intended for development and local use only.

## Instructions to run the application

Expected: Linux shell with Python(version 3.7 or higher) available as `python3`

```bash
# clone the repository
git clone https://github.com/kalinapetrcuni/ci2.git

# create Python virtual enviroment
python3 -m venv .venv

# activate the enviroment
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt

# navigate into the A08 directory
cd ci2/A08

# run the web app
python3 app.py

```

To query Chembl for your molecule enter its canonical SMILES string into the form titled `Enter SMILES:` and press the `Search` button (or ENTER on your keyboard).
The output (and/or possible error messages) will be displayed below the search form.


## Example outputs

entered SMILES: `O=C(O)c1ccc(C(=O)O)cc1`

Output:
```
Compound Information
CHEMBL ID: 	CHEMBL1374420
Preferred Name: 	TEREPHTHALIC ACID
Molecular Formula: 	C8H6O4
Molecular Weight: 	166.13
Canonical SMILES: 	O=C(O)c1ccc(C(=O)O)cc1
InChI: 	InChI=1S/C8H6O4/c9-7(10)5-1-2-6(4-3-5)8(11)12/h1-4H,(H,9,10)(H,11,12)
InChI Key: 	KKEYFWRCBNTPAC-UHFFFAOYSA-N
Molecule Type: 	Small molecule
```
Interestingly enough PubChem uses a slightly different standard for its SMILES than CHEMBL and thus the terephthalic acid SMILES `C1=CC(=CC=C1C(=O)O)C(=O)O` from PubChem will not match the molecule in Chembl 
resulting in the following error from our web app:

> No compound was found for the given SMILES, or the CHEMBL service is currently unavailable. Make sure you are entering CHEMBL canonical (aromatic) SMILES. Othes SMILES dialects might not match the target molecule.

After entering the literal string `terephthalic acid` the following error is shown:

> Invalid input. Please enter valid SMILES