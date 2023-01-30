# module defines an application to curate a playlist
# with a sqlite3 db as a backend for data storage

from helper import helper
from db_operations import db_operations

data = helper.data_cleaner("songs.csv")

# modify to your chinook db connection
db_ops = db_operations("../Databases/chinook/chinook.db")

# function checks if the table is empty or not
def is_empty():
    query = '''
    SELECT COUNT(*)
    FROM songs;
    '''

    result = db_ops.single_record(query)
    return result == 0

# function inserts data into table if it is empty
def pre_process():
    # edited to allow addition of extra records on start
    csv = helper.get_csv()
    if csv != 'no':
        data = helper.data_cleaner(csv)
    else:
        data = helper.data_cleaner("songs.csv")

    if csv != 'no'or is_empty():
        attribute_count = len(data[0])
        placeholders = ("?,"*attribute_count)[:-1]
        query = "INSERT INTO songs VALUES("+placeholders+")"
        db_ops.bulk_insert(query,data)


def start_screen():
    print("Welcome to your playlist!")


# show user options
def options():
    print("Select from the following menu options:\n1 Find songs by artist\n" \
    "2 Find songs by genre\n3 Find songs by feature\n" \
    "4 Update a song\n5 Delete\n6 Exit")
    return helper.get_choice([1,2,3,4,5,6])

# option 1, search table to show songs by artist
def search_by_artist():
    query = '''
    SELECT DISTINCT Artist
    FROM songs;
    '''
    print("Artists in playlist:")
    artists = db_ops.single_attribute(query)

    # show artists in table, also create dictionary for choices
    choices = {}
    for i in range(len(artists)):
        print(i,artists[i])
        choices[i] = artists[i]
    index = helper.get_choice(choices.keys())

    # user can ask to see 1, 5, or all songs
    print("How many songs do you want returned for",choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    # prepare query and show results
    query = "SELECT DISTINCT name FROM songs WHERE Artist=:artist ORDER BY RANDOM()"
    dictionary = {"artist":choices[index]}
    if num != 0:
        query +=" LIMIT:lim"
        dictionary["lim"] = num
    helper.pretty_print(db_ops.name_placeholder_query(query,dictionary))


# option 2, search table for songs by genre
def search_by_genre():
    query = '''
    SELECT DISTINCT Genre
    FROM songs;
    '''
    print("Genres in playlist:")
    genres = db_ops.single_attribute(query)

    # show genres in table, also create dictionary for choices
    choices = {}
    for i in range(len(genres)):
        print(i,genres[i])
        choices[i] = genres[i]
    index = helper.get_choice(choices.keys())

    # how many records
    print("How many songs do you want returned for",choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    # run query and show results
    query = "SELECT DISTINCT name FROM songs WHERE Genre =:genre ORDER BY RANDOM()"
    dictionary = {"genre":choices[index]}
    if num != 0:
        query +=" LIMIT:lim"
        dictionary["lim"] = num
    helper.pretty_print(db_ops.name_placeholder_query(query,dictionary))

# option 3, search songs by asc,desc order of audio feature
def search_by_feature():
    features = ['Danceability','Liveness','Loudness'] # features to show the user
    choices = {}
    for i in range(len(features)):
        print(i,features[i])
        choices[i] = features[i]
    index = helper.get_choice(choices.keys())

    # how many records
    print("How many songs do you want returned for "+choices[index]+"?")
    print("Enter 1, 5, or 0 for all songs")
    num = helper.get_choice([1,5,0])

    # order  by ascending or descending
    print("Do you want results sorted by the feature in ascending or descending order?")
    order = input("ASC or DESC: ")

    # prepare query and show results
    query = "SELECT DISTINCT Name FROM songs ORDER BY "+choices[index]+" "+order
    dictionary = {}
    if num!=0:
        query+=" LIMIT :lim"
        dictionary['lim'] = num
    helper.pretty_print(db_ops.name_placeholder_query(query,dictionary))

# option 4, asks for song name and allows user to update 1 attribute of that song
def update_song():
    attributes = ["Name", "Artist", "Album","releaseDate", "Explicit"]
    results = ["", "", "", "", ""]

    print("What song do you wish to update? This is case sensitive.")
    name = input("Song name: ")
    if helper.song_check(name) == False:
        return None

    helper.pretty_print(results)
    print("Enter the number associated with the attribute you wish to update.")
    num = helper.get_choice([1,2,3,4,5])-1

    while True:
        update = input("Enter the updated "+attributes[num]+" value: ")
        if num <= 2:
            break
        if num == 3:
            dateFormat = True
            for i in range(0, len(update)):
                try:
                    int(update)
                except:
                    if i == 4 or i == 7:
                        pass
                    else:
                        print("Please format dates as YYYY-MM-DD.")
                        dateFormat = False
                        break
            if dateFormat == True:
                break
        elif num == 4:
            if update.lower() == "true":
                update = True
                break
            elif update.lower() == "false":
                update = False
                break
            else:
                print("Please enter 'true' or 'false' for the Explicit attribute")

    db_ops.update_attribute(name,attributes[num],update)

def delete_song():
    print("What song do you wish to delete? This is case sensitive.")
    name = input("Song name: ")
    if helper.song_check(name) == False:
        return None
    db_ops.delete_record(name)


# main program
pre_process()
start_screen()
while True:
    user_choice = options()
    if user_choice == 1:
        search_by_artist()
    elif user_choice == 2:
        search_by_genre()
    elif user_choice == 3:
        search_by_feature()
    elif user_choice == 4:
        update_song()
    elif user_choice == 5:
        delete_song()
    elif user_choice == 6:
        print("Goodbye!")
        break



db_ops.destructor()
