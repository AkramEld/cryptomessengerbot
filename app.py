import os, sys
import requests
from flask import Flask, request
from pymessenger import Bot
app = Flask(__name__)

#stores requests for btc price in different currencies using api
x=requests.get('https://api.coindesk.com/v1/bpi/currentprice/CAD.json')
y=requests.get('https://api.coindesk.com/v1/bpi/currentprice/GBP.json')

PAGE_ACCESS_TOKEN = "EAAWMoLgKtqgBAPZA0aRc3iLdux0TmlkZCLPKaQo3ZA4E6ZAkOliIjxCuk9R4bWcnqXvS24tUYveM8UySZAUlqHUvvYeiYsaYNRZCPQiZBu8WSYlCsTBDbuRyBrpVkMQEBwAtiPxwEfLZAKHJwk14SvJdGcou3S3ml05DeZAFtwhX8KyJmyGngLNhh"
bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():

    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:


                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):

                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']



                    else:
                        messaging_text = 'no text'

                        #ouputs price given input
                response = messaging_text
                if response=='btc,usd':
                    bot.send_text_message(sender_id, 'The current price of bitcoin in U.S Dollars is: $'+ x.json()['bpi']['USD']['rate'])
                elif response=='btc,gbp':
                    bot.send_text_message(sender_id, 'The current price of bitcoin in British Pounds is: £'+ y.json()['bpi']['GBP']['rate'])

                elif response=='btc,cad':
                    bot.send_text_message(sender_id, 'The current price of bitcoin in Canadian Dollars is: $'+ x.json()['bpi']['CAD']['rate'])

                else:
                    bot.send_text_message(sender_id, "Invalid Entry, Please Try again!")



    return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug = True, port = 80)
