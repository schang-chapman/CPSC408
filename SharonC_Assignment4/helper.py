# module contains miscellaneous functions
from db_operations import db_operations

db_ops = db_operations("../Databases/chinook/chinook.db")

class helper():
    # function parses a string and converts to appropriate type
    @staticmethod
    def convert(value):
        types = [int,float,str] # order needs to be this way
        if value == '':
            return None
        for t in types:
            try:
                return t(value)
            except:
                pass

    # function reads file path to clean up data file
    @staticmethod
    def data_cleaner(path):
        with open(path,"r",encoding="utf-8") as f:
            data = f.readlines()

        data = [i.strip().split(",") for i in data]
        data_cleaned = []
        for row in data[:]:
            row = [helper.convert(i) for i in row]
            data_cleaned.append(tuple(row))
        return data_cleaned

    # function checks for user input given a list of choices
    @staticmethod
    def get_choice(lst):
        choice = input("Enter choice number: ")
        while choice.isdigit() == False:
            print("Incorrect option. Try again")
            choice = input("Enter choice number: ")

        while int(choice) not in lst:
            print("Incorrect option. Try again")
            choice = input("Enter choice number: ")
        return int(choice)

    # function prints a list of strings nicely
    @staticmethod
    def pretty_print(lst):
        print("Results..")
        for i in lst:
            print(i)
        print("")

    # function asks user for csv input
    def get_csv():
        csv = input("If you want to add more songs from a csv, " +
        "please provide its name. Otherwise, type 'no'.\n")
        if csv.lower() == 'no':
            return 'no'
        else:
            return csv

    # function checks to make sure the song exists
    def song_check(name):
        query = "SELECT DISTINCT Name FROM songs"
        dictionary = {}
        songNames = db_ops.name_placeholder_query(query, dictionary)
        songFound = False
        for i in songNames:
            if str(i) == name:
                songFound = True
        if songFound == False:
            print ("Song not found.")
        return songFound
