from __future__ import print_function
from Functions.Functions import *


# options of the programs
print("Welcome, please insert a option\n"
      "1.- Generate json file with empty fields\n"
      "2.- Generate automatically the tables using a sql server script\n"
      "3.- Created new tables\n"
      "4.- Exit")
option = input()

# validation of the user input
while option.isalpha() or int(option) <1 or int(option) > 4:
    print("The option that you input it's incorrect")
    option = input()

# program
option = int(option)
while option != 4:

    # make the json file if the user input 1
    if option == 1:
        file_txt = input("Insert the name of the file to read (PD: Only files with extension txt)\n")
        while file_txt.split(".")[-1] != "txt":
            file_txt = input("File can't read, try again (PD: Only files with extension txt)\n")
        if validate_of_txt(file_txt):
            json = create_principal_dic(file_txt)
            json = makes_columns_tables(file_txt, json)
            create_json(json)
        else:
            print("You insert a not sql file")

    # the program ask the name of txt file to make the tables automatically
    elif option == 2:
        file_txt = input("Insert the name of the file to read (PD: Only file with extension txt)\n")
        while file_txt.split(".")[-1] != "txt":
            file_txt = input("File can't read, try again (PD: Only file with extension txt)\n")
        # created tables
        print("Good Luck !")
        create_table_shell_automatically(file_txt)

    # the program ask the name of the table, the region, the url endpoint to generate the tables
    elif option == 3:
        file_txt = input("Insert the name of the file to read (PD: Only file with extension txt)\n")
        while file_txt.split(".")[-1] != "txt":
            file_txt = input("File can't read, try again (PD: Only file with extension txt)\n")
        flat = "A"
        while flat != "E":

            # validation of the name of the table
            flat_copy = "A"
            while flat_copy != "E":
                print("Input the name of the table")
                name_table = input()
                print("The name of your table is : {} it's this information wasn't correct press E ")
                if validation_name_table(name_table):
                    flat_copy = input()
                else:
                    print("You have input a incorrect character")
                    flat_copy = "A"

            # validation of the region and the endpoint url
            print("Input the region and endpoint url separate with coma and all merge")
            string = input()
            while validation_of_region_endpoint(string):
                string = input("Please insert a correct data: ")
            region, endpoint_url = split_of_name(string)
            print("Input the name of the primary key")
            primary_key = input()
            # creation of the table
            create_table(region, endpoint_url, name_table, primary_key)
            print("Write E to exit or ")

    # another input of option
    print("Input another option or 4 to exit")
    option = input()
    while option.isalpha() or int(option) < 1 or int(option) > 4:
        print("The option that you input it's incorrect")
        option = input()
    option = int(option)

print("Thanks for user my program ");