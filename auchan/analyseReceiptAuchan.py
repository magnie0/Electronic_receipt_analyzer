
#peritem
#per_item_pattern = "^(?P<name>.+)\s(?P<code>\d{6}[A-Z]?)\s(?P<quantity>\d+)\s-?x(?P<perItem>\d+,\d\d)\s(?P<total>\d+,\d\d)"

#weight
#per_kg_pattern = "^(?P<name>.+)\s(?P<code>\d{6}[A-Z]?)\s(?P<weight>\d,\d\d\d)\s-?x(?P<perKg>\d+,\d\d)\s(?P<total>\d+,\d\d)"
import re
#regexes for product lines
name_pattern = r"(?P<name>.+)"
code_pattern = r"(?P<code>\d{5,6}[A-Z]?)"
item_count_pattern = r"(?P<quantity>\d+)"
item_price_pattern = r"-?x(?P<perItem>\d+,\d\d)"
kg_count_pattern = r"(?P<weight>\d,\d\d\d)"
kg_price_pattern = r"x(?P<perKg>\d+,\d\d)"
total_pattern = r"(?P<total>\d+,\d\d)"

#peritem
per_item_pattern = f"^{name_pattern}\s{code_pattern}\s{item_count_pattern}\s{item_price_pattern}\s{total_pattern}"

#perkg
per_kg_pattern = f"^{name_pattern}\s{code_pattern}\s{kg_count_pattern}\s{kg_price_pattern}\s{total_pattern}"

def str_to_float(s):
    return float(s.replace(',','.'))
def Analyse_Receipt_Auchan(str):
    data = str.splitlines()
    other_lines = [] #for checking if sth isn't caught
    for line in data:
        if (line == ""):
            continue
        match = re.search(per_item_pattern, line)
        if (match):
            n, c, q, p, t = match.groups()
            #print(f"PerItem {n} {c} {q} {p} {t}")
            item = str_to_float(q)
            peritem = str_to_float(p)
            total = str_to_float(t)
            if (round(item*peritem,2) != round(total, 2)):
                print(f"total isn't equal {n} in {q} x {p} != {t}")
            continue
        match = re.search(per_kg_pattern, line)
        if (match):
            n, c, k, p, t = match.groups()
            #print(f"PerKg {n} {c} {k} {p} {t}")
            kg = str_to_float(k)
            perkg = str_to_float(p)
            total = str_to_float(t)
            if (round(kg*perkg,2) != round(total, 2)):
                print(f"total isn't equal {n} in {k} x {p} != {t}")
            continue
        other_lines.append(line)
    print("===============Other found lines")
    print("\n".join(other_lines))
