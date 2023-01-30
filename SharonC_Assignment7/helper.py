import mysql.connector


class helper():
    # constructor with connection to db
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': 'password1',
            'host': '35.226.231.247',
            'database': 'cpsc408'
        }
        self.connector = mysql.connector.connect(**self.config)
        self.cursor = self.connector.cursor()
        print("Connection made")

    # parses data and converts it to the appropriate value
    @staticmethod
    def convert(value):
        types = [int,float,str]
        if value == '':
            return None
        for t in types:
            try:
                return t(value)
            except:
                pass

    # parses the csv and returns the info as a list of tuples
    @staticmethod
    def data_cleaner():
        with open("expeditionData.csv","r",encoding="utf-8") as f:
            data = f.readlines()

        data = [i.strip().split(",") for i in data]
        data_cleaned = []
        for row in data[:]:
            row = [helper.convert(i) for i in row]
            data_cleaned.append(tuple(row))
        del data_cleaned[0]
        return data_cleaned

    # inserts multiple records at once
    def bulk_insert(self, query, records):
        self.cursor.executemany(query, records)
        self.connector.commit()

    # inserts records into desired table
    def insert_table(self, data, table):
        attribute_count = len(data[0])
        placeholders = ("%s,"*attribute_count)[:-1]
        query = "INSERT INTO "+table+" VALUES("+placeholders+")"
        helper.bulk_insert(self, query, data)

    # returns the results of a SELECT statement w/ a single attribute as a dictionary
    def single_attribute_dictionary(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results

    # close connection
    def destructor(self):
        self.cursor.close()
        self.connector.close()
