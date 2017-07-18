__author__ = 'zexxonn'

import os
import sys
import json

import requests
from flask import request

from app import webapp
from helpers import SetMenu as MH
from app.finance import ForexPython as FXP
from app import ServerStates  as SS
from DatabaseLayer import DatabaseLayer
from WikiHandler import WikiHandler

UserHelpMessage = "Hello. This is help for current ChatBot.\n\n" \
                  "Button Weather: use it to ask for current weather at you location.\n\n" \
                  "Button Fx Rate: use it to ask for Fx Rate on currency pair on some date.\n" \
                  "You have to provide information in format \"{0} {1}\" or \"{0}\" (for Fx Rate on today date).\n" \
                  "For example \"EURRUB\" or \"EURUSD 2017.07.03\"\n\n" \
                  "If after click on a button you provided incorrect input for ChatBot, " \
                  "then for continuing you have to click on button again.\n\n" \
                  "Also you can type any requests about machine learning, and bot provide you with Wikipedia link if it will find appropriate information.".format(FXP.currencyFormat, FXP.timeFormatForUser)

def locationQuickReply(recipient_id):
    return {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": "Share your location.",
            "quick_replies": [
                {
                    "content_type": "location",
                }
            ]
        }
    }

def simpleText(recipient_id, message_text):
    return {
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    }

class SendActions(object):

    @staticmethod
    def askLocation(senderId):
        sendMessage(senderId, locationQuickReply(senderId))

    @staticmethod
    def sendSimpleText(senderId, textMessage):
        sendMessage(senderId, simpleText(senderId, textMessage))

    @staticmethod
    def sendWeatherInformation(senderId, latitude, longitude):
        sendMessage(senderId, simpleText(senderId, getInfoFromOpenWeatherMap(latitude, longitude)))

class RequestHandler(object):

    @staticmethod
    def handleMessageEvent(messagingEvent):

        senderId    = messagingEvent["sender"]["id"]     # the facebook ID of the person sending you the message
        recipientId = messagingEvent["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
        messageInfo = messagingEvent["message"]

        serverCurrentState = SS.ServerStateId( DatabaseLayer.getServerState(senderId) )
        serverBaseState = SS.ServerStateId( SS.ServerStateId.SERVER_BASE_STATE )

        if serverCurrentState == SS.ServerStateId.SERVER_REQUESTED_USERS_LOCATION:
            if "attachments" in messageInfo:
                for attachment in messageInfo["attachments"]:
                    if ("payload" in attachment) and ("coordinates" in attachment["payload"]):
                        location  = attachment["payload"]["coordinates"]
                        latitude  = location["lat"]
                        longitude = location["long"]
                        DatabaseLayer.saveLocation(senderId, latitude, longitude)
                        SendActions.sendWeatherInformation(senderId, latitude, longitude)
            else:
                SendActions.sendSimpleText(senderId, "Can\'t provide weather information. You had to provide you location coordinates.")

            if not (serverCurrentState == serverBaseState):
                DatabaseLayer.updateServerState(senderId, str(serverBaseState))

        elif "text" in messageInfo and messageInfo["text"]:
            messageText = messageInfo["text"]  # the message's text
            if serverCurrentState == SS.ServerStateId.SERVER_ASKED_USER_FOR_CCY_PAIR:
                DatabaseLayer.saveCurrencyPairRequest(senderId, messageText)
                SendActions.sendSimpleText(senderId, str( FXP.getExchangeRate(messageText) ))
            else:
                resText = WikiHandler.request(messageText)
                SendActions.sendSimpleText(senderId, resText)
                DatabaseLayer.saveSimpleMessage(senderId, messageText)

            if not (serverCurrentState == serverBaseState):
                DatabaseLayer.updateServerState(senderId, str(serverBaseState))

    @staticmethod
    def handlePostbackEvent(messagingEvent):
        senderId     = messagingEvent["sender"]["id"]     # the facebook ID of the person sending you the message
        recipientId  = messagingEvent["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
        payloadValue = messagingEvent["postback"]["payload"]

        serverCurrentState = SS.ServerStateId( DatabaseLayer.getServerState(senderId) )

        if payloadValue == MH.PayloadTypes.HELP:
            SendActions.sendSimpleText(senderId, UserHelpMessage)

        elif payloadValue == MH.PayloadTypes.WEATHER:
            SendActions.askLocation(senderId)
            state = SS.ServerStateId( SS.ServerStateId.SERVER_REQUESTED_USERS_LOCATION )
            DatabaseLayer.updateServerState(senderId, str(state))

        elif payloadValue == MH.PayloadTypes.EXCHANGE_RATE:
            SendActions.sendSimpleText(senderId, "provide info as \"{0} {1}\" or \"{0}\"".format(FXP.currencyFormat, FXP.timeFormatForUser))
            state = SS.ServerStateId( SS.ServerStateId.SERVER_ASKED_USER_FOR_CCY_PAIR )
            DatabaseLayer.updateServerState(senderId, str(state))

def getInfoFromOpenWeatherMap(latitude, longitude):

    apiKey = webapp.config['OPEN_WEATHER_MAP_API_KEY'] #os.environ.get('OPEN_WEATHER_MAP_API_KEY')
    url = 'http://api.openweathermap.org/data/2.5/weather?'
    headers = { "Content-Type": "application/json" }
    params = {
        "lat"  : latitude,
        "lon"  : longitude,
        "appid": apiKey,
        "units": "metric",
        "lang" : "rus"
    }

    resp = requests.get(url, params=params, headers=headers)
    data = resp.json()

    description = data['weather'][0]['description'].title()
    icon        = data['weather'][0]['icon']
    weather     = data["main"]
    place       = data["name"]

    textResult = ": {}\n" \
            .join(["Description" , "Temperature", "Pressure",  "Humidity: {}"]) \
            .format("{}, {}".format(place, description), weather['temp'], weather['pressure'], weather['humidity'])

    return textResult

def sendMessage(recipientId, message):

    log("sending message to {recipient}: {text}".format(recipient=recipientId, text=str(message)))

    params = {
        "access_token": webapp.config['FB_PAGE_ACCESS_TOKEN'] #os.environ["FB_PAGE_ACCESS_TOKEN"]
    }

    headers = {
        "Content-Type": "application/json"
    }

    data = json.dumps(message)
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages",
            params=params, headers=headers, data=data)

    if resp.status_code != 200:
        log(resp.status_code)
        log(resp.text)

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

@webapp.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == webapp.config["FB_VERIFY_TOKEN"]: #os.environ["FB_VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200

@webapp.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log("================================================================")
    log(data)  # for testing
    log("================================================================")

    if data["object"] == "page":

        for entry in data["entry"]:

            for messagingEvent in entry["messaging"]:

                # MESSAGE event handling
                if messagingEvent.get("message"):  # someone sent us a message
                    RequestHandler.handleMessageEvent(messagingEvent)

                # POSTBACK event handling
                if messagingEvent.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    RequestHandler.handlePostbackEvent(messagingEvent)

                # DELIVERY event handling
                if messagingEvent.get("delivery"):  # delivery confirmation
                    pass

                # OPTIN event handling
                if messagingEvent.get("optin"):  # optin confirmation
                    pass

    return "ok", 200

