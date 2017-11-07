import json, re

# set arrays for dates
range_dates = []
no_dates = []
other_dates = []

# set arrays for range_dates counter
a_counter = []

# pythex_date = regex for year
pythex_date = re.compile("\d{4}")

# opens hopper_dump.json written by cds_request.py
with open("hopper_dump.json","r") as f:
	encoder = json.load(f)

	# loops through each json object in hopper_dump + by display date value
	for an_object in encoder:
		object_date = an_object["display_date"]

		# checks for an object with no date ("n.d.") + appends object to no_dates array
		if object_date == "n.d.":
			no_dates.append(an_object)

		# checks for an object with dates
		else:
			regex_date = pythex_date.findall(object_date)
			earliest_date = int(regex_date[0])

			# appends object that fall into range (1925-1937, inclusive) to range_dates array 
			if (earliest_date >= 1925) and (earliest_date <= 1937):
				range_dates.append(an_object)
				a_counter.append(earliest_date)
			# appends object that falls outside range to other_dates array
			else:
				other_dates.append(an_object)

# status update
print("Count of objects with no dates: " + str(len(no_dates)))
print("Count of objects within date range: " + str(len(range_dates)))
print("Count of objects outside of date range: " + str(len(other_dates)))

sorted_dates = sorted(a_counter)
range_dates_count = dict((i, sorted_dates.count(i)) for i in sorted_dates)
print(range_dates_count)

# # stores sorted json results for later with pretty print
# # hopper_dates.json = the goods!
# json.dump(no_dates,open("hopper_nodates.json","w"),indent=4)
# json.dump(range_dates,open("hopper_dates.json","w"),indent=4)
# json.dump(other_dates,open("hopper_otherdates.json","w"),indent=4)