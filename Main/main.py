from Functions.Functions import *


file_txt = "example.txt"
if validate_of_txt(file_txt):
    json = create_principal_dic(file_txt)
    json = makes_columns_tables(file_txt, json)
    create_json(json)