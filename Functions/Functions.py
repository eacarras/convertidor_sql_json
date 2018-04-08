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
    if count > 0:
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


