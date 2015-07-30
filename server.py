from flask import Flask, render_template, jsonify, redirect, url_for
from main import getUpdates
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
    if len(update_id_deque) == 2 and delta != 0:
        delta = update_id_deque[1] - update_id_deque[0]
        for _ in rs[-delta:]:
            message_text = _['message']['text']
            if message_text.startswith('/g'):
                return redirect(url_for('google'), message=message_text[3:])
    return jsonify(updates)

@app.route('/google/<message>')
def google(message):
    r = requests.get('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + message)
    return jsonify(r.json())

if __name__ == '__main__':
    app.run(debug=True)
