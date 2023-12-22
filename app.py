from flask import Flask

app = Flask(__name__)

@app.route("/")
def social_network_activity():
    # TODO: your code here
    json_response = {}
    return json_response
