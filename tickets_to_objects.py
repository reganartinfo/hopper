from collections import Counter
import json

def objectCounter(jsonfile):
	with open(jsonfile,"r") as f:
		encoder = json.load(f)

		no_date_counter = 0
		object_counter = 0
		strong_match_counter = 0
		weak_match_counter = 0

		exact_matches = []

		for an_object in encoder:
			object_counter += 1
			if an_object["display_date"] == "n.d.":
				no_date_counter += 1
			else:
				earliest_date = int(an_object["earliest_date"])
				latest_date = int(an_object["latest_date"])
				if earliest_date==latest_date:
					strong_match_counter += 1
					exact_matches.append(earliest_date)
				else:
					weak_match_counter += 1

		print("num of objects: " + str(object_counter))
		print("n.d. count: " + str(no_date_counter))
		print("strong match count: " + str(strong_match_counter))
		print("exact matches: " + str(Counter(exact_matches)))
		print("weak match count: " + str(weak_match_counter))

objectCounter("hopper_final_dates.json")