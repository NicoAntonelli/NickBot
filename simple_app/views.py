from datetime import datetime
from flask import Flask, render_template


from . import app
from simple_app.bot_logic import bot_logic


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")


# Hello Message (Not a Bot)
@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name=None):
    return render_template("hello_there.html", name=name, date=datetime.now())


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


@app.route("/api/bot_info")
def bot_info():
    return render_template("bot.html")


# SMS / WhatsApp Bot
@app.route("/api/bot", methods=["POST"])
def bot():
    return bot_logic()
