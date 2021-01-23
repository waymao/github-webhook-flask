########################################################################
#    main.py
#   
#   accepts webhooks from github, checkes the message integrity,
#   and does the action in ./action.py
#   
#   2021.1.23, wm
#
########################################################################


from flask import Flask, request, jsonify
import os

import hmac
from hashlib import sha256

from action import actions, event, secret, ref

app = Flask(__name__)
secret = os.getenv("SECRET")
ref = os.getenv("GITHUB_REF")

@app.route("/update/", methods = ['POST'])
def update():
    # request type
    if (request.method != 'POST'):
        response = jsonify({"error": "Wrong HTTP method"})
        response.status_code = 400
        return response

    # processing signature
    signature_raw = request.headers.get("X-Hub-Signature-256")
    signature_parts = signature_raw.split("=")
    if (signature_parts[0].lower() != "sha256" or len(signature_parts) != 2):
        response = jsonify({"error": "Wrong sha256 signature format"})
        response.status_code = 400
        return response
    signature = signature_parts[1]

    # begin checking integrity
    req_body = request.data
    h = hmac.new(secret, req_body, sha256)
    if (signature != h.hexdigest()):
        response = jsonify({"error": "Signature check failed"})
        response.status_code = 403
        return response
    
    # event type
    event_type = request.headers.get("X-GitHub-Event")
    if (event_type != event):
        response = jsonify({"result": "success", "updated": "none"})
        response.status_code = 200
        return response

    # begin check if is the branch we want and do the action
    obj = request.json()
    if (obj['ref'] and obj['ref'] == ref):
        try:
            for action in actions:
                action()
            response = jsonify({"result": "success", "updated": "yes"})
            response.status_code = 200
            return response
        except:
            response = jsonify({"error": "action run failed"})
            response.status_code = 500
            return response

    else:
        response = jsonify({"result": "success"})
        response.status_code = 200
        return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
