from flask import Flask, request, jsonify
import caluclations

app = Flask(__name__)

#api route
@app.route("/api", methods=['GET'])
def home():
    reqDate = str(request.args['date'])
    code, msg, payload = caluclations.getPayload(reqDate=reqDate)
    payloadJSON = {
        "code": code,
        "msg": msg,
        "data": payload
    }
    response = jsonify(payloadJSON)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return(response)

#helper route
@app.route('/')
def default():
    return "App is live. make Api call at /api?date= (YYYY-MM-DD). contact developer for information"

if __name__ == '__main__':
    app.run()