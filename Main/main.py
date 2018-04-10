from __future__ import print_function
from Functions.Functions import *


print("Welcome, please insert 'G' to generate a json file with the columns and fillings in blank "
      "or any key to go direct to the create of tables")
key = input().upper()
count = 0

# make the json file if the user input 'G'
if key == "G":
    file_txt = input("Insert the name of the file to read (PD: Onlyfile with extension txt)\n")
    while file_txt.split(".")[-1] != "txt":
        file_txt = input("File can't read, try again (PD: Onlyfile with extension txt)\n")
    count = 1
    if validate_of_txt(file_txt):
        json = create_principal_dic(file_txt)
        json = makes_columns_tables(file_txt, json)
        create_json(json)
    else:
        print("You insert a not sql file")

# the program ask the name of txt file to make the tables only if the user not generate the json file
if count == 0:
    file_txt = input("Insert the name of the file to read (PD: Only file with extension txt)\n")
    while file_txt.split(".")[-1] != "txt":
        file_txt = input("File can't read, try again (PD: Only file with extension txt)\n")

# the program ask the region and endpoint_url and validated it
print("Please insert the region and the endpoint url, all separate with coma and merge")
String = input()
while validation_of_region_endpoint(String):
    print("Incorrect input, please insert the characters in the correct form")
    String = input()
region, endpoint_url = split_of_name(String)

# created tables
print("PD: When you finish only write at the final 'F', Good Luck")
key = "A"
while key != "F":
    create_table_shell(region, endpoint_url)
    print("Insert 'F' or any key to continue creating tables")
    key = input()
