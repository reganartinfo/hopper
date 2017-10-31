import json, re

range_dates = []
no_dates = []
other_dates = []
pythex_date = re.compile("\d{4}")

with open("hopper_dump.json","r") as f:
	encoder = json.load(f)
	for an_object in encoder:
		object_date = an_object["display_date"]
		if object_date == "n.d.":
			no_dates.append(an_object)
		else:
			regex_date = pythex_date.findall(object_date)
			earliest_date = int(regex_date[0])
			if (earliest_date >= 1925) and (earliest_date <= 1937):
				range_dates.append(an_object)
			else:
				other_dates.append(an_object)

print("Count of objects with no dates: " + str(len(no_dates)))
print("Count of objects within date range: " + str(len(range_dates)))
print("Count of objects outside of date range: " + str(len(other_dates)))

json.dump(no_dates,open("hopper_nodates.json","w"),indent=4)
json.dump(range_dates,open("hopper_dates.json","w"),indent=4)
json.dump(other_dates,open("hopper_otherdates.json","w"),indent=4)