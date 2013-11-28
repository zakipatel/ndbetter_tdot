from twilio.rest import TwilioRestClient
import twilio.twiml

from flask import Flask
from flask import request

app = Flask(__name__)
 
@app.route("/")
def hello():
    return "Hello World!"

@app.route("/receive-sms", methods=['GET', 'POST'])
def reply():
	print "Received Message"
	if request.form['Body'] 
	resp = twilio.twiml.Response()
	resp.message("<Next Question>")
	return str(resp)

else:

 
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

