from bs4 import BeautifulSoup
from collections import Counter
from itertools import cycle
from urllib.request import urlretrieve
import csv, json, re, requests, os

# functions for artwork by Edward Hopper in the Whitney's permanent collection (referred to as 'Objects' in TMS)
def hopperObjects():

	# checks if path exists for data directory before making CDS API requests
	def dataPathCheck(query,json_output):
		cwd = os.getcwd()
		filepath = os.path.join(cwd,'data')
		if not os.path.exists(filepath):
			os.mkdir(filepath)
		os.chdir(filepath)

		filepath = os.path.join(os.getcwd(),json_output)
		
		# checks if json dump already exists
		if os.path.exists(filepath):

			# asks for user input if they want to overwrite it
			choice = input('A copy of '+json_output+' already exists. Do you wish to overwrite it? [y/n]\n')
			if choice == 'y':
				print('Beginning to make requests to CDS API for JSON collection data from the Whitney Museum . . .')
				cdsRequest(query,json_output)
			elif choice == 'n':
				print('Got it. No CDS API request will be made.')
			else:
				print('Invalid choice, buddy.')

		else:
			cdsRequest(query,json_output)

	# makes CDS API requests for all Hopper-related Objects
	def cdsRequest(query,json_output):
		r = requests.get('http://collection.whitney.org/json/objects', params=query)

		if r.status_code != 200:
			print ('There was an error with', r)

		data = json.loads(r.text)
		total_count = data['count']

		# CDS API returns 1 page with 36 results per request --> params cannot be changed :(
		page_count = round(total_count/36)
		page = 1
		hopper_objects = []

		# while loop makes request + increments page # until all results are returned
		while page <= page_count:
			print('Requesting page ' + str(page) + ' . . .')
			query = {'format':'json', 'artist_id':'621', 'page':page}
			r = requests.get('http://collection.whitney.org/json/objects', params=query)
			data = json.loads(r.text)
			for an_object in data['results']:
				hopper_objects.append(an_object)
			page += 1

		# stores json results for later use with pretty print
		json.dump(hopper_objects,open(json_output,'w'), indent=4)

		# cd
		os.chdir('..')

	# cleans messy dates following CCO standards for indexing
	def cleanDates(json_input,json_output):
		re_year = re.compile('[0-9]{4}')
		re_start = re.compile('^[0-9]{4}')
		re_end = re.compile('[0-9]{4}$')
		re_head = re.compile('^[0-9]{2}')
		re_tail = re.compile('[0-9]{2}$')

		with open(json_input,'r') as f:
			encoder = json.load(f)

			all_dates = []		

			# loops through each json object in hopper_dump
			for an_object in encoder:
				object_date = an_object['display_date']
				# creates earliest date and latest date keys + values
				earliest_date = {'earliest_date': object_date}
				latest_date = {'latest_date': object_date}
				
				# checks for an object with no date ("n.d.")
				if (object_date == 'n.d.') or (len(object_date) == 4):
					an_object.update(earliest_date)
					an_object.update(latest_date)

				else:
					# cleans c.xxxx, including adding space to display date
					if len(object_date) == 6:
						search = re_year.findall(object_date)
						an_object['display_date'] = 'ca. ' + search[0]
						earliest_date['earliest_date'] = int(search[0]) - 5
						latest_date['latest_date'] = int(search[0]) + 5
						an_object.update(earliest_date)
						an_object.update(latest_date)

					if len(object_date) == 7:
						# cleans c. xxxx
						if 'c.' in object_date:
							search = re_year.findall(object_date)
							an_object['display_date'] = 'ca. ' + search[0]
							earliest_date['earliest_date'] = int(search[0]) - 5
							latest_date['latest_date'] = int(search[0]) + 5
							an_object.update(earliest_date)
							an_object.update(latest_date)
						# cleans xxxx-xx
						else:
							full_year = re_year.findall(object_date)
							head = re_head.findall(object_date)
							tail = re_tail.findall(object_date)
							new_year = head[0] + tail[0]
							earliest_date['earliest_date'] = full_year[0]
							latest_date['latest_date'] = new_year
							an_object.update(earliest_date)
							an_object.update(latest_date)

					if len(object_date) == 9:
						# cleans c.xxxx-xx
						if 'c.' in object_date:
							search = object_date[2:]
							an_object['display_date'] = 'ca. ' + search
							full_year = re_year.findall(search)
							head = re_head.findall(search)
							tail = re_tail.findall(search)
							new_year = head[0] + tail[0]
							earliest_date['earliest_date'] = int(full_year[0]) - 5
							latest_date['latest_date'] = new_year
							an_object.update(earliest_date)
							an_object.update(latest_date)
						# cleans xxxx-xxxx
						else:
							search = re_year.findall(object_date)
							earliest_date['earliest_date'] = search[0]
							latest_date['latest_date'] = search[1]
							an_object.update(earliest_date)
							an_object.update(latest_date)

					if len(object_date) == 10:
						# cleans After xxxx
						if 'After' in object_date:
							search = re_year.findall(object_date)
							earliest_date['earliest_date'] = search[0]
							latest_date['latest_date'] = int(search[0]) + 10
							an_object.update(earliest_date)
							an_object.update(latest_date)
						# cleans c. xxxx-xx
						else:
							search = object_date[3:]
							an_object['display_date'] = 'ca. ' + search
							full_year = re_year.findall(search)
							head = re_head.findall(search)
							tail = re_tail.findall(search)
							new_year = head[0] + tail[0]
							earliest_date['earliest_date'] = int(full_year[0]) - 5
							latest_date['latest_date'] = new_year
							an_object.update(earliest_date)
							an_object.update(latest_date)
							
					if len(object_date) == 12:
						# cleans c. xxxx-xxxx
						if 'c.' in object_date:
							search = object_date[3:]
							an_object['display_date'] = 'ca. ' + search
							full_year = re_year.findall(search)
							earliest_date['earliest_date'] = int(full_year[0]) - 5
							latest_date['latest_date'] = full_year[1]
							an_object.update(earliest_date)
							an_object.update(latest_date)
						# cleans xxxx or xxxx
						else:
							search = re_year.findall(object_date)
							earliest_date['earliest_date'] = search[0]
							latest_date['latest_date'] = search[1]
							an_object.update(earliest_date)
							an_object.update(latest_date)

					# cleans xxxx, posthumous print
					if len(object_date) == 22:
						search = re_year.findall(object_date)
						earliest_date['earliest_date'] = search[0]
						latest_date['latest_date'] = search[0]
						an_object.update(earliest_date)
						an_object.update(latest_date)

					if len(object_date) == 25:
						# cleans c. xxxx, posthumous print
						if 'c.' in object_date:
							search = object_date[3:]
							an_object['display_date'] = 'ca. ' + search
							full_year = re_year.findall(search)
							earliest_date['earliest_date'] = int(full_year[0]) - 5
							latest_date['latest_date'] = int(full_year[0]) + 5
							an_object.update(earliest_date)
							an_object.update(latest_date)
						# cleans xxxx-xx, posthumous print	
						else:
							full_year = re_year.findall(search)
							head = re_head.findall(search)
							tail = re_tail.findall(search)
							new_year = head[0] + tail[0]
							earliest_date['earliest_date'] = full_year[0]
							latest_date['latest_date'] = new_year
							an_object.update(earliest_date)
							an_object.update(latest_date)

				all_dates.append(an_object)

			# stores json results for later use with pretty print
			json.dump(all_dates,open(json_output,'w'),indent=4)

	# filters clean dates in range (1925-1937, inclusive)
	def filterDates(json_input,json_output):
		with open(json_input,'r') as f:
			encoder = json.load(f)

			filter_dates = []

			for an_object in encoder:
				earliest_date = an_object['earliest_date']
				latest_date = an_object['latest_date']

				if earliest_date == 'n.d.':
					filter_dates.append(an_object)

				else:
					# appends objects that fall into range
					if (int(earliest_date) >= 1925 and int(earliest_date) <= 1937) or (int(latest_date) >= 1925 and int(latest_date) <= 1937):
						filter_dates.append(an_object)
			
			# stores json results for later use with pretty print
			json.dump(filter_dates,open(json_output,'w'),indent=4)

	# counts # of Hopper Objects that match each ticket date, either identically (strong) or in range (weak)
	def objectCounter(jsonfile):
		with open(jsonfile,'r') as f:
			encoder = json.load(f)

			# counters
			no_date_counter = 0
			object_counter = 0
			strong_match_counter = 0
			weak_match_counter = 0

			# set array for exact matches
			# Counter subclass in sanity check will break results down by year
			exact_matches = []

			# dict for weak matches
			ticket_years = list(range(1925,1938))
			ticket_dict = dict.fromkeys(ticket_years,0)

			for an_object in encoder:
				object_counter += 1

				# checks for an object with no date ("n.d.") + increments no date counter
				if an_object['display_date'] == 'n.d.':
					no_date_counter += 1

				else:
					# checks for strong date matches (i.e. when earliest_date == latest_date) + increments strong match counter
					earliest_date = int(an_object['earliest_date'])
					latest_date = int(an_object['latest_date'])
					if earliest_date==latest_date:
						strong_match_counter += 1
						exact_matches.append(earliest_date)

					else:
						# increments weak match counter
						weak_match_counter += 1
						for a_year in ticket_dict:
							# checks for weak date matches
							if (earliest_date <= a_year) and (latest_date >= a_year):
								ticket_dict[a_year] += 1

			print('num of objects: ' + str(object_counter))
			print('n.d. count: ' + str(no_date_counter))
			print('strong match count: ' + str(strong_match_counter))
			print('exact matches: ' + str(Counter(exact_matches)))
			print('weak match count: ' + str(weak_match_counter))
			print(ticket_dict)

	dataPathCheck({'format':'json', 'artist_id':'621'},'hopper_dump.json')
	cleanDates('hopper_dump.json','hopper_object_dates.json')
	filterDates('hopper_object_dates.json','hopper_final_dates.json')
	objectCounter('hopper_final_dates.json')

# functions for ticket stubs from events attended by Edward Hopper in the Whitney's archives
def enrichTickets():

	# scrapes playwright name and IBDB person ID from IBDB
	def ibdbRequest(csv_input,csv_output):
		# opens empty CSV for writing with enriched data
		with open(csv_output,'w') as f_out:
			writer = csv.writer(f_out)

			# opens CSV with ticket data (exported from Google Sheets)
			with open(csv_input,'r') as f_in:
				reader = csv.reader(f_in)

				for row in reader:
					ibdb_production_id = row[9]
					# concatenates URL with IBDB Production ID slug
					ibdb_search = 'https://www.ibdb.com/broadway-production/' + ibdb_production_id
					ibdb_request = requests.get(ibdb_search, verify=False)
					ibdb_html = ibdb_request.text
					ibdb_soup = BeautifulSoup(ibdb_html,'html.parser')
					# regex to help scrape IBDB Playwright ID
					pythex = re.compile('[0-9]*$')
					production_table = ibdb_soup.find('table',attrs={'class':'production-staff'})
					table_rows = production_table.findAll('td')

					# looks for tag with "Written" (e.g. "Written by") + plucks ID from href attr + grabs playwright name from content
					for a_row in table_rows:
						if 'Written' in a_row.contents[0]:
							writer_data = a_row.find('a')
							writer_href = writer_data['href']
							ibdb_writer_id = pythex.findall(writer_href)[0]
							ibdb_writer_name = writer_data.string

							# updates playwright data for CSV
							row[14] = ibdb_writer_name
							row[15] = ibdb_writer_id

					# writes into newly created
					writer.writerow(row)

	# sends SPARQL queries to Wikidata, returns properties for matching
	def wikidataRequest(wiki_query):
		wiki_request = requests.get(wiki_query)
		wiki_html = wiki_request.text
		wiki_soup = BeautifulSoup(wiki_html,'html.parser')
		wiki_binding = wiki_soup.findAll('binding')
		
		global wiki_results
		wiki_results = []
		for binding_tag in wiki_binding:
			uri = binding_tag.find('uri')
			literal = binding_tag.find('literal')
			if uri != None:
				wiki_id = uri.string.rsplit('/', 1)[1]
			if literal != None:
				ibdb_id = literal.string
				a_result = ibdb_id,wiki_id
				wiki_results.append(a_result)
		return(wiki_results)

	# adds Wikidata IDs for IBDB production IDs
	def addProductions(csv_input,csv_output):
		cwd = os.getcwd()
		filepath = os.path.join(cwd,'data')
		if not os.path.exists(filepath):
			os.mkdir(filepath)
		os.chdir(filepath)
		wikidataRequest('https://query.wikidata.org/sparql?query=SELECT%20%2a%20WHERE%20%7B%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP1218%20%3FInternet_Broadway_Database_production_ID.%20%7D%0A%7D%0ALIMIT%205000')
		with open(csv_output,'w') as f_out:
			writer = csv.writer(f_out)
			with open(csv_input,'r') as f_in:
				reader = csv.reader(f_in)
				header = next(reader)
				for row in reader:
					for a_result in wiki_results:
						if row[9] == str(a_result[0]):
							row[10] = a_result[1]
					writer.writerow(row)

	addProductions('confirmed_tickets.csv','wiki_production_data.csv')

	def addShows(csv_input,csv_output):
		wikidataRequest('https://query.wikidata.org/sparql?query=SELECT%20%2a%20WHERE%20%7B%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP1219%20%3FInternet_Broadway_Database_show_ID.%20%7D%0A%7D')
		with open(csv_output,'w') as f_out:
			writer = csv.writer(f_out)
			with open(csv_input,'r') as f_in:
				reader = csv.reader(f_in)
				for row in reader:
					for a_result in wiki_results:
						if row[11] == str(a_result[0]):
							row[12] = a_result[1]
					writer.writerow(row)

	addShows('wiki_production_data.csv','wiki_show_data.csv')

	def addPlaywrights(csv_input,csv_output):
		wikidataRequest('https://query.wikidata.org/sparql?query=SELECT%20%2a%20WHERE%20%7B%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP1220%20%3FInternet_Broadway_Database_person_ID.%20%7D%0A%7D')
		with open(csv_output,'w') as f_out:
			writer = csv.writer(f_out)
			with open(csv_input,'r') as f_in:
				reader = csv.reader(f_in)
				for row in reader:
					for a_result in wiki_results:
						if row[14] == str(a_result[0]):
							row[15] = a_result[1]
					writer.writerow(row)

	addPlaywrights('wiki_show_data.csv','wiki_playwright_data.csv')

	def addVenues(csv_input,csv_output):
		wikidataRequest('https://query.wikidata.org/sparql?query=SELECT%20%2a%20WHERE%20%7B%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP1217%20%3FInternet_Broadway_Database_venue_ID.%20%7D%0A%7D')
		with open(csv_output,'w') as f_out:
			writer = csv.writer(f_out)
			with open(csv_input,'r') as f_in:
				reader = csv.reader(f_in)
				for row in reader:
					for a_result in wiki_results:
						if row[0] == str(a_result[0]):
							row[1] = a_result[1]
					writer.writerow(row)

	addVenues('wiki_playwright_data.csv','wiki_venue_data.csv')

	def nestTickets(csv_input,json_output):
		with open(csv_input,'r') as f:
			reader = csv.reader(f)
			headers = ['venue_id_ibdb','venue_id_wikidata','venue_name_ibdb','venue_address_ibdb_googlezip','venue_lifecycle_ibdb','venue_status_ibdb','file_id_hopper','event_title_hopper','event_title_ibdb','production_id_ibdb','production_id_wikidata','show_id_ibdb','show_id_wikidata','writer_name_ibdb','writer_id_ibdb','writer_id_wikidata','event_category_ibdb','event_year_hopper','event_month_hopper','event_date_hopper','scope_content_hopper','note_hopper']
			venue_id_header = headers[0]
			venue_headers = headers[0:6]
			ticket_headers = headers[6:]
			ticket_headers.insert(0,venue_id_header)

			venue_data = []
			ticket_data = []
			all_data = []
			for row in reader:
				venue_id_ibdb = row[0]
				venue_rows = row[0:6]
				ticket_rows = row[6:]
				ticket_rows.insert(0,venue_id_ibdb)
				ticket_data.append(ticket_rows)
				if venue_rows not in venue_data:
					venue_data.append(venue_rows)
					venue_dict = dict(zip(venue_headers,venue_rows))
					all_data.append(venue_dict)

			for a_venue in all_data:
				a_venue['tickets'] = []
				for a_ticket in ticket_data:
					if a_venue['venue_id_ibdb'] == a_ticket[0]:
						ticket_dict = dict(zip(ticket_headers[1:],a_ticket[1:]))
						a_venue['tickets'].append(ticket_dict)

			json.dump(all_data,open(json_output,'w'),indent=4)

	nestTickets('wiki_venue_data.csv','nested_ticket_data.json')

	def addGeocodes(json_input,json_output,api_key):
		with open(json_input,'r') as f:
			encoder = json.load(f)

			all_data = []
			for an_object in encoder:
				address = an_object['venue_address_ibdb_googlezip'].split()
				address_start = address[0]
				query = address_start

				for el in address[1:]:
					query += '+' + el

				payload = {'address': query, 'key': api_key}
				r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?',params=payload)
				api_results = json.loads(r.text)
				an_object['google_geocode_api'] = api_results['results']
				all_data.append(an_object)

			json.dump(all_data,open(json_output,'w'),indent=4)

	# ibdbRequest('confirmed_tickets.csv','ibdb_ticket_data.csv')
		# N.B. code no longer works, although did scrape successfully mid-November 2017
		# function is commented out for now to keep data flowing while illustrating process
	addGeocodes('nested_ticket_data.json','final_ticket_data.json','AIzaSyDElq1yMMEFinn3sYd3I02xrJSxKShesBg')

	def wikiURLs(json_input,json_output):
		cwd = os.getcwd()
		filepath = os.path.join(cwd,'data')
		if not os.path.exists(filepath):
			os.mkdir(filepath)
		os.chdir(filepath)

		with open(json_input,'r') as f:
			encoder = json.load(f)

			all_data = []
			for an_object in encoder:
				venue_id_wikidata = an_object['venue_id_wikidata']
				an_object['venue_wikipedia_url'] = 'NULL'

				if venue_id_wikidata != 'NULL':
					wikidata_request = requests.get('https://www.wikidata.org/wiki/Special:EntityData/' + venue_id_wikidata + '.json')
					data = json.loads(wikidata_request.text)
					try:
						an_object['venue_wikipedia_url'] = data['entities'][venue_id_wikidata]['sitelinks']['enwiki']['url']
					except KeyError:
						an_object['venue_wikipedia_url'] = 'No Wikipedia entry in English available.'

				for a_ticket in an_object['tickets']:
					show_id_wikidata = a_ticket['show_id_wikidata']
					writer_id_wikidata = a_ticket['writer_id_wikidata']
					a_ticket['show_wikipedia_url'] = 'NULL'
					a_ticket['writer_wikipedia_url'] = 'NULL'

					if show_id_wikidata != 'NULL':
						wikidata_request = requests.get('https://www.wikidata.org/wiki/Special:EntityData/' + show_id_wikidata + '.json')
						data = json.loads(wikidata_request.text)
						try:
							a_ticket['show_wikipedia_url'] = data['entities'][show_id_wikidata]['sitelinks']['enwiki']['url']
						except KeyError:
							a_ticket['show_wikipedia_url'] = 'No Wikipedia entry in English available.'

					if writer_id_wikidata != 'NULL':
						wikidata_request = requests.get('https://www.wikidata.org/wiki/Special:EntityData/' + writer_id_wikidata + '.json')
						data = json.loads(wikidata_request.text)
						try:
							a_ticket['writer_wikipedia_url'] = data['entities'][writer_id_wikidata]['sitelinks']['enwiki']['url']
						except KeyError:
							a_ticket['writer_wikipedia_url'] = 'No Wikipedia entry in English available.'

				all_data.append(an_object)

			json.dump(all_data,open(json_output,'w'),indent=4)

	wikiURLs('final_ticket_data.json','wiki_urls.json')

hopperObjects()
enrichTickets()