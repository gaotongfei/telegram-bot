import requests
import os

tg_bot_token = os.environ.get('tg_bot_token')
url_prefix = 'https://api.telegram.org/bot' + tg_bot_token + '/'

def getMe():
    url = url_prefix + 'getMe'
    r = requests.get(url)
    print(r.status_code)
    print(r.text)

def sendMessage(chat_id, text):
    url = url_prefix + 'sendMessage?chat_id={0}&text={1}'.format(chat_id, text)
    r = requests.get(url)
    return r.json()

def getUpdates():
    url = url_prefix + 'getUpdates'
    r = requests.get(url)
    return r.json()

def google_api(message):
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + message
    r = requests.get(url)
    return r.json()
