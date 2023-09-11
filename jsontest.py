import json
# Open the JSON file


terms = ["F17", "E17", "F18", "E18", "F19", "E19", "F20", "E20", "F21", "E21", "F22", "E22", "F23"]

# Grade check
data_len = 0
e404 = 0
grade = 0
fewgrade = 0
something_else = 0
unknown_key = ""

for term in terms:
    with open(f'html_persistence/{term}_grades.json', 'r', encoding='utf-8') as json_file:
        # Load the JSON data as a dictionary
        data = json.load(json_file)

    data_len += len(data)
    for key, value in data.items():
        if "404 - File or directory not found." in value:
            e404 += 1
        elif "Eksamensgennemsnit" in value:
            grade += 1
        elif "Fordelingen vises ikke da tre eller færre har været til denne eksamen." in value:
            fewgrade += 1
        else:
            something_else += 1
            unknown_key = key

duplicate = e404 + grade + fewgrade + something_else
print(f"e404 = {e404}")
print(f"grade = {grade}")
print(f"fewgrade = {fewgrade}")
print(f"else = {something_else}")
print(f"{duplicate}={data_len}")
if unknown_key != "":
    print(unknown_key)
print()


# Evaluation check
data_len = 0
e404 = 0
evaluation = 0
something_else = 0
unknown_key = ""

for term in terms:
    with open(f'html_persistence/{term}_evaluations.json', 'r', encoding='utf-8') as json_file:
        # Load the JSON data as a dictionary
        data = json.load(json_file)

    data_len += len(data)
    for key, value in data.items():
        if len(value) == 0:
            e404 += 1
        elif ("Statistik" in value) and ("kunne besvare dette evalueringsskema" in value):
            evaluation += 1
        else:
            something_else += 1
            unknown_key = key

duplicate = e404 + evaluation  + something_else
print(f"e404 = {e404}")
print(f"evaluation = {evaluation}")
print(f"else = {something_else}")
print(f"{duplicate}={data_len}")
if unknown_key != "":
    print(unknown_key)
print()


# Information check
data_len = 0
e404 = 0
info = 0
something_else = 0
unknown_key = ""

for term in terms:
    with open(f'html_persistence/{term}_information.json', 'r', encoding='utf-8') as json_file:
        # Load the JSON data as a dictionary
        data = json.load(json_file)

    data_len += len(data)
    for key, value in data.items():
        if "Unknown coursecode" in value:
            e404 += 1
        elif "Course information" in value:
            info += 1
        else:
            something_else += 1
            unknown_key = key

duplicate = e404 + info  + something_else
print(f"e404 = {e404}")
print(f"info = {info}")
print(f"else = {something_else}")
print(f"{duplicate}={data_len}")
if unknown_key != "":
    print(unknown_key)
print()