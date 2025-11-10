import sys
import csv
import sqlite3
import re 

class myDatabaseManager:
    """
    TODO: description
    """
    def __init__(self, script_args):
        connection = sqlite3.connect("db.sqlite") # create/connect to database
        self.connection = connection
        self.cursor = connection.cursor() # get cursor object to issue commands to the database through
        print("Opened connection to database.")

        if len(script_args) > 1: # check if source file filenames were passed as parameters
            self.source_files = script_args[1:]
        else:
            self.source_files = None
    

    def _table_exists(self, table_name):
        """Private helper function: Check whether table with given table_name exists in the database."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",(table_name,))
        return self.cursor.fetchone() is not None # check whether the cursor found a matching table and return corresponding Boolean


    def _create_table(self, table_name):
        """Private helper function: Create a table with given table_name in the database."""
        self.cursor.execute() #TODO: table creation


    def _validate_identifier_name(self, identifier_name):
        """Check identifier_name for signs of injection attack. Return identifier if it contains only letters, numbers or _ else raise error."""
        safe_pattern_re = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*$') # regex for safe identifier names
        if not isinstance(identifier_name, str) or not safe_pattern_re.match(identifier_name):
            raise ValueError(f"Input led to invalid identifier name: {identifier_name!r}")
        else:
            return identifier_name


    def _infer_column_datatypes(self,data_row):
        """Infer datatypes of columns from a row of data. Return list of SQL datatype specifiers (e.g. INTEGER, TEXT, REAL)"""
        INTEGER_RE = re.compile(r'^[+-]?\d+$') # Matches an integer (optional leading + or -)
        REAL_RE = re.compile(r'^[+-]?(\d+\.\d*|\.\d+|\d+)([eE][+-]?\d+)?$') # Matches a real/float number (decimal or scientific notation)
        
        column_types = []
        for entry in data_row:
            if INTEGER_RE.match(entry):
                column_types.append("INTEGER")
            elif REAL_RE.match(entry):
                column_types.append("REAL")
            else:
                column_types.append("TEXT")
        return(column_types)


    def enter_sources(self):
        """Check whether tables corresponding to all self.source_files exist ... if not create them."""
        if self.source_files != None:
            for file in self.source_files:
                file_without_ext = file.split(".")[0]

                if not self._table_exists(file_without_ext):
                    new_table_name = self._validate_identifier_name(file_without_ext)

                    with open(file,"r", encoding="utf-8") as f:
                        reader = csv.reader(f,delimiter=";")
                        csv_contents = list(reader)
                    columns = []
                    for tentative_column in csv_contents[0]:
                        columns.append(self._validate_identifier_name(tentative_column))
                    
                    if len(csv_contents) >1:
                        column_types = self._infer_column_datatypes(csv_contents[1])
                    else:
                        raise(Exception(f"Couldn't create database table from {file}. File contains no data to infer column types."))
                    
                    if columns[0].lower() == "id":
                        column_types[0] = "INTEGER PRIMARY KEY"
                    else:
                        columns.insert(0,"ID")
                        column_types.insert(0,"INTEGER PRIMARY KEY")
                    
                    column_string = ""
                    for column_name, column_type in zip(columns, column_types):
                        column_string += (column_name + " " + column_type + ", ")
                    column_string = column_string.rstrip(", ")

                    self.cursor.execute(f"CREATE TABLE {new_table_name} ({column_string})")
                    # TODO: fill tables with data
                    print(f"Created table '{new_table_name}'.")

                else:
                    print(f"Table '{file_without_ext}' already exists and was not recreated.")


    def commit_and_close(self):
        """Commit changes and close connection to database. Wrapper for corresponding methods of sqlite3.Connection"""
        self.connection.commit()
        self.connection.close()
        print("Committed changes and closed connection to database.")
    
    # TODO: Albania cities method



if __name__ == "__main__": # check if the code is being called as a script
     app = myDatabaseManager(sys.argv)
     app.enter_sources()
     app.commit_and_close()