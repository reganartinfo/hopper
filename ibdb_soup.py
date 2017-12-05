from bs4 import BeautifulSoup
import csv, json, re, requests

def playwrightData(csvfile,jsonfile):
	# all_data = set array for structured data
	all_data = []

	# opens CSV with enriched ticket data (exported from Google Sheets)
	with open(csvfile,"r") as f:
		reader = csv.reader(f)

		# converts CSV to dictionary
		for row in reader:
			csv_to_json = {"file_id": row[0], "venue_name": row[2], "venue_id": row[3], "venue_address": row[4], "venue_lifecycle": row[5], "venue_status": row[6], "event_title": row[8], "event_id": row[9], "event_category": row[10], "event_date": {"year":row[11], "month": row[12], "date": row[13]}, "scope_notes": row[14]}
			production_id = row[9]

			# concatenates URL with IBDB Production ID slug
			ibdb_search = "https://www.ibdb.com/broadway-production/" + production_id
			ibdb_request = requests.get(ibdb_search, verify=False)

			ibdb_html = ibdb_request.text
			soup = BeautifulSoup(ibdb_html,"html.parser")

			# regex to help scrape IBDB Playwright ID
			pythex = re.compile("[0-9]*$")

			production_table = soup.find("table",attrs={"class":"production-staff"})
			table_rows = production_table.findAll("td")

			# looks for tag with "Written" (e.g. "Written by") + plucks ID from href attr + grabs playwright name from content
			for a_row in table_rows:
				if "Written" in a_row.contents[0]:
					writer_data = a_row.find("a")
					writer_href = writer_data['href']
					writer_id = pythex.findall(writer_href)[0]
					writer_name = writer_data.string

					# adds playwright keys to CSV dictionary
					csv_to_json.update({"playwright_name": writer_name, "playwright_id": writer_id})

			# saves dictionary to string for JSON dump
			all_data.append(csv_to_json)

	# JSON data dump with pretty print
	json.dump(all_data,open(jsonfile,"w"),indent=4)

playwrightData("ticket_test.csv","ticket_test.json")