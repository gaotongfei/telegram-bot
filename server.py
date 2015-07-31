from flask import Flask, render_template, jsonify, redirect, url_for, request
from main import getUpdates, google_api, sendMessage
import json
import collections
import re
import requests

app = Flask(__name__)
update_id_deque = collections.deque(maxlen=2)

@app.route('/')
def index():
    updates = getUpdates()
    rs = updates["result"]
    global update_id_deque
    update_id_deque.append(rs[-1]['update_id'])

    if len(update_id_deque) == 1:
        pass
    if len(update_id_deque) == 2:
        delta = update_id_deque[1] - update_id_deque[0]
        if delta != 0:
            for _ in rs[-delta:]:
                print(_['message']['chat']['id'])
                message_text = _['message']['text']
                if message_text.startswith('/g'):
                    return redirect(url_for('google', message=message_text[3:], chat_id=_['message']['chat']['id']))
    return jsonify(updates)

@app.route('/google/<message>')
def google(message):
    google_api_json = google_api(message)
    google_rs_message = ''
    rs = google_api_json['responseData']['results']
    for _ in rs:
        google_rs_message += "url:{} \ntitle:{} \ncontent:{}".format(_['url'], _['title'], _['content'])
        sendMessage(request.args.get('chat_id'), google_rs_message)

    print(google_rs_message)
    #r = requests.get('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + message)
    return jsonify(google_api_json)

if __name__ == '__main__':
    app.run(debug=True)
