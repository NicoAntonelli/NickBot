from flask import request
from twilio.twiml.messaging_response import MessagingResponse
import requests

# SMS/WhatsApp Bot - Request Analysis and Response
def bot_logic():
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
    if "meme" in incoming_msg:
        # Return a meme pic
        r = requests.get("https://some-random-api.ml/meme")
        if r.status_code == 200:
            data = r.json()
            meme = data["image"]
        msg.media(meme)
        responded = True
    if not responded:
        if "hello" in incoming_msg:
            msg.body("Hello World, curious human! Ask me about memes or famous quotes!")
        else:
            msg.body("I only know about famous quotes and memes, sorry!")
    return str(resp)
