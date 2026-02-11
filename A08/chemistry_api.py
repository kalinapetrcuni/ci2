"""
chemistry_api.py

CHEMBL access layer for querying compound information by SMILES.
"""

from chembl_webresource_client.new_client import new_client
from typing import Optional, Dict


def get_compound_by_smiles(smiles: str) -> Optional[Dict]:
    """
    Query CHEMBL for a compound matching the given SMILES string.

    Parameters
    ----------
    smiles : str
        SMILES representation of the compound.

    Returns
    -------
    dict or None
        Dictionary with selected compound information for the first result,
        or None if no compound is found or an error occurs.
    """

    if not smiles or not smiles.strip():
        print("SMILES input was empty or contained only whitespace")
        return None

    try:
        molecule = new_client.molecule

        # Query CHEMBL by SMILES
        results = molecule.filter(smiles=smiles)

        # get the first result if available
        first = next(iter(results), None)
        if first is None:
            print("first was None")
            return None

        # Extract relevant fields
        compound_data = {
            "chembl_id": first.get("molecule_chembl_id"),
            "preferred_name": first.get("pref_name"),
            "molecular_formula": first.get("molecule_properties", {}).get("full_molformula"),
            "molecular_weight": first.get("molecule_properties", {}).get("full_mwt"),
            "canonical_smiles": first.get("molecule_structures", {}).get("canonical_smiles"),
            "inchi": first.get("molecule_structures", {}).get("standard_inchi"),
            "inchi_key": first.get("molecule_structures", {}).get("standard_inchi_key"),
            "molecule_type": first.get("molecule_type"),
        }

        return compound_data

    except Exception as e:
        # Any network, API, or parsing error is handled gracefully
        print("API call failed with the following exception: {e}")
        return None
