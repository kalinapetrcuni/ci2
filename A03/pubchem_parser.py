# the tag is <iupacname>
import sys 
from bs4 import BeautifulSoup as bs

class PubchemParser:
    """
    Implements functionality for task A03, student #5.
    
    PubchemParser.run method:\n
    Parse PubChem search result in .xml format given as first script argument and print IUPAC names of compounds to stdout.
    If no target file is given as script argument, print error message with instructions.
    """
    def __init__(self):
        pass

    def run(self):
            """
            Parse PubChem search result in .xml format given as first script argument and print IUPAC names of compounds to stdout.
            If no target file is given as script argument, print error message with instructions.
            """
            if __name__ == "__main__":
                if len(sys.argv) > 1:
                    script_arg1 = sys.argv[1]

                    # open file and parse it with beautifulsoup
                    with open(str(script_arg1), "r") as file:
                        dom = bs(file, "lxml-xml")
                    
                    # iterate over all <iupacname> tags in the XML and print each one's contents
                    for name in dom.find_all("iupacname"):
                         print(name.text)

                else:
                    no_argument_error = f"\nERROR: No target filename was given.\nPlease pass target filename as first argument when calling the script: python pubchem_parser.py <filename>.xml"
                    print(no_argument_error)

myParser = PubchemParser()
myParser.run()