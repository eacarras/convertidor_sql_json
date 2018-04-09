words_of_my_sql = ["SET", "DROP", "CREATE", "PRIMARY", "INSERT"]


def create_principal_dic(file_txt):
    json = {}
    file = open(file_txt, "r")
    for line in file:
        line = line.strip()
        if line.count(" ") > 0:
            line = line.split(" ")
            if("TABLE" in line) and ("DROP" in line):
                table = line[-1].strip("[").strip(";")
                table = table.strip("]")
                json[table] = []
    file.close()
    return json;


def makes_columns_tables(file_txt, json):
    file = open(file_txt, "r")
    count_copy = 0
    line_first = file.readlines()
    line_second = line_first
    counter_init = 0
    for line_first in line_first:
        count_copy = counter_init
        line_first = line_first.strip()
        if line_first.count(" ") > 0:
            line_first = line_first.split(" ")
            if ("TABLE" in line_first) and ("CREATE" in line_first):
                table = line_first[-1].strip("[").strip("]")
                for lines in line_second:
                    line = line_second[count_copy + 2]
                    line = line.strip()
                    line = line.split(" ")
                    if "CONSTRAINT" in line_second[count_copy + 4]:
                        break
                    else:
                        column = line[0].strip("[").strip("]")
                        json[table].append(column)
                    count_copy += 1
        counter_init += 1
    file.close()
    return json;


def validate_of_txt(file_txt):
    global words_of_my_sql
    file = open(file_txt, "r")
    count = 0
    for line in file:
        line = line.strip()
        if line.count(" ") > 0:
            line = line.split(" ")
            for word in words_of_my_sql:
                if word in line:
                    count += 1
    if count >= 5:
        return True
    else:
        return False;


def create_json(json_dic):
    file = open("model.json", "w")
    file.write("{\n")
    for table, columns in json_dic.items():
        file.write("  '{}': [\n".format(table))
        file.write("   {\n")
        for column in columns:
            if column == columns[-1]:
                file.write("     '{}': ''\n".format(column))
            else:
                file.write("     '{}': '',\n".format(column))
        file.write("   },\n")
    file.write("}\n")


def make_window():
    import tkinter as tk
    window = tk.Tk()
    window.title("SqlDBM to Json file")
    window.geometry('380x300')
    window.configure(background='navy')
    label_first = tk.Label(window,text="Welcome to my Json converter", bg="navy", fg="white")
    label_first.pack(fill=tk.X)
    window.mainloop()


def create_Table_shell(name_database, endpoint, region):
    import boto3

    dynamodb = boto3.resource(name_database, region_name=region, endpoint_url=endpoint)
    name_table = input("Insert the name of the table")
    flat = "S"
    while flat != "N":
        print("This is the name of the table that you insert " + name_table + "if it's okey please enter N")
        flat = input()
    attribute_name = input("Insert the attributeName of you Primary Key: ")
    key_type = input("Insert the key type of your Primary key: ")
    attribute_name_definitions = input("Insert the attribute name of the attribute definitions: ")
    attribute_type = input("Insert the attribute type of the attribute definitions: ")
    read_capacity = input("Insert the read capacity: ")
    write_capacity = input("Insert the write capacity: ")
    table = dynamodb.create_table(
        TableName=name_table,
        KeySchema=[
            {
                'AttributeName': attribute_name,
                'KeyType': key_type
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName' : attribute_name_definitions,
                'AttributeType' : attribute_type
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits' : read_capacity,
            'WriteCapacityUnits' : write_capacity
        }
    )

    print("Table status: ", table.table_status)


def validation_of_namedatabase_region_endpoint(String):
    split = String.split(",")
    len_split = len(split)
    if (len_split == 3):
        endpoint = split[-1]
        endpoint_split = endpoint.split(":")
        if endpoint_split[0] == "http" or endpoint_split[0] == "https":
            return False
    else:
        return True


def split_of_Name(String):
    String = String.split(",")
    database = String[0] ; region = String[1] ; endpoint = String[-1]
    return database,region,endpoint
