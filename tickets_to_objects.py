from collections import Counter
import json

def objectCounter(jsonfile):
	# opens json dump written by hopper_better_dates.py
	with open(jsonfile,"r") as f:
		encoder = json.load(f)

		# init counters
		no_date_counter = 0
		object_counter = 0
		strong_match_counter = 0
		weak_match_counter = 0

		# set array for exact matches
		exact_matches = []

		# creates dict counter for weak matches
		ticket_years = list(range(1925,1938))
		ticket_dict = dict.fromkeys(ticket_years,0)

		# loops through each json object + increments total object counter
		for an_object in encoder:
			object_counter += 1

			# checks for an object with no date ("n.d.") + increments no date counter
			if an_object["display_date"] == "n.d.":
				no_date_counter += 1
			else:
				# checks for strong date matches (i.e. when earliest_date == latest_date) + increments strong match counter
				earliest_date = int(an_object["earliest_date"])
				latest_date = int(an_object["latest_date"])
				if earliest_date==latest_date:
					strong_match_counter += 1
					exact_matches.append(earliest_date)
				else:
					# increments weak match counter
					weak_match_counter += 1
					# loops through ticket dates in dict counter
					for a_year in ticket_dict:
						# increments weak date by year if in range
						if (earliest_date <= a_year) and (latest_date >= a_year):
							ticket_dict[a_year] += 1

		# sanity checks/status update
		print("num of objects: " + str(object_counter))
		print("n.d. count: " + str(no_date_counter))
		print("strong match count: " + str(strong_match_counter))
		print("exact matches: " + str(Counter(exact_matches)))
		print("weak match count: " + str(weak_match_counter))
		print(ticket_dict)

objectCounter("hopper_final_dates.json")