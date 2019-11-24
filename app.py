from flask import Flask, render_template, request, json, redirect
import africastalking
import firebase_admin
from firebase_admin import db, credentials

# Initialize Firebase Admin
cred = credentials.Certificate("./service.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://devfestaddis-c5f0d.firebaseio.com/'
})

# Create a reference to the Database

root = db.reference()

# Authenticate with africastalking

username = "sandbox"
api_key = "c7b3cf6e957bfb978ca8c6cb15665a83f06f6c82a534ad81dbf726acf2f77469"
africastalking.initialize(username, api_key)

# initialize SMS service

sms = africastalking.SMS

# create flask app

app = Flask(__name__)

# create routes to views


@app.route("/", methods=["GET", "POST"])
def main():

    return render_template('index.html')


@app.route("/showSMSPage", methods=["GET", "POST"])
def showSendSMS():
    return render_template('sms.html')

# route SMS sending route
# request sent via AJAX


@app.route("/sendSMS", methods=["POST"])
def sendSMS():

    # Reading values from the UI

    if request.method == "POST":
        _sms_message = request.form["smsMessage"]
        _phone_number = request.form["phoneNumber"]

        response = sms.send(_sms_message, [str(_phone_number)])

        # Save sent messages

        message_saving = root.child("messages").set(response)

        print(response)

        if _sms_message and _phone_number:
            return json.dumps({'html': '<span>All fields are good. Sending SMS and saving to Firebase</span>'})
        else:
            return json.dumps({'html': '<span>Please fill the required fields</span>'})

        return redirect(request.url)


if __name__ == "__main__":
    app.run(debug=True)
