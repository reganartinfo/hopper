from bs4 import BeautifulSoup
import re, requests, json

ibdb_search = "https://www.ibdb.com/broadway-production/8372"
ibdb_request = requests.get(ibdb_search, verify=False)

ibdb_html = ibdb_request.text
soup = BeautifulSoup(ibdb_html,"html.parser")

pythex = re.compile("[0-9]*$")

production_table = soup.find("table",attrs={"class":"production-staff"})
table_rows = production_table.findAll("td")

for a_row in table_rows:
	if "Written" in a_row.contents[0]:
		writer_data = a_row.find("a")
		writer_href = writer_data['href']
		writer_id = pythex.findall(writer_href)[0]
		writer_name = writer_data.string
		print(writer_name, writer_id)