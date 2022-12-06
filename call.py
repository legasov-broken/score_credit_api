
import json
import numpy
from credit_score import credit_score
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/v1/test', methods=['GET','POST'])
def api():
    data = json.loads(request.data)
    x = numpy.array(data["input"])
    pred = credit_score(x)
    return jsonify(pred)
app.run()
