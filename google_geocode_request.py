import csv, json, requests

def geocodeRequest(csvfile, jsonfile, key):
	with open(csvfile,"r") as f:
		reader = csv.reader(f)
		all_data = []
		key_list = []
		header_row = next(reader)
		for a_field in header_row:
			key_list.append(a_field)

		for row in reader:
			address = row[4].split()
			street_num = address[0]
			query = street_num

			for el in address[1:]:
				query += "+" + el
			
			payload = {"address": query, "key": key}
			r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?",params=payload)
			api_results = json.loads(r.text)
			ticket_stub = dict(zip(key_list,row))
			ticket_stub["google_geocode_api"] = api_results["results"]
			all_data.append(ticket_stub)

		json.dump(all_data,open(jsonfile,"w"),indent=4)