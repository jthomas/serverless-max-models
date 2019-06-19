from maxfw.core import MAXApp
from api import ModelPredictAPI
from config import API_TITLE, API_DESC, API_VERSION
import json
import base64
from flask import Flask, request, Response

max_app = MAXApp(API_TITLE, API_DESC, API_VERSION)
max_app.add_api(ModelPredictAPI, '/predict')

# Use flask test client to simulate HTTP requests for the prediction APIs
# HTTP request data will come from action invocation parameters, neat huh? :)
test_client = max_app.app.test_client()
app = Flask(__name__)

# This implements the Docker runtime API used by Apache OpenWhisk
# https://github.com/apache/incubator-openwhisk/blob/master/docs/actions-docker.md
# /init is a no-op as everything is provided in the image.
@app.route("/init", methods=['POST'])
def init():
    return ''

# Action invocation requests will be received as the `value` parameter in request body.
# Web Actions provide HTTP request parameters as `__ow_headers` & `__ow_body` parameters.
@app.route("/run", methods=['POST'])
def run():
    body = request.json
    form_body = body['value']['__ow_body']
    headers = body['value']['__ow_headers']

    # binary image content provided as base64 strings
    content = base64.b64decode(form_body)

    # send fake HTTP request to prediction API with invocation data
    r = test_client.post('/model/predict', data=content, headers=headers)
    r_headers = dict((x, y) for x, y in r.headers)

    # binary data must be encoded as base64 string to return in JSON response
    is_image = r_headers['Content-Type'].startswith('image')
    r_data = base64.b64encode(r.data) if is_image else r.data
    body = r_data.decode("utf-8")

    response = {'headers': r_headers, 'status': r.status_code, 'body': body }
    print (r.status)
    return Response(json.dumps(response), status=200, mimetype='application/json')

app.run(host='0.0.0.0', port=8080)
