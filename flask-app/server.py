from flask import Flask
from flask import render_template
from flask_socketio import SocketIO
import wikipedia
from collections import *
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET KEY HERE'
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template('index.html')


def message_received(methods=['GET', 'POST']):
    print('message was received!!!')


@socketio.on('check article')
def get_article(query):
    return_article = None
    # if something inputted, use it
    error_msg = ""
    if query:
        search_results = wikipedia.search(query, 1)
        # if search returns results
        if search_results:
            return_article = search_results[0]
            # make sure page is not disambiguation
            try:
                wikipedia.summary(return_article, 1)
                # SUCCESS
            except wikipedia.DisambiguationError:
                error_msg = "Be more specific!"
                return_article = None
        # throw error if search doesn't work
        else:
            error_msg = "Invalid search, try again!"
    # if nothing inputted, choose random article
    else:
        return_article = wikipedia.random()
    print("Found article:", return_article)
    socketio.emit('article return', json.dumps({"error": error_msg, "title": return_article}))


@socketio.on('submit articles')
def start_search(json):
    print('Received my event: ', json)
    socketio.emit('my response', json, callback=message_received)


if __name__ == "__main__":
    socketio.run(app, debug=True)
