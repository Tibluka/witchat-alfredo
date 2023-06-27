from flask import Flask, request
from flask_cors import CORS
from services import messages

app = Flask(__name__)
CORS(app)

@app.route('/messages/save', methods = ['POST'])
def send():
    try:
        API_KEY = request.headers["Authorization"]
        message = request.json['message']
        chatGptResponse = messages.sendMessage(message, API_KEY)
        res = {}
        res['message'] = chatGptResponse
        return res, 200
    except:
        e = {}
        e['error'] = e['message']
        return e, 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug = True, port = 6000)