# module defines operations to use with sqlite3 database
import sqlite3


class db_operations():
    def __init__(self,conn_path): # constructor with connection path to db
        self.connection = sqlite3.connect(conn_path)
        self.cursor = self.connection.cursor()
        print("connection made..")

    # function for bulk inserting records
    def bulk_insert(self,query,records):
        # edited to pass over records with an ID already in the system
        while len(records) > 0:
            try:
                self.cursor.executemany(query, records)
                del records[0]
            except:
                del records[0]
                pass
        self.connection.commit()
        print("query executed..")

    # function to return a single value from table
    def single_record(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    # function to return a single attribute values from table
    def single_attribute(self,query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        for i in results:
            if i == None:
                results.remove(None)
        #results.remove(None)
        return results

    # function to return a single attribute values from table using a dictionary
    def single_attribute_dictionary(self,query,dictionary):
        self.cursor.execute(query,dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results

    # SELECT with named placeholders
    def name_placeholder_query(self,query,dictionary):
        self.cursor.execute(query,dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results

    # function to update a single attribute in a single record
    def update_attribute(self,songName,attributeName,newAttribute):
        query = "UPDATE songs SET "+attributeName+" =:newAttribute WHERE Name =:songName;"
        dictionary = {"newAttribute":newAttribute,"songName":songName}
        self.cursor.execute(query,dictionary)
        self.connection.commit()
        print("Attribute updated..")

    # function to delete a single record with the given name
    def delete_record(self,name):
        query = "DELETE FROM songs WHERE Name =:name"
        self.cursor.execute(query,{"name":name})
        self.connection.commit()
        print("Record deleted..")

    # close connection
    def destructor(self):
        self.connection.close()
