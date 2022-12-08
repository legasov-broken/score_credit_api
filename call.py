
import json
import numpy
from credit_score import credit_score
from score_all_users import score_users
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/v1/score_card', methods=['POST'])
def api():
    data = json.loads(request.data)
    out = score_users(data)
    return jsonify(out)
app.run()
