from twilio.rest import TwilioRestClient
import twilio.twiml
import requests
from unicodedata import normalize
import json,httplib,requests

from flask import Flask, request, session, json

app = Flask(__name__)

app.secret_key = 'testing'
 
@app.route("/")
def hello():
    return "Hello World!"

def getLatLng(barang):
	'''if request.method == 'GET':
		barang = None
		if 'barang' in request.args:
			barang = request.args.get('barang')'''

	if barang:
		url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s,%s&sensor=false' % (barang, "philippines")
		r = requests.get(url)
		location = json.loads(r.text)['results'][0]['geometry']['location']
		return location
		
	return "Barangay not found. Can't parse lat/long"


@app.route("/receive-sms", methods=['GET', 'POST'])
def reply():
	print "Received Message"

	counter = session.get('counter', 0)
	
	if request.form['Body']:
		resp = twilio.twiml.Response()
		help_request = {}
		if counter == 0: 
			resp.message("What is your Barangay? (e.g. Cabungaan)")
			session['number'] = request.form['From']
			
			# TODO: check whether it's a valid Barangay
			print session['number']

			session['counter'] += counter
			return str(resp)
		
		elif counter == 1:
			latlng = getLatLng(request.form['Body'])
			session['lat'] = latlng['lat']
			session['lng'] = latlng['lng']
			print "Lat Lng" + session['lat'] + ", " +session['lng']

			resp.message("What do you need? Enter all that apply (e.g. 12 for Water and Food): 1)Water, 2)Food, 3)Medical, 4)Shelter, 5)Electricity")
			session['counter'] += 1
			return str(resp)

		elif counter == 2:
			help_request = session.get('help_request')
			help_request['type'] = request.form['Body']
			session['help_request'] = help_request

			# TODO: handle invalid option
			# anything that is not 1-6 is invalid, only the other numbers should be taken into account
			Water=Food=Medical=Shelter=Electricity = False

			if '1' in help_request['type']:
				Water = True

			elif '2' in help_request['type']:
				Food = True

			elif '3' in help_request['type']:
				Medical = True
			
			elif '4' in help_request['type']:
				Shelter = True

			elif '5' in help_request['type']:
				Electricity = True
			
			'''# TODO: handle route 6 options
			elif '6' in help_request['type']: 
				# Present other options to the user
				resp.message("What do you need? Enter all that apply (e.g. 12 for Water and Food): 1)Water, 2)Food, 3)Medical, 4)Shelter, 5)Electricity, 6)Other")
				counter += 1
				session['counter'] = counter
				return str(resp)'''
			
			#Save to database
			connection = httplib.HTTPSConnection('api.parse.com', 443)
			connection.connect()

			connection.request('POST', '/1/classes/report', json.dumps({
				"phone_number": help_request['number'],
				"barangay": help_request['bar'], 
				"Lat": help_request['lat'],
				"Lng": help_request['lng'],
				"water" : Water,s
				"food": Food,
				"shelter" : Shelter,
				"medical" : Medical, 
				"electricity" : Electricity
			}), {
				"X-Parse-Application-Id": "b5pEXTYYR7yI6WAKbraPuE6x6ktBWVg8goWK5QY6",
				"X-Parse-REST-API-Key": "DkYbgIV0WLnwIDjjx0HK7jEwu51kWUvYUsTPc3tf",
				"Content-Type": "application/json"
			})
			result = json.loads(connection.getresponse().read())
			print result

			#check for successful save, if not, fail gracefully

			session['counter'] +=1
			resp.message("Thanks!")
			return str(resp)
		else:
			resp.message("Thanks!")
			return str(resp)
	else:
		resp.message("Thank you for your report.")
		return str(resp)	

	#TODO: timeout for sessions




'''@app.route("/latlng")
def getLatLng():
	if request.method == 'GET':
		barang = None
		if 'barang' in request.args:
			barang = request.args.get('barang')

		if barang:
			url = 'http://maps.googleapis.com/maps/api/geocode/json?address=%s,%s&sensor=false' % (barang, "philippines")
			r = requests.get(url)
			location = json.loads(r.text)['results'][0]['geometry']['location']
			return json.dumps(location)
 		else:
 			return "Barangay not found. Can't parse lat/long"'''

if __name__ == "__main__":
    app.run(debug=True)

 

