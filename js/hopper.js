// creates map of Broadway theater district
var mymap = L.map('mapid').setView([40.7590, -73.9845], 14);

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
		iconAnchor: [0,50],
		popupAnchor: [22,-30]
	}
});

var redIcon = new ticketIcon({iconUrl: 'http://icon-park.com/imagefiles/location_map_pin_orange10.png'});

// http://youmightnotneedjquery.com/
// AJAX request
var request = new XMLHttpRequest();
request.open('GET', '/final_ticket_data.json', true);

request.onload = function() {
  if (request.status >= 200 && request.status < 400) {
    // success!
    var hopperData = JSON.parse(request.responseText);
    hopperData.forEach(function(hdata){
      var venueName = hdata.venue_name_ibdb;
      var venueAddress = hdata.venue_address_ibdb_googlezip;
      var venueLat = hdata.google_geocode_api[0].geometry.location.lat;
      var venueLng = hdata.google_geocode_api[0].geometry.location.lng;
      var tickets = hdata.tickets;
      var ticketCount = tickets.length;
      var addressPop = '<b>'+venueName+'</b><br/>'+venueAddress+'<br/>Ticket Count: '+ticketCount+'<br/>';

      var ticketPop = ''
      tickets.forEach(function(tdata){
        var eventTitle = tdata.event_title_ibdb;
        var eventYear = tdata.event_year_hopper;
        var writerName = tdata.writer_name_ibdb;
        if (writerName == 'NULL') {
          writerName = 'N/A';
        };
        var wikiID = tdata.writer_id_wikidata;
        ticketPop = ticketPop+'<br/>Production: <i>'+eventTitle+'</i> ('+eventYear+')<br/>Written by: '+writerName;
        if (wikiID == 'NULL') {
          var wikiPop = ''
        } else {
          var wikiPop = ' (<a href="https://www.wikidata.org/wiki/'+wikiID+'" target="_blank">'+wikiID+'</a>)';
        };
        ticketPop = ticketPop+wikiPop+'<br/>';
      });

      addressPop = addressPop+ticketPop

      L.marker([venueLat, venueLng], {icon: redIcon}).addTo(mymap).bindPopup(addressPop);

    });
  } else {
    // reached our target server, but it returned an error
  }
};

request.onerror = function() {
  // there was a connection error of some sort
};

request.send();