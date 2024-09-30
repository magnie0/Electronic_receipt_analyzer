import pandas as pd
import json
def create_empty(excel_file_path, name_sheet, name_database):
    df = pd.read_excel(excel_file_path, sheet_name=name_sheet, dtype=str)
    dictionary_categories = dict()
    for index, row in df.iterrows():
        print(f"Row {index} data: {row.to_dict()}")
        line = row.to_dict()
        cat0 = line['Kat0']
        cat1 = line['Kat1']
        cat2 = line['Kat2']
        code = line['Code']
        if cat0 not in dictionary_categories:
            dictionary_categories[cat0] = dict()
        
        if cat1 not in dictionary_categories[cat0]:
            dictionary_categories[cat0][cat1] = dict()

        if cat2 not in dictionary_categories[cat0][cat1]:
            dictionary_categories[cat0][cat1][cat2] = []
    

    json_object = json.dumps(dictionary_categories, ensure_ascii=False, indent=4).encode('utf8')
    with open("sample.json", "w") as outfile:
        outfile.write(json_object.decode())

create_empty('./data/Rozpisanie zakupów .xlsx','Pogląd Mappingu','')