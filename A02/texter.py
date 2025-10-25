import sys


class Texter:
    """
    Implements functionality for task A02, student #5.
    
    Texter.run method:\n
    Prints number of words and number of words starting with a capital letter in the target file to stdout.
    If no target file is given as script argument, prints error message with instructions.
    """
    def __init__(self):
        pass

    def run(self):
        """
        Performs Texter functionality. 
        Prints number of words and number of words starting with a capital letter in the target file to stdout.
        If no target file is given as script argument, prints error message with instructions.
        """
        if __name__ == "__main__":
            if len(sys.argv) > 1:
                script_arg1 = sys.argv[1]

                # read contents of target file
                with open(str(script_arg1), "r") as file:
                    contents = file.read()
                
                # count and print the number of words
                words = contents.split()
                num_words = len(words)
                print(f"Number of words: {num_words}")
                
                # count and print the number of words starting with a capital letter
                cap_start_words = [x for x in words if x[0].isupper()]
                num_cap_start_words = len(cap_start_words)
                print(f"Number of words starting with capital letter: {num_cap_start_words}")
            else:
                no_argument_error = f"\nERROR: No target filename was given\nPlease pass target filename as first argument when calling the script: python texter.py <filename>.txt"
                print(no_argument_error)

# create an instance of the Texter class
my_texter = Texter()

# run the functionality
my_texter.run()