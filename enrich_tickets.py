from bs4 import BeautifulSoup
import csv, json, re, requests
# from itertools import chain

def enrichTickets():

	def ibdbRequest(csv_input,csv_output):
		with open(csv_output,'w') as f_out:
			writer = csv.writer(f_out)
			with open(csv_input,'r') as f_in:
				reader = csv.reader(f_in)
				for row in reader:
					ibdb_production_id = row[9]

					ibdb_search = 'https://www.ibdb.com/broadway-production/' + ibdb_production_id
					ibdb_request = requests.get(ibdb_search, verify=False)
					ibdb_html = ibdb_request.text
					print(ibdb_html)

					ibdb_soup = BeautifulSoup(ibdb_html,'html.parser')
					pythex = re.compile('[0-9]*$')
					production_table = ibdb_soup.find('table',attrs={'class':'production-staff'})
					table_rows = production_table.findAll('td')

					for a_row in table_rows:
						if 'Written' in a_row.contents[0]:
							writer_data = a_row.find('a')
							writer_href = writer_data['href']
							ibdb_writer_id = pythex.findall(writer_href)[0]
							ibdb_writer_name = writer_data.string

							row[14] = ibdb_writer_name
							row[15] = ibdb_writer_id

					writer.writerow(row)

	# ibdbRequest('confirmed_tickets.csv','ibdb_ticket_data.csv')

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

	def addProductions(csv_input,csv_output):
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

	# addProductions('ibdb_ticket_data.csv','wiki_production_data.csv')

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

	# addShows('wiki_production_data.csv','wiki_show_data.csv')

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

	# addPlaywrights('wiki_show_data.csv','wiki_playwright_data.csv')

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

	# addVenues('wiki_playwright_data.csv','wiki_venue_data.csv')

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
				# ticket_dict = dict(zip(ticket_headers,ticket_rows))

			for a_venue in all_data:
				a_venue['tickets'] = []
				for a_ticket in ticket_data:
					if a_venue['venue_id_ibdb'] == a_ticket[0]:
						ticket_dict = dict(zip(ticket_headers[1:],a_ticket[1:]))
						a_venue['tickets'].append(ticket_dict)

			json.dump(all_data,open(json_output,'w'),indent=4)

	# nestTickets('wiki_venue_data.csv','nested_ticket_data.json')

	def addGeocodes(json_input,json_output,api_key):
		with open(json_input,'r') as f:
			encoder = json.load(f)

			all_data = []
			for an_object in encoder:
				address = an_object['venue_address_ibdb_googlezip'].split()
				address_start = address[0]
				query = address_start

				for el in address[1:]:
					query += "+" + el

				payload = {'address': query, 'key': api_key}
				r = requests.get('https://maps.googleapis.com/maps/api/geocode/json?',params=payload)
				api_results = json.loads(r.text)
				an_object['google_geocode_api'] = api_results['results']
				all_data.append(an_object)

			json.dump(all_data,open(json_output,'w'),indent=4)

	addGeocodes('nested_ticket_data.json','final_ticket_data.json','AIzaSyDElq1yMMEFinn3sYd3I02xrJSxKShesBg')

enrichTickets()