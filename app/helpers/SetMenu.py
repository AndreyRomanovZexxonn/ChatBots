__author__ = 'zexxonn'

import requests
import json
import os

class PayloadTypes(object):
    HELP = "DEV_PAYLOAD_HELP"
    WEATHER = "DEV_PAYLOAD_WEATHER"
    EXCHANGE_RATE = "DEV_PAYLOAD_EXCHANGE_RATE"
    GET_STARTED_BUTTON = "DEV_PAYLOAD_GET_STARTED"

def addGetStartedButton():
    params  = {"access_token": os.environ["FB_PAGE_ACCESS_TOKEN"]}
    headers = {"Content-Type": "application/json"}
    message = {"get_started": {"payload": PayloadTypes.GET_STARTED_BUTTON}}
    data = json.dumps(message)
    res = requests.delete("https://graph.facebook.com/v2.6/me/messenger_profile",
    				params=params, headers=headers, data=data)
    print "Response:"
    print res.content

def setGreetingMessage():
    params  = {"access_token": os.environ["FB_PAGE_ACCESS_TOKEN"]}
    headers = {"Content-Type": "application/json"}
    message = {
        "greeting":[
        {
            "locale":"default",
            "text":"Hello!"
        }]
    }

    data = json.dumps(message)
    res = requests.delete("https://graph.facebook.com/v2.6/me/messenger_profile",
    				params=params, headers=headers, data=data)

    print "Response:"
    print res.content


def deleteMenu():
    params  = {"access_token": os.environ["FB_PAGE_ACCESS_TOKEN"]}
    headers = {"Content-Type": "application/json"}

    message = {"fields": ["persistent_menu"]}

    data = json.dumps(message)
    res = requests.delete("https://graph.facebook.com/v2.6/me/messenger_profile",
    				params=params, headers=headers, data=data)

    print "Response:"
    print res.content

def addPersistentMenu():
    params  = {"access_token": os.environ["FB_PAGE_ACCESS_TOKEN"]}
    headers = {"Content-Type": "application/json"}

    message = {
        "persistent_menu":[
        {
            "locale":"default",
            "composer_input_disabled":True,
            "call_to_actions": [
            {
                "title": "Help",
                "type": "postback",
                "payload": PayloadTypes.HELP
            },
            {
                "title": "Weather",
                "type": "postback",
                "payload": PayloadTypes.WEATHER
            },
            {
                "title": "Fx Rate",
                "type": "postback",
                "payload": PayloadTypes.EXCHANGE_RATE
            }]
        },
        {
            "locale":"default",
            "composer_input_disabled": False
        }
]
    }

    data = json.dumps(message)
    res = requests.post("https://graph.facebook.com/v2.6/me/messenger_profile",
    				params=params, headers=headers, data=data)

    print "Response:"
    print res.content


def addMenu():
    params  = {"access_token": os.environ["FB_PAGE_ACCESS_TOKEN"]}
    headers = {"Content-Type": "application/json"}

    message = {
          "setting_type": "call_to_actions",
          "thread_state": "existing_thread",
          "call_to_actions": [
            {
                "title": "Help",
                "type": "postback",
                "payload": PayloadTypes.HELP
            },
            {
                "title": "Weather",
                "type": "postback",
                "payload": PayloadTypes.WEATHER
            },
            {
                "title": "Fx Rate",
                "type": "postback",
                "payload": PayloadTypes.EXCHANGE_RATE
            }
          ]}


    data = json.dumps(message)
    res = requests.post("https://graph.facebook.com/v2.6/me/thread_settings",
    				params=params, headers=headers, data=data)

    print "Response:"
    print res.content

if __name__ == "__main__":

    #addGetStartedButton()
    #setGreetingMessage()
    #addPersistentMenu()
    addMenu()
