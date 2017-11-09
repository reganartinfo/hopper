from urllib.request import urlretrieve
import json, os

new_directory = "theater_images"
url_head = "http://collectionimages.whitney.org/standard/"
url_tail = "/largerpage.jpg"

directory = "/"

with open("hopper_dump.json","r") as f:
	cwd = os.getcwd()
	filepath = os.path.join(cwd,new_directory)
	if not os.path.exists(filepath):
	 	os.mkdir(filepath)
	os.chdir(filepath)

	encoder = json.load(f)
	for an_object in encoder:
		title = an_object["title"]
		if "theat" in title or "Theat" in title or "movie" in title or "Movie" in title or "bicycle" in title or "Bicycle" in title:
			image_id = str(an_object["primary_image_id"])
			url = url_head + image_id + url_tail
			filename = image_id + ".jpg"
			urlretrieve(url,filename)