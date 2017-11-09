import json, re

def getDates(filename):
	# set arrays for dates
	clean_dates = []
	messy_dates = []
	no_dates = []
	no_range = []

	# set arrays for range_dates counter
	a_counter = []

	# opens hopper_dump.json written by cds_request.py
	with open(filename,"r") as f:
		encoder = json.load(f)

		# loops through each json object in hopper_dump + by display date value
		for an_object in encoder:
			object_date = an_object["display_date"]
			# creates earliest date and latest date keys + values
			earliest_date = {"earliest_date": object_date}
			latest_date = {"latest_date": object_date}

			# checks for messy display dates + appends object to messy_dates array
			if len(object_date) > 4:
				messy_dates.append(an_object)

			# checks for an object with no date ("n.d.") + appends object to no_dates array
			elif object_date == "n.d.":
				an_object.update(earliest_date)
				an_object.update(latest_date)
				no_dates.append(an_object)

			else:
				# appends object that fall into range (1925-1937, inclusive) to clean_dates array 
				if (int(object_date) >= 1925) and (int(object_date) <= 1937):
					an_object.update(earliest_date)
					an_object.update(latest_date)
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

def cleanDates(filename1,filename2):
	char_count = []
	clean_dates = []

	pythex_year = re.compile("[0-9]{4}")
	pythex_head = re.compile("^[0-9]{2}")
	pythex_tail = re.compile("[0-9]{2}$")

	with open(filename1,"r") as f:
		encoder = json.load(f)

		for an_object in encoder:
			object_date = an_object["display_date"]
			# creates earliest date and latest date keys + values
			earliest_date = {"earliest_date": object_date}
			latest_date = {"latest_date": object_date}

			# cleans c.xxxx, including adding space to display date
			if len(object_date) == 6:
				no_circa = pythex_year.findall(object_date)
				an_object["display_date"] = "ca. " + no_circa[0]
				earliest_date["earliest_date"] = int(no_circa[0]) - 5
				latest_date["latest_date"] = int(no_circa[0]) + 5
				an_object.update(earliest_date)
				an_object.update(latest_date)
				clean_dates.append(an_object)

			if len(object_date) == 7:
				# cleans c. xxxx
				if "c." in object_date:
					no_circa = pythex_year.findall(object_date)
					earliest_date["earliest_date"] = int(no_circa[0]) - 5
					latest_date["latest_date"] = int(no_circa[0]) + 5
					an_object.update(earliest_date)
					an_object.update(latest_date)
					clean_dates.append(an_object)
				#cleans xxxx-xx
				else:
					full_year = pythex_year.findall(object_date)
					head = pythex_head.findall(object_date)
					tail = pythex_tail.findall(object_date)
					new_year = head[0] + tail[0]
					earliest_date["earliest_date"] = full_year[0]
					latest_date["latest_date"] = new_year
					an_object.update(earliest_date)
					an_object.update(latest_date)
					clean_dates.append(an_object)

			if len(object_date) == 9:
				# cleans c.xxxx-xx, including adding space to display date
				if "c." in object_date:
					no_circa = pythex_year.findall(object_date)
					earliest_date["earliest_date"] = int(no_circa[0]) - 5
				print(object_date)

# getDates("hopper_dump.json")
cleanDates("hopper_messydates.json","hopper_cleandates.json")