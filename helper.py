import requests
import os

tg_bot_token = os.environ.get('tg_bot_token')
youdao_keyfrom = os.environ.get('youdao_keyfrom')
youdao_key = os.environ.get('youdao_key')
nasa_api_key = os.environ.get('nasa_api_key')

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


def youdao_api(message):
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom={}&key={}&type=data&doctype=json&version=1.1&q={}'\
          .format(youdao_keyfrom, youdao_key, message.encode('utf-8'))
    r = requests.get(url)
    return r.json()


def nasa_api(message):
    if message is None:
        url = 'https://api.nasa.gov/planetary/apod?concept_tags=True&api_key={}'\
              .format(nasa_api_key)
    else:
        url = 'https://api.nasa.gov/planetary/apod?concept_tags=True&api_key={}&date={}'\
              .format(nasa_api_key, message)
    r = requests.get(url)
    return r.json()
