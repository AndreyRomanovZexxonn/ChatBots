__author__ = 'zexxonn'

import json
import requests
import os

'''
curl -X POST -H "Content-Type: application/json" -d '{
  "setting_type":"greeting",
  "greeting":{
    "text":"Hi {{user_first_name}}, welcome to this bot."
  }
}' "https://graph.facebook.com/v2.6/me/thread_settings?access_token=PAGE_ACCESS_TOKEN"
'''
def main():

    params  = { "access_token": os.environ["FB_PAGE_ACCESS_TOKEN"] }
    headers = { "Content-Type": "application/json" }

    message = {
        "setting_type":"greeting",
        "greeting": {
            "text":"Hi {{user_first_name}}, welcome to this bot."
        }
    }

    data = json.dumps(message)
    res = requests.post("https://graph.facebook.com/v2.6/me/thread_settings",
    				params=params, headers=headers, data=data)

    print "Response:"
    print res.content

if __name__ == "__main__":
    main()
