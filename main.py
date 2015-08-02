# coding=utf-8
from helper import getUpdates, google_api, sendMessage, youdao_api
import json
import collections
import time
import requests

update_id_deque = collections.deque(maxlen=2)
chat_id = 0

def main():
    updates = getUpdates()
    rs = updates["result"]
    global update_id_deque
    update_id_deque.append(rs[-1]['update_id'])

    if len(update_id_deque) == 1:
        print("len is 1")
        pass
    if len(update_id_deque) == 2:
        print("len is 2")
        delta = update_id_deque[1] - update_id_deque[0]
        if delta != 0:
            print("delta is not 0")
            for _ in rs[-delta:]:
                message_text = _['message']['text']
                if message_text.startswith('/g'):
                    global chat_id
                    chat_id = _['message']['chat']['id']
                    google(message_text[3:])
                    update_id_deque.append(rs[-1]['update_id'])
                    #print("1 ", update_id_deque[0],"2 ", update_id_deque[1])
                elif message_text.startswith('/trans'):
                    chat_id = _['message']['chat']['id']
                    translate(message_text[7:])
                    update_id_deque.append(rs[-1]['update_id'])

def google(message):
    google_rs_message = ''
    rs = google_api(message)['responseData']['results']
    for _ in rs[:1]:
        google_rs_message += "{}\n{}".format(_['url'].encode('utf-8'), _['content'].encode('utf-8'))
        #chat_id = '98496186'
        sendMessage(chat_id, str(google_rs_message))

def translate(message):
    rs = youdao_api(message)
    if rs['errorCode'] == 0:
        if 'basic' in rs:
            translate_rs_message = "{}\n{}".format(rs['translation'][0].encode('utf-8'), rs['basic']['explains'][0].encode('utf-8'))
        else:
            translate_rs_message = "{}".format(rs['translation'][0].encode('utf-8'))
        sendMessage(chat_id, str(translate_rs_message))
    elif rs['errorCode'] == 20:
        sendMessage(chat_id, u"要翻译的文本过长")
    elif rs['errorCode'] == 30:
        sendMessage(chat_id, u"无法进行有效的翻译")
    elif rs['errorCode'] == 40:
        sendMessage(chat_id, u"不支持的语言类型")
    elif rs['errorCode'] == 50:
        sendMessage(chat_id, u"无效的key")
    elif rs['errorCode'] == 60:
        sendMessage(chat_id, u"无词典结果，仅在获取词典结果生效")

while True:
    main()
    print("updating")
    time.sleep(0.5)
