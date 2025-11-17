import sys
import glob
import re
import os
import warnings
from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs
from rdkit.Chem import rdFingerprintGenerator
import numpy as np

class cdxml2sdfConverter:
    """
    Implements functionality for task A05.
    Take input filenames and optionally output filename (default cdxml2sdf.sdf) from cmdline arguments.
    Convert all molecules from input cdxml files into a single sdf file.
    Print the original filenames of the 2 most similar molecules according to Tanimoto along with the similarity value.
    """
    def __init__(self, script_args):
        self.molecules = {} # dict to store molecule extracted from individual inputs
        if len(script_args) > 1: # check if source file filenames were passed as parameters
            self.input_files = self._filter_cdxml(self._resolve_output_filename(self._expand_arg_wildcards(script_args[1:])))
        else:
            raise Exception(f"No input file was given.\nSpecify input files in cmdline arguments (bash style wildcards supported).\n e.g. python cdxml2sdf.py <input_filename1>")
    

    def generate_output_sdf(self):
        """
        Combine contents of input CDXML files into a single .sdf file given by self.output_file. 
        Report skipped files in case of reading issues.
        """
        writer = Chem.SDWriter(self.output_file)

        for file in self.input_files:
            try:
                mols = Chem.rdmolfiles.MolsFromCDXMLFile(file, sanitize=False, removeHs=False)
            except Exception as e:
                print(f"[ERROR] Failed to parse {file}: {e}")
                continue

            for mol in mols:
                writer.write(mol)
                if file in self.molecules:
                    self.molecules[file] = self.molecules[file].append(mol)
                else:
                    self.molecules[file] = [mol]
        writer.close()
        print(f"\nWrote output to {self.output_file}\n")


    def analyze_similarities_in_output(self):
        """
        Find the 2 most similar molecules according to Tanimoto coming from the input files. 
        Print the filenames they originated from and the similarity value.
        """
        print("\nInialized molecular similarity analysis:")
        # Load molecules in conversion output (excluded invalid entries)
        mols = [self.molecules[original_input_file][0] for original_input_file in self.input_files if self.molecules[original_input_file] is not None]
        sanitized_mols = []
        for idx,mol in enumerate(mols):
            try:
                Chem.SanitizeMol(mol)  # Fix valences, assign implicit Hs, aromatize, etc.
                mol.UpdatePropertyCache(strict=False)  # ensure atom properties are set
                sanitized_mols.append(mol)
            except Exception as e:
                print(f"Skipping molecule from file {self.input_files[idx]} due to sanitization error: {e}")

        # Compute fingerprints
        morgan_gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
        fps = [morgan_gen.GetFingerprint(mol) for mol in sanitized_mols]

        # Compute similarity matrix all against all
        n = len(fps)
        similarity_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(i, n):
                sim = DataStructs.TanimotoSimilarity(fps[i], fps[j])
                similarity_matrix[i, j] = sim
                similarity_matrix[j, i] = sim  # fill half of the matrix based on symmetry
        
        # find the 2 most similar
        np.fill_diagonal(similarity_matrix, -1) # exclude self similarity
        max_idx = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)
        i, j = max_idx

        # convert to filenames from which the similar molecules originated
        file_i = self.input_files[i]
        file_j = self.input_files[j]
        similarity_value = similarity_matrix[i,j]
        print(f"\nMost similar molecules are from files: {file_i}, {file_j} \nSimilarity: {similarity_value}")


    def _expand_arg_wildcards(self, args):
        """
        Internal helper method: Return a list of relative paths to all targeted files. 
        Including ones resulting from wildcards in arguments.
        """
        expanded = []
        for a in args:
        # If the argument contains wildcard characters, expand it
            if any(ch in a for ch in ["*", "?", "["]):
                expanded_files = glob.glob(a)
                expanded.extend(expanded_files)
            else:
                expanded.append(a)
        return expanded


    def _resolve_output_filename(self, argument_files):
        """
        Resolve and assign the output_file attribute based on cmdline arguments. 
        Return arguments without output specification (only inputs).
        """
        output_file = ""
        output_file_pattern = re.compile(r".*\.sdf$") # regex to match any .sdf file
        for file in argument_files:
            if output_file_pattern.match(file):
                if output_file:
                    raise Exception("Too many output files specified. Specify at most one .sdf file in the cmdline arguments (default: cdxml2sdf.sdf)")
                else:
                    output_file += file
                    argument_files.remove(output_file) # remove the newly found output filename from the list of input files
        if output_file:
            if os.path.isfile(output_file):
                warnings.warn(f"The specified output {output_file} already exists. The default cdxml2sdf.sdf was used instead.", UserWarning)
                self.output_file = "cdxml2sdf.sdf"
            else:
                self.output_file = output_file 
        else:
            self.output_file = "cdxml2sdf.sdf" # none specified use default output
        return argument_files


    def _filter_cdxml(self, argument_files):
        input_file_pattern = re.compile(r".*\.cdxml$") # regex to match any .cdxml file
        for file in argument_files:
            if not input_file_pattern.match(file):
                raise Exception(f"Invalid input file specified: {file}\nOnly .cdxml files accepted as input.")
        return(argument_files)



if __name__ == "__main__": # check if the code is being called as a script
     app = cdxml2sdfConverter(sys.argv)
     app.generate_output_sdf()
     app.analyze_similarities_in_output()

