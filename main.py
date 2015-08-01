from helper import getUpdates, google_api, sendMessage
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

def google(message):
    google_rs_message = ''
    rs = google_api(message)['responseData']['results']
    for _ in rs[:1]:
        google_rs_message += "{}\n{}".format(_['url'].encode('utf-8'), _['content'].encode('utf-8'))
        #chat_id = '98496186'
        sendMessage(chat_id, google_rs_message)

while True:
    main()
    print("updating")
    time.sleep(1)

