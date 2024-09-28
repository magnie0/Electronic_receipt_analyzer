
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
per_item_pattern = f"^{name_pattern}\s{code_pattern}\s{item_count_pattern}\s{item_price_pattern}\s{total_pattern}"

#perkg
per_kg_pattern = f"^{name_pattern}\s{code_pattern}\s{kg_count_pattern}\s{kg_price_pattern}\s{total_pattern}"

#discount line
discount_pattern = f"^Rabat\s{name_pattern}\s{code_pattern}\s-{total_pattern}"

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
            total_sum += total
            products.append(Product(date, n,q,p,t))
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
            total_sum += total
            products.append(Product(date,n,k,p,t))
            continue
        match = re.search(discount_pattern, line)
        if (match):
            n, c, p = match.groups()
            print("znizka: "+n+"  "+p)
            total = str_to_float(p)
            total_sum -= total
            #TODO Add handling reducted price
            continue
        match = re.search(sum_pattern, line)
        if (match):
            t = match.group(1)
            sum_from_receipt = str_to_float(t)
            print("laczna suma: "+t)


        other_lines.append(line)
    print("suma_dodana: "+str(round(total_sum,2)))
    print("suma_z_paragonu: "+str(round(sum_from_receipt,2)))
    print("===============Other found lines")
    print("\n".join(other_lines))

    return products
