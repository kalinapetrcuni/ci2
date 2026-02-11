from chemistry_api import get_compound_by_smiles

molecule = get_compound_by_smiles("C1=CC(=CC=C1C(=O)O)C(=O)O")

print(molecule)
