words_of_my_sql = ["SET", "DROP", "CREATE", "PRIMARY", "INSERT"]
words_avalibles_tables = ["A", "a", "B", "b", "C", "c", "D", "d", "E", "e", "F", "f", "G", "g", "H", "h","I", "i"
                         "J", "j", "K", "k", "L", "l", "M", "m", "N", "n", "O", "o", "P", "p", "Q", "q", "R", "r"
                         "S", "s", "T", "t", "U", "u", "V", "v", "w", "W", "X", "x", "Y", "y", "Z", "z", "0", "1"
                         "2", "3", "4", "5", "6", "7", "8", "9", "-", "_", "."]


def create_principal_dic(file_txt):
    json = {}
    file = open(file_txt, "r")
    for line in file:
        line = line.strip()
        if line.count(" ") > 0:
            line = line.split(" ")
            if("TABLE" in line) and ("CREATE" in line):
                table = line[-1].strip("[")
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
        file.write("   ],\n")
    file.write("}\n")


def make_window():
    import tkinter as tk
    window = tk.Tk()
    window.title("SqlDBM to Json file")
    window.geometry('380x300')
    window.configure(background='navy')
    label_first = tk.Label(window, text="Welcome to my Json converter", bg="navy", fg="white")
    label_first.pack(fill=tk.X)
    window.mainloop()


def create_table_shell_automatically(file_txt, endpoint_url):
    import boto3
    import time

    # extract name of tables in the file
    name_tables = []
    file = open(file_txt, "r")
    for line in file:
        line = line.strip()
        if line.count(" ") > 0:
            line = line.split(" ")
            if ("TABLE" in line) and ("CREATE" in line):
                table = line[-1].strip("[")
                table = table.strip("]")
                name_tables.append(table)

    # extract the primary key of the tables
    name_primary_keys = []
    file = open(file_txt, "r")
    for line in file:
        line = line.strip()
        if line.count(" ") > 0:
            line = line.split(" ")
            if ("CONSTRAINT" in line) and ("PRIMARY" in line) and (len(line) == 7):
                table = line[-2].strip("(")
                table = table.strip("]")
                table = table.strip("[")
                name_primary_keys.append(table)
            elif ("CONSTRAINT" in line) and ("PRIMARY" in line) and (len(line) == 8):
                name_primary_keys.append("fact")

    # connect with DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url=endpoint_url)

    # create the tables with his primary keys
    count = 0
    for name_table in name_tables:
        name_table = "bpm_"+name_table
        time.sleep(30)
        table = dynamodb.create_table(
            TableName=name_table,
            KeySchema=[
                {
                    'AttributeName': name_primary_keys[count],
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': name_primary_keys[count],
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        count += 1
        print("Table status: ", table.table_status)

    # confirmation of successfully
    print("The database was created successfully")


def create_table(region, endpoint_url, name_table, primary_key):
    import boto3
    import time

    # connect with DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name=region, endpoint_url=endpoint_url)

    # create the tables with his primary keys
    time.sleep(30)
    table = dynamodb.create_table(
        TableName=name_table,
        KeySchema=[
            {
                'AttributeName': primary_key,
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': primary_key,
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    # confirmation of successfully
    print("Table status: ", table.table_status);


def validation_name_table(name):
    global words_avalibles_tables
    counter = 0
    for letter in name:
        if letter not in words_avalibles_tables:
            counter += 1
    if counter == 0:
        return True
    else:
        return False;


def get_process(process_name):
    import psutil

    for process in psutil.process_iter():
        if process.name() == process_name:
            return process;


def get_pid(process_name):
    import psutil

    for process in psutil.process_iter():
        if process.name() == process_name:
            return process.pid


def get_endpoint(string):
    file = open(".env", "r")
    for line in file:
        line = line.strip()
        line = line.split(" ")
        if string == line[0]:
            endpoint = line[-1]
    file.close()
    return endpoint


def drop_table(region, endpoint_url, name_table):
    import boto3

    dynamodb = boto3.resource('dynamodb', region_name=region, endpoint_url=endpoint_url)
    table = dynamodb.Table(name_table)
    table.delete();


def drop_all_the_tables():
    import boto3

    # validation of the process input
    process_name = input("Please input the service that you want to use: ")
    p_1 = get_process(process_name)
    if p_1 is not None:
        status = True
    else:
        status = False

    # search the status of the process
    if status:
        id = get_pid(process_name)
        p = Process(id)
        endpoint_url = get_endpoint("localhost")
    else:
        endpoint_url = get_endpoint("cloud")
    # the program ask the name of txt file to make the tables automatically
    file_txt = input("Insert the name of the file to read (PD: Only file with extension txt)\n")
    while file_txt.split(".")[-1] != "txt":
        file_txt = input("File can't read, try again (PD: Only file with extension txt)\n")
    # drop the tables
    # extract name of tables in the file
    name_tables = []
    file = open(file_txt, "r")
    for line in file:
        line = line.strip()
        if line.count(" ") > 0:
            line = line.split(" ")
            if ("TABLE" in line) and ("CREATE" in line):
                table = line[-1].strip("[")
                table = table.strip("]")
                name_tables.append(table)
    print("Please insert the region ")
    region = input()
    dynamodb = boto3.resource('dynamodb', region_name=region, endpoint_url=endpoint_url)
    for tablee in name_tables:
        table = dynamodb.Table(tablee)
        table.delete();


def ingresar_datos(region, endpoint_url, name_table):
    import boto3
    import json
    import decimal

    dynamodb = boto3.resource('dynamodb', region_name=region, endpoint_url=endpoint_url)
    table = dynamodb.Table(name_table)

    # with open("moviedata.json") as json_file: