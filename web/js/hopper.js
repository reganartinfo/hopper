// creates map of Broadway theater district
var mymap = L.map('mapid').setView([40.7590, -73.9845], 13);

// imports Stamen's toner map style
var tonerUrl = "http://{S}tile.stamen.com/toner/{Z}/{X}/{Y}.png";
var url = tonerUrl.replace(/({[A-Z]})/g, function(s) {
    return s.toLowerCase();
});

// adds tile layer
var basemap = L.tileLayer(url, {
    subdomains: ['','a.','b.','c.','d.'],
    minZoom: 0,
    maxZoom: 20,
    type: 'png',
    attribution: 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>'
});
basemap.addTo(mymap);

// creates custom ticket icons
var ticketIcon = L.Icon.extend({
	options: {
		iconSize: [50,50],
		iconAnchor: [25,25],
		popupAnchor: [3,-15]
	}
});

var redIcon = new ticketIcon({iconUrl: 'https://image.ibb.co/dYMAcw/ticket_red.png'}),
    yellowIcon = new ticketIcon({iconUrl: 'https://image.ibb.co/b8bnPb/ticket_yellow.png'}),
    blueIcon = new ticketIcon({iconUrl: 'https://image.ibb.co/fpyCqG/ticket_blue.png'}),
    blackIcon = new ticketIcon({iconUrl: 'https://image.ibb.co/hkUwHw/ticket_black.png'});

// http://youmightnotneedjquery.com/
// AJAX request
var request = new XMLHttpRequest();
request.open('GET', '/theatre_only.json', true);

request.onload = function() {
  if (request.status >= 200 && request.status < 400) {
    // success!
    var hopperData = JSON.parse(request.responseText);
    hopperData.forEach(function(hdata){
      var venueName = hdata.venue_name_ibdb;
      var venueAddress = hdata.venue_address_ibdb_googlezip;
      var venueLat = hdata.google_geocode_api[0].geometry.location.lat;
      var venueLng = hdata.google_geocode_api[0].geometry.location.lng;

      // adds custom marker to map
      L.marker([venueLat, venueLng], {icon: redIcon}).addTo(mymap).bindPopup('<b>'+venueName+'</b><br/>'+venueAddress);
    });
  } else {
    // reached our target server, but it returned an error
  }
};

request.onerror = function() {
  // there was a connection error of some sort
};

request.send();