# coding=utf-8
from helper import getUpdates, google_api, sendMessage, youdao_api, nasa_api
import collections
import time

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

                elif message_text.startswith('/trans'):
                    chat_id = _['message']['chat']['id']
                    translate(message_text[7:])
                    update_id_deque.append(rs[-1]['update_id'])

                elif message_text.startswith('/nasa'):
                    chat_id = _['message']['chat']['id']
                    if len(message_text.strip()) == 5:
                        nasa_pic(message=None)
                    else:
                        nasa_pic(message_text[6:])
                    update_id_deque.append(rs[-1]['update_id'])
                elif message_text.startswith('/help'):
                    chat_id = _['message']['chat']['id']
                    help_message = str("命令列表：\n \
                            * /g <关键词> google搜索 \n \
                            * /trans <翻译的内容> \n \
                            * /nasa [日期(若不填，默认为美国时间当日, 格式如2015-08-03)]")
                    sendMessage(chat_id, help_message)


def google(message):
    google_rs_message = ''
    rs = google_api(message)['responseData']['results']
    for _ in rs[:1]:
        google_rs_message += "{}\n{}".format(_['url'].encode('utf-8'), _['content'].encode('utf-8'))
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


def nasa_pic(message):
    rs = nasa_api(message)
    if 'error' in rs:
        sendMessage(chat_id, rs['error'])
    else:
        nasa_pic_and_explanation = "{}".format(rs['url'])
        sendMessage(chat_id, nasa_pic_and_explanation)

while True:
    main()
    print("updating")
    time.sleep(2)
