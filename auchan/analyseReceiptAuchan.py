
#peritem
#^(?P<name>.+)\s(?P<code>\d{6}[A-Z]?)\s(?P<quantity>\d+)\s-?x(?P<perItem>\d+,\d\d)\s(?P<total>\d+,\d\d)

#weight
#^(?P<name>.+)\s(?P<code>\d{6}[A-Z]?)\s(?P<weight>\d,\d\d\d)\s-?x(?P<perKg>\d+,\d\d)\s(?P<total>\d+,\d\d)


#example usage
# m = re.search(regex, line)
# if m is not None:
#     m.group("name") - take value