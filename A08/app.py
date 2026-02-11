"""
Flask web application for querying CHEMBL compound information by SMILES.
"""

from flask import Flask, render_template, request
from chemistry_api import get_compound_by_smiles
from rdkit import Chem

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    compound = None
    error_message = None
    smiles_input = ""

    if request.method == "POST":
        smiles_input = request.form.get("smiles", "").strip()

        if not smiles_input:
            error_message = "Please enter a SMILES string."
        else:
            # check SMILES validity using RDkit
            if Chem.MolFromSmiles(smiles_input) is None:
                error_message = "Invalid input. Please enter valid SMILES"
            else:
                # query database
                result = get_compound_by_smiles(smiles_input)

                if result is None:
                    error_message = (
                        "No compound was found for the given SMILES, "
                        "or the CHEMBL service is currently unavailable. "
                        "Make sure you are entering CHEMBL canonical (aromatic) SMILES. " 
                        "Othes SMILES dialects might not match the target molecule."
                    )
                else:
                    compound = result

    return render_template(
        "index.html",
        compound=compound,
        error_message=error_message,
        smiles_input=smiles_input,
    )


if __name__ == "__main__":
    app.run(debug=False)
