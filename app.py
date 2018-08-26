from flask import Flask, request, jsonify
from flask_cors import CORS

import cards

app = Flask(__name__)
CORS(app)

# add a new card
@app.route('/cards', methods = ['POST'])
def add_new_card():
    data = request.get_json()
    cards.add_card(
        data['front'],
        data['back'],
    )
    return ""

@app.route('/review', methods = ['GET'])
def get_review():
    return jsonify(cards.get_review())

@app.route('/do_rep', methods = ['POST'])
def do_rep():
    data = request.get_json()
    uuid, ease = data['uuid'], data['ease']
    cards.do_rep(uuid, ease)
    return ""
