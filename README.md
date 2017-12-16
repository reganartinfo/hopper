# Hopper at the Theatre

## Linked Open Data for Museums Fellowship, 2017-2018
[Whitney Museum of American Art](https://whitney.org/) x [Pratt Institute School of Information](https://www.pratt.edu/academics/information/)

## Overview
This project investigates the cultural and theatrical landscape of Edward Hopper’s New York using linked open data (LOD) technologies. Leveraging the unparalleled collection of Hopper’s art and archival materials held by the Whitney Museum of American Art, Hopper at the Theatre contextualizes the artist’s personal and professional geographies towards the end of the interwar period circa 1925 to 1937. Part one of Hopper at the Theatre targets primary source data for semantic enrichment from event ticket stubs in the newly established Sanborn Hopper Archive. By reconciling and transforming this unique dataset with additional raw data from external information silos and linking the result to open knowledge bases, this project will deliver an easily accessible and dynamic endpoint for users to interactively discover and explore the material memory of Hopper’s New York City. Selected reflections of this dataset will be used to emphasize interesting patterns in order to draw out engaging and perhaps hidden narratives from the artist’s day-to-day.

The [preliminary deliverable](https://reganartinfo.github.io/hopper/) is an interactive map built with [Leaflet](http://leafletjs.com/) and [Stamen Maps](http://maps.stamen.com/) to satisfy the course requirements for [Programming for Cultural Heritage](http://pfch.nyc/) (LIS-664-01). Each icon on the Leaflet map marks a distinct theatre's geographical point. Clicking on any marker opens a popup containing the following information:
* The theatre's name
* The theatre's address
* The count of ticket stubs issued by the theatre and saved by Edward Hopper
* A list of shows attended by Edward Hopper at the theatre, including:
  * The show's title
  * The year Hopper attended the show
  * The name of the show's playwright (if available)
  * The playwright's Wikidata ID (if available)

## Data Sources
Primary source metadata has been generously provided by the Whitney Museum of American Art, along with access to their Collection Data Server/System (CDS) API. Additional data sources include:
* [Carnegie Hall Archives Linked Data](https://github.com/CarnegieHall/linked-data)
* [Cinema Treasures](http://cinematreasures.org/)
* [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/start)
* [Internet Broadway Database](https://www.ibdb.com/)
* [Internet Movie Database](https://www.imdb.com/)
* [Wikidata API](https://www.wikidata.org/w/api.php)

## Implementation
Clone or download the repo to create a local copy on your computer. Open your CLI, change your working directory to **_hopper_**, and enter the following command to run *all* data ingestion scripts.
```
$python3 hopper.py
```
Enriched datasets should automatically be created and modfied in the **_hopper/data_** directory. To set up a local testing server and play with the Leaflet visualization, set **_hopper_** as your working directory, and enter the following command:
```
$python3 -m http.server
```
Then, open a new browser window to http://0.0.0.0:8000/
