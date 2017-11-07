import json

# set arrays for dates
clean_dates = []
messy_dates = []
no_dates = []
no_range = []

# set arrays for range_dates counter
a_counter = []

# opens hopper_dump.json written by cds_request.py
with open("hopper_dump.json","r") as f:
	encoder = json.load(f)

	# loops through each json object in hopper_dump + by display date value
	for an_object in encoder:
		object_date = an_object["display_date"]

		# checks for messy display dates + appends object to messy_dates array
		if len(object_date) > 4:
			messy_dates.append(an_object)

		# checks for an object with no date ("n.d.") + appends object to no_dates array
		elif object_date == "n.d.":
			no_dates.append(an_object)

		else:
			# appends object that fall into range (1925-1937, inclusive) to clean_dates array 
			if (int(object_date) >= 1925) and (int(object_date) <= 1937):
				clean_dates.append(an_object)
				a_counter.append(object_date)
			# appends object that falls outside range to no_range array
			else:
				no_range.append(an_object)

# status updates
print("Count of objects with clean dates within range: " + str(len(clean_dates)))
# counts clean dates within range by frequency
sorted_dates = sorted(a_counter)
range_dates_freq = dict((i, sorted_dates.count(i)) for i in sorted_dates)
print(range_dates_freq)

print("Count of objects with clean dates outside range: " + str(len(no_range)))
print("Count of objects with messy dates: " + str(len(messy_dates)))
print("Count of objects with no dates: " + str(len(no_dates)))

# stores sorted json results for later with pretty print
# hopper_cleandates.json = the goods!
json.dump(no_dates,open("hopper_nodates.json","w"),indent=4)
json.dump(clean_dates,open("hopper_cleandates.json","w"),indent=4)
json.dump(messy_dates,open("hopper_messydates.json","w"),indent=4)
json.dump(no_range,open("hopper_norange.json","w"),indent=4)