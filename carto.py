import json

def getGeo(json_input,json_output):
	with open(json_input,'r') as f_in:
		encoder_in = json.load(f_in)

		output_data = []

		for an_object in encoder_in:
			lat_data = an_object['google_geocode_api'][0]['geometry']['location']['lat']
			lng_data = an_object['google_geocode_api'][0]['geometry']['location']['lng']
			an_object.pop('google_geocode_api')
			an_object['latitude'] = lat_data
			an_object['longitude'] = lng_data
			output_data.append(an_object)

		json.dump(output_data,open(json_output,'w'),indent=4)

getGeo('final_ticket_data.json','hopper_carto.json')