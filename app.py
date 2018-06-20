from flask import Flask, request, jsonify
from flask_cors import CORS

import cards

app = Flask(__name__)
CORS(app)

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
