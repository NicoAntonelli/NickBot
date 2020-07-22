from datetime import datetime
from flask import Flask, render_template, request
from twilio.twiml.messaging_response import MessagingResponse
from . import app
import requests


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name=None):
    return render_template("hello_there.html", name=name, date=datetime.now())


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


# SMS / WhatsApp Bot
@app.route("/api/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if "quote" in incoming_msg:
        # Return a quote
        r = requests.get("https://api.quotable.io/random")
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = "I could not retrieve a quote at this time, sorry."
        msg.body(quote)
        responded = True
    if "cat" in incoming_msg:
        # Return a cat pic
        msg.media("https://cataas.com/cat")
        responded = True
    if not responded:
        if "hello" in incoming_msg:
            msg.body("Hello World, curious human! Ask me about cats or famous quotes!")
        else:
            msg.body("I only know about famous quotes and cats, sorry!")
    return str(resp)
