
#peritem
#per_item_pattern = "^(?P<name>.+)\s(?P<code>\d{6}[A-Z]?)\s(?P<quantity>\d+)\s-?x(?P<perItem>\d+,\d\d)\s(?P<total>\d+,\d\d)"

#weight
#per_kg_pattern = "^(?P<name>.+)\s(?P<code>\d{6}[A-Z]?)\s(?P<weight>\d,\d\d\d)\s-?x(?P<perKg>\d+,\d\d)\s(?P<total>\d+,\d\d)"
import re
from utils.product import Product
#regexes for product lines
name_pattern = r"(?P<name>.+)"
code_pattern = r"(?P<code>\d{3,6}.?)" #last char sometimes is as ] we don't use the code product so it isn't important for us
item_count_pattern = r"(?P<quantity>\d+)"
item_price_pattern = r"-?x(?P<perItem>\d+,\d\d)"
kg_count_pattern = r"(?P<weight>\d,\d{1,3})"
kg_price_pattern = r"x(?P<perKg>\d+,\d\d)"
total_pattern = r"(?P<total>\d+,\d\d)"

#peritem
per_item_pattern = f"^{name_pattern}\s{item_count_pattern}\s{item_price_pattern}\s{total_pattern}"

#perkg
per_kg_pattern = f"^{name_pattern}\s{kg_count_pattern}\s{kg_price_pattern}\s{total_pattern}"

#discount line
discount_pattern = f"^Rabat\s{name_pattern}\s-{total_pattern}"

#date line
date_pattern = f"(?P<year>\d\d\d\d)-(?P<month>\d\d)-(?P<day>\d\d)"

#line that shouldn;t be parsing as product starts with
last_line_pattern = f"SPRZEDAZ OPODATK"

#name_and_code
name_and_code_pattern = f"{name_pattern}\s{code_pattern}"

#sum
sum_pattern = f"^SUMA\sPLN\s{total_pattern}"

def str_to_float(s):
    return float(s.replace(',','.'))
def Receipt_To_Product(input_str, date):
    data = input_str.splitlines()
    other_lines = [] #for checking if sth isn't caught
    total_sum = 0
    products = []
    sum_from_receipt = 0

    check_line = False
    for line in data:
        if (line == ""):
            continue

        match = re.search(date_pattern, line)
        if (match):
            y, m, d = match.groups()
            check_line = True
            #TODO check date
            continue

        match = re.search(sum_pattern, line)
        if (match):
            t = match.group(1)
            sum_from_receipt = str_to_float(t)
        
        match = re.search(last_line_pattern, line)
        if (match):
            check_line = False
        
        if not check_line:
            continue

        #products
        match = re.search(per_item_pattern, line)
        if (match):
            name_and_code, q, p, t = match.groups()
            n = ""
            c = ""
            submatch = re.search(name_and_code_pattern, name_and_code)
            if (submatch):
                n, c = submatch.groups()
            else:
                n = name_and_code
            #print(f"PerItem {n} {c} {q} {p} {t}")
            item = str_to_float(q)
            peritem = str_to_float(p)
            total = str_to_float(t)
            if (round(item*peritem,2) != round(total, 2)):
                print(f"total isn't equal {n} in {q} x {p} != {t}")
            total_sum += total
            products.append(Product(date, n,c,item,peritem,total))
            continue
        match = re.search(per_kg_pattern, line)
        if (match):
            name_and_code, k, p, t = match.groups()
            n = ""
            c = ""
            submatch = re.search(name_and_code_pattern, name_and_code)
            if (submatch):
                n, c = submatch.groups()
            else:
                n = name_and_code
            #print(f"PerKg {n} {c} {k} {p} {t}")
            kg = str_to_float(k)
            perkg = str_to_float(p)
            total = str_to_float(t)
            if (round(kg*perkg,2) != round(total, 2)):
                print(f"total isn't equal {n} in {k} x {p} != {t}")
            total_sum += total
            products.append(Product(date,n,c,kg,perkg,total))
            continue
        match = re.search(discount_pattern, line)

        #discount
        if (match):
            name_and_code, p = match.groups()
            n = ""
            c = ""
            submatch = re.search(name_and_code_pattern, name_and_code)
            if (submatch):
                n, c = submatch.groups()
            else:
                n = name_and_code
            print("znizka: "+n+"  "+p)
            total = str_to_float(p)
            total_sum -= total
            products.append(Product(date,n,c,0,0,-total))
            #TODO Add handling reducted price
            continue

        other_lines.append(line)
    
    print("------ Other found lines ------")
    print("\n".join(other_lines))
    print("------ End of other found lines ------")

    print("suma_dodana: "+str(round(total_sum,2)))
    print("suma_z_paragonu: "+str(round(sum_from_receipt,2)))
    return products
