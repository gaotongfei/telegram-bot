from main import getUpdates, google_api, sendMessage
import json
import collections
import re
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
                print(_['message']['chat']['id'])
                message_text = _['message']['text']
                if message_text.startswith('/g'):
                    global chat_id
                    chat_id = _['message']['chat']['id']
                    google(message_text[3:])
    #return json.dumps(updates)

def google(message):
    google_rs_message = ''
    rs = google_api(message)['responseData']['results']
    for _ in rs:
        google_rs_message += "url:{} \ntitle:{} \ncontent:{}".format(_['url'], _['title'], _['content'])
        #chat_id = '98496186'
        print(chat_id)
        sendMessage(chat_id, google_rs_message)
    #r = requests.get('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + message)
    return json.dumps(google_api_json)

main()
#google('flask')

