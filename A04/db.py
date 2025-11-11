import sys
import csv
import sqlite3
import re 

class myDatabaseManager:
    """
    Provides functionality for assignment A04. 
    Creates/ connects to database upon instance creation. 
    Fills it with data from csv files provided as cmdline arguments when calling the script.
    Reports the question from assignment and its answer to stdout.
    """
    def __init__(self, script_args):
        connection = sqlite3.connect("db.sqlite") # create/connect to database
        self.connection = connection
        self.cursor = connection.cursor() # get cursor object to issue commands to the database through
        print("Opened connection to database.\n")

        if len(script_args) > 1: # check if source file filenames were passed as parameters
            self.source_files = script_args[1:]
        else:
            self.source_files = None
    

    def _table_exists(self, table_name):
        """Private helper function: Check whether table with given table_name exists in the database."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",(table_name,))
        return self.cursor.fetchone() is not None # check content of cursor for table (None if no object in cursor)


    def _validate_identifier_name(self, identifier_name):
        """Check identifier_name for signs of injection attack. Return identifier if it contains only letters, numbers or underscore else raise error."""
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
        """Check whether tables corresponding to all self.source_files exist ... if not create them and fill with data in source files"""
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
                        raise(Exception(f"Couldn't create database table from {file}. File contains no data to infer column datatypes."))
                    
                    id_in_source_file = False
                    if columns[0].lower() == "id":
                        column_types[0] = "INTEGER PRIMARY KEY"
                        id_in_source_file = True
                    else:
                        columns.insert(0,"ID")
                        column_types.insert(0,"INTEGER PRIMARY KEY")
                    
                    # construct the SQL query to create new table new_table_name
                    column_and_type_str = ""
                    for column_name, column_type in zip(columns, column_types):
                        column_and_type_str += (column_name + " " + column_type + ", ")
                    column_and_type_str = column_and_type_str.rstrip(", ")

                    self.cursor.execute(f"CREATE TABLE {new_table_name} ({column_and_type_str})")
                    
                    # compile data column names into a string
                    data_column_name_str = ", ".join(columns[1:])

                    # generate the right number of value placeholders depending on data columns
                    placeholders = ", ".join("?" for _ in columns[1:])

                    # fill the table with data
                    for row in csv_contents[1:]:
                        if id_in_source_file:
                            self.cursor.execute(f"INSERT INTO {new_table_name} ({data_column_name_str}) VALUES ({placeholders})", row[1:])
                        else:
                            self.cursor.execute(f"INSERT INTO {new_table_name} ({data_column_name_str}) VALUES ({placeholders})", row)

                    print(f"Created table '{new_table_name}'.")

                else:
                    print(f"Table '{file_without_ext}' already exists and was not recreated.")


    def count_Albania_cities(self):
        "Print question, determine the number of Albanian cities in the database and print the result."
        print("\nQ: How many cities in the database are from Albania?")
        if self._table_exists("city") and self._table_exists("country"):
            self.cursor.execute("SELECT Code FROM country WHERE Name='Albania'")
            self.cursor.execute("SELECT COUNT(*) FROM city WHERE CountryCode = ?", (str(self.cursor.fetchall()[0][0]),))
            print(f"A: {self.cursor.fetchall()[0][0]}\n")
        else:
            print("ERROR: Couldn't determine the number of cities. Table 'country' or 'city' is missing in the database. Please provide the corresponding source csv file.")
    
    
    def commit_and_close(self):
        """Commit changes and close connection to database. Wrapper for corresponding methods of sqlite3.Connection"""
        self.connection.commit()
        self.connection.close()
        print("Committed changes and closed connection to database.")


if __name__ == "__main__": # check if the code is being called as a script
     app = myDatabaseManager(sys.argv)
     app.enter_sources()
     app.count_Albania_cities()
     app.commit_and_close()