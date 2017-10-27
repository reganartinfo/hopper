import requests, json

query = {"format":"json", "artist_id":"621"}
r = requests.get("http://collection.whitney.org/json/objects", params=query)

if r.status_code != 200:
	print ("There was an error with", r)

data = json.loads(r.text)

# total_count = total # of results that match query
total_count = data["count"]
# CDS API returns 1 page with 36 results per request --> params cannot be changed :(
page_count = round(total_count/36)
# initialize page param
page = 1
# set array for results
hopper_objects = []

# while loop makes request + increments page # until all results are returned
while page <= page_count:
	print("Requesting page " + str(page) + " . . .")
	query = {"format":"json", "artist_id":"621", "page":page}
	r = requests.get("http://collection.whitney.org/json/objects", params=query)
	data = json.loads(r.text)
	for an_object in data["results"]:
		hopper_objects.append(an_object)
	page += 1

# stores json results for later with pretty print
json.dump(hopper_objects,open("hopper.json","w"), indent=4)