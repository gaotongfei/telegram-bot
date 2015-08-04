import requests
import os

'''
:param tg_bot_toKen: telegram bot 的 api token，在此处
  https://core.telegram.org/bots/api#authorizing-your-bot
  阅读如何获得token

:param youdao_keyfrom: 有道词典api key，可在此处申请
  http://fanyi.youdao.com/openapi?path=data-mode

:param youdao_key: 同上

:param nasa_api_key: https://api.nasa.gov/index.html#apply-for-an-api-key 此处申请

'''

# 你可以通过在命令行中输入export tg_bot_token=your-telegram-bot-token来配置你的token，
# 同理youdao_keyfrom，youdao_key，nasa_api_key也可以这么配置，如果你不喜欢这种方式，可以直接改为明文。

tg_bot_token = os.environ.get('tg_bot_token')
youdao_keyfrom = os.environ.get('youdao_keyfrom')
youdao_key = os.environ.get('youdao_key')
nasa_api_key = os.environ.get('nasa_api_key')

'''
:param url_prefix: https://core.telegram.org/bots/api#making-requests 阅读此处
'''
url_prefix = 'https://api.telegram.org/bot' + tg_bot_token + '/'


def getMe():
    '''
    :func getMe(): 用来验证token是否有效
    '''
    url = url_prefix + 'getMe'
    r = requests.get(url)
    print(r.status_code)
    print(r.text)


def sendMessage(chat_id, text):
    '''
    :func sendMessage(chat_id, text): https://core.telegram.org/bots/api#sendmessage 阅读此处
    返回json
    :param chat_id: telegram的id名，注意此id名是数字形式
    '''
    url = url_prefix + 'sendMessage?chat_id={0}&text={1}'.format(chat_id, text)
    r = requests.get(url)
    return r.json()


def getUpdates():
    '''
    :func getUpdates: https://core.telegram.org/bots/api#getupdates 阅读此处
    返回json
    '''
    url = url_prefix + 'getUpdates'
    r = requests.get(url)
    return r.json()


def google_api(message):
    '''
    :func google_api: https://developers.google.com/web-search/docs/
    返回json
    '''
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + message
    r = requests.get(url)
    return r.json()


def youdao_api(message):
    '''
    :func youdao_api: 和上面类似，调用api，返回json
    '''
    url = 'http://fanyi.youdao.com/openapi.do?keyfrom={}&key={}&type=data&doctype=json&version=1.1&q={}'\
          .format(youdao_keyfrom, youdao_key, message.encode('utf-8'))
    r = requests.get(url)
    return r.json()


def nasa_api(message):
    '''
    同上
    '''
    if message is None:
        url = 'https://api.nasa.gov/planetary/apod?concept_tags=True&api_key={}'\
              .format(nasa_api_key)
    else:
        url = 'https://api.nasa.gov/planetary/apod?concept_tags=True&api_key={}&date={}'\
              .format(nasa_api_key, message)
    r = requests.get(url)
    return r.json()
