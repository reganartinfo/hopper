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
			# creates earliest date and latest date keys + values for indexing
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
				# appends objects that 1) have a "natural" 4-digit int for their display date + 2) fall into range (1925-1937, inclusive) to clean_dates array
				if (int(object_date) >= 1925) and (int(object_date) <= 1937):
					earliest_date["earliest_date"] = int(object_date)
					latest_date["latest_date"] = int(object_date)
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
	# hopper_cleandates1.json == the goods!
	json.dump(no_dates,open("hopper_nodates.json","w"),indent=4)
	json.dump(clean_dates,open("hopper_cleandates1.json","w"),indent=4)
	json.dump(messy_dates,open("hopper_messydates.json","w"),indent=4)
	json.dump(no_range,open("hopper_norange.json","w"),indent=4)

# cleans messy dates following CCO standards for indexing
def cleanDates(filename1):
	# set arrays for dates
	clean_dates = []
	in_range = []

	# pythex_var = various regexes to help scrape dates
	pythex_year = re.compile("[0-9]{4}")
	pythex_start = re.compile("^[0-9]{4}")
	pythex_end = re.compile("[0-9]{4}$")
	pythex_head = re.compile("^[0-9]{2}")
	pythex_tail = re.compile("[0-9]{2}$")

	with open(filename1,"r") as f1:
		encoder1 = json.load(f1)

		for an_object in encoder1:
			object_date = an_object["display_date"]
			# creates earliest date and latest date keys + values
			earliest_date = {"earliest_date": object_date}
			latest_date = {"latest_date": object_date}

			# cleans c.xxxx, including adding space to display date
			if len(object_date) == 6:
				search = pythex_year.findall(object_date)
				an_object["display_date"] = "ca. " + search[0]
				earliest_date["earliest_date"] = int(search[0]) - 5
				latest_date["latest_date"] = int(search[0]) + 5
				an_object.update(earliest_date)
				an_object.update(latest_date)
				clean_dates.append(an_object)

			if len(object_date) == 7:
				# cleans c. xxxx
				if "c." in object_date:
					search = pythex_year.findall(object_date)
					an_object["display_date"] = "ca. " + search[0]
					earliest_date["earliest_date"] = int(search[0]) - 5
					latest_date["latest_date"] = int(search[0]) + 5
					an_object.update(earliest_date)
					an_object.update(latest_date)
					clean_dates.append(an_object)
				# cleans xxxx-xx
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
					search = object_date[2:]
					an_object["display_date"] = "ca. " + search
					full_year = pythex_year.findall(search)
					head = pythex_head.findall(search)
					tail = pythex_tail.findall(search)
					new_year = head[0] + tail[0]
					earliest_date["earliest_date"] = int(full_year[0]) - 5
					latest_date["latest_date"] = new_year
					an_object.update(earliest_date)
					an_object.update(latest_date)
					clean_dates.append(an_object)
				# cleans xxxx-xxxx	
				else:
					search = pythex_year.findall(object_date)
					earliest_date["earliest_date"] = search[0]
					latest_date["latest_date"] = search[1]
					an_object.update(earliest_date)
					an_object.update(latest_date)
					clean_dates.append(an_object)

			if len(object_date) == 10:
				# cleans After xxxx
				if "After" in object_date:
					search = pythex_year.findall(object_date)
					earliest_date["earliest_date"] = search[0]
					latest_date["latest_date"] = int(search[0]) + 10
					an_object.update(earliest_date)
					an_object.update(latest_date)
					clean_dates.append(an_object)
				# cleans c. xxxx-xx
				else:
					search = object_date[3:]
					an_object["display_date"] = "ca. " + search
					full_year = pythex_year.findall(search)
					head = pythex_head.findall(search)
					tail = pythex_tail.findall(search)
					new_year = head[0] + tail[0]
					earliest_date["earliest_date"] = int(full_year[0]) - 5
					latest_date["latest_date"] = new_year
					an_object.update(earliest_date)
					an_object.update(latest_date)
					clean_dates.append(an_object)

			if len(object_date) == 12:
				# cleans c. xxxx-xxxx
				if "c." in object_date:
					search = object_date[3:]
					an_object["display_date"] = "ca. " + search
					full_year = pythex_year.findall(search)
					earliest_date["earliest_date"] = int(full_year[0]) - 5
					latest_date["latest_date"] = full_year[1]
					an_object.update(earliest_date)
					an_object.update(latest_date)
					clean_dates.append(an_object)
				# cleans xxxx or xxxx
				else:
					search = pythex_year.findall(object_date)
					earliest_date["earliest_date"] = search[0]
					latest_date["latest_date"] = search[1]
					an_object.update(earliest_date)
					an_object.update(latest_date)
					clean_dates.append(an_object)

			# cleans xxxx, posthumous print
			if len(object_date) == 22:
				search = pythex_year.findall(object_date)
				earliest_date["earliest_date"] = search[0]
				latest_date["latest_date"] = search[0]
				an_object.update(earliest_date)
				an_object.update(latest_date)
				clean_dates.append(an_object)

			if len(object_date) == 25:
				# cleans c. xxxx, posthumous print
				if "c." in object_date:
					search = object_date[3:]
					an_object["display_date"] = "ca. " + search
					full_year = pythex_year.findall(search)
					earliest_date["earliest_date"] = int(full_year[0]) - 5
					latest_date["latest_date"] = int(full_year[0]) + 5
					an_object.update(earliest_date)
					an_object.update(latest_date)
					clean_dates.append(an_object)
				# cleans xxxx-xx, posthumous print	
				else:
					full_year = pythex_year.findall(search)
					head = pythex_head.findall(search)
					tail = pythex_tail.findall(search)
					new_year = head[0] + tail[0]
					earliest_date["earliest_date"] = full_year[0]
					latest_date["latest_date"] = new_year
					an_object.update(earliest_date)
					an_object.update(latest_date)
					clean_dates.append(an_object)

	# appends objects that fall into range (1925-1937, inclusive) to in_range array  
	for a_date in clean_dates:
		if ((int(a_date["earliest_date"]) >= 1925) and (int(a_date["earliest_date"]) <= 1937)) or ((int(a_date["latest_date"]) >= 1925) and (int(a_date["latest_date"]) <= 1937)):
			in_range.append(a_date)

	# stores sorted json results for later with pretty print
	json.dump(in_range,open("hopper_cleandates2.json","w"),indent=4)

# merges "naturally" clean dates with dates needing more TLC, both within range
def mergeDates(filename1, filename2):
	with open(filename1,"r") as f1:
		encoder1 = json.load(f1)
		with open(filename2,"r") as f2:
			encoder2 = json.load(f2)
			for an_object in encoder1:
				encoder2.append(an_object)
			# squeaky clean date index :)
			json.dump(encoder2,open("hopper_scrubbed.json","w"),indent=4)

getDates("hopper_dump.json")
cleanDates("hopper_messydates.json")
mergeDates("hopper_cleandates1.json","hopper_cleandates2.json")