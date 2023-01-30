from helper import helper

# handles all the csv parsing and database operations
helper = helper()

# pulls data from the csv file and inserts into staging
def staging_setup():
    data = helper.data_cleaner()
    helper.insert_table(data, "staging")

# selects for info from staging and inserts into agency
def agency_setup():
    query = "SELECT DISTINCT Agency FROM staging"
    name_dict = helper.single_attribute_dictionary(query)
    query = "SELECT DISTINCT agencyOrigin FROM staging"
    origin_dict = helper.single_attribute_dictionary(query)

    agency_info = []
    if len(name_dict) == len(origin_dict):
        for i in range(len(name_dict)):
            agency_info += [(name_dict[i], origin_dict[i])]
    else:
        print("Error: Uneven number of agency attributes")
    helper.insert_table(agency_info, "agency (Name, Origin)")


# selects for info from staging and inserts into astronaut
# references agency table for agencyID
def astronaut_setup():
    query = "SELECT Astronaut FROM staging"
    name_dict = helper.single_attribute_dictionary(query)
    query = "SELECT Age FROM staging"
    age_dict = helper.single_attribute_dictionary(query)

    query = "SELECT Agency FROM staging"
    agency_dict = helper.single_attribute_dictionary(query)
    query = "SELECT name FROM agency"
    agency_ref = helper.single_attribute_dictionary(query)

    for i in range(len(agency_ref)):
        for j in range(len(agency_dict)):
            if agency_dict[j] == agency_ref[i]:
                agency_dict[j] = i+1

    astro_info = []
    if len(name_dict) == len(age_dict) and len(name_dict) == len(agency_dict):
        for i in range(len(name_dict)):
            astro_info += [(name_dict[i], age_dict[i], agency_dict[i])]
    else:
        print("Error: Uneven number of astronaut attributes")
    helper.insert_table(astro_info, "astronaut (Name, Age, Agency)")


# selects for info from staging and inserts into expedition
def expedition_setup():
    query = "SELECT DISTINCT Expedition FROM staging"
    exp_dict = helper.single_attribute_dictionary(query)
    query = "SELECT Duration FROM staging GROUP BY Expedition, Duration"
    dur_dict = helper.single_attribute_dictionary(query)

    exp_info = []
    if len(exp_dict) == len(dur_dict):
        for i in range(len(exp_dict)):
            exp_info += [(exp_dict[i], dur_dict[i])]
    else:
        print("Error: Uneven number of agency attributes")
    helper.insert_table(exp_info, "expedition")


# selects for info from staging and inserts into agency
# references astronaut for astronautID
def astroExp_setup():
    query = "SELECT Expedition FROM staging"
    exp_dict = helper.single_attribute_dictionary(query)

    query = "SELECT Astronaut FROM staging"
    astro_dict = helper.single_attribute_dictionary(query)
    query = "SELECT name FROM astronaut"
    astro_ref = helper.single_attribute_dictionary(query)

    for i in range(len(astro_ref)):
        for j in range(len(astro_dict)):
            if astro_dict[j] == astro_ref[i]:
                astro_dict[j] = i+1

    astroExp_info = []
    if len(exp_dict) == len(astro_dict):
        for i in range(len(exp_dict)):
            astroExp_info += [(exp_dict[i], astro_dict[i])]
    else:
        print("Error: Uneven number of astronauts and expeditions")
    helper.insert_table(astroExp_info, "astro_expedition (Expedition, Astronaut)")

print("Starting.")
staging_setup()
print("Staging complete.")
agency_setup()
print("Agency complete.")
astronaut_setup()
print("Astronaut complete.")
expedition_setup()
print("Expedition complete.")
astroExp_setup()
print("astro_expedition complete.")
helper.destructor()
print("Goodbye.")
