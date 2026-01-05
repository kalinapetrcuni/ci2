import sys
from openbabel import pybel


class SmilestoPovConvertor:
    """
    Converts input .smi file with single molecule SMILES and converts it to a .pov file 
    containing the POV-Ray specifiecation of the 3D molecule structure using OpenBabel.
    """
    def __init__(self, cmdline_args):
        self.cmdline_args = cmdline_args
        if len(cmdline_args) == 2: # check if a filename was given as cmdline argument
            self.input_file = cmdline_args[1]
        else:
            raise Exception(f"Please provide exactly 1 source filename as cmdline arguement. e.g. python ala5.py <test>.smi")
        
        
    def convert_to_pov(self):
        """Loads SMILES from self.input_file and converts 3D structure in .pov with the same filename"""        
        
        # load the SMILES from file
        mol = next(pybel.readfile("smi", self.input_file))
        
        # generate 3D coordinates
        mol.make3D()
        
        # optimize with a force field (recommended)
        mol.localopt(forcefield="mmff94")

        # write POV-Ray file
        output_filename = self.input_file.rstrip(".smi") + ".pov"
        mol.write("pov",output_filename, overwrite=True)


if __name__ == "__main__": # check if the code is being called as a script
     app = SmilestoPovConvertor(sys.argv)
     app.convert_to_pov()
