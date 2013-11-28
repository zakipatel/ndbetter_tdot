from twilio.rest import TwilioRestClient
import twilio.twiml

from flask import Flask, request, session

app = Flask(__name__)

app.secret_key = 'testing'
 
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/receive-sms", methods=['GET', 'POST'])
def reply():
	print "Received Message"

	counter = session.get('counter', 0)
	
	if request.form['Body']:
		resp = twilio.twiml.Response()
		if counter == 0: 
			resp.message("What is your Barangay? (e.g. Cabungaan)")
			help_request = {}
			help_request['number'] = request.form['From']
			help_request['bar'] = request.form['Body']
			# TODO: check whether it's a valid Barangay
			session['help_request'] = help_request
			counter += 1
			session['counter'] = counter
			return str(resp)
		elif counter == 1:
			resp.message("Do you need: 1)Water, 2)Food, 3)Medical, 4)Shelter, 5)Electricity, 6)Others (options will follow)")
			counter += 1
			session['counter'] = counter
			return str(resp)
		elif counter == 2:
			help_request = session.get('help_request')
			help_request['type'] = request.form['Body']
			# TODO: handle invalid option
			session['help_request'] = help_request
			resp.message("Thanks!")
			return str(resp)
	else:
		pass
 
if __name__ == "__main__":
    app.run(debug=True)

 
''' Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "ACf22848a320c719539086936ae83b210c"
auth_token  = "bb09e98f22a93cd446056680610e5078"
client = TwilioRestClient(account_sid, auth_token)
 
message = client.sms.messages.create(body="Hi Justine! Do you need help?",
    to="+14167104589",    # Replace with your phone number
    from_="+16132090604") # Replace with your Twilio number
print message.sid'''




#TO DO: recieve inbound sms
#TO DO: Build the flow
#TO DO: Decide what to store

