 # /index.py

from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# run Flask app
if __name__ == "__main__":
    app.run() 

@app.route('/webhook', methods=['POST'])
def webhook(): 
    data = request.get_json(silent=True,force=True)
    reply='';
    if(data['queryResult']['intent']['displayName']=='placement statistics'):
        reply=placementData(data);
        return reply;
    elif(data['queryResult']['intent']['displayName']=='print forms'):
        reply=printForm(data);
        return reply;


def printForm(data):

    reply = {
        "fulfillmentText": "provide payment",
    }
    return jsonify(reply)

def placementData(data): 
    #data = request.get_json(silent=True,force=True)
    #result = data.get("queryResult")
    #parameters = result.get("parameters")
    year=data['queryResult']['parameters']['year']
    #year = parameters.get("year")
    if year == '2019':
        reply = {
            "fulfillmentText": "CTS 75 CTS 170",
        }
        return jsonify(reply)

    else:
        reply = {
            "fulfillmentText": "Record not Available",
        }
        return jsonify(reply)

def detect_intent_texts(project_id, session_id, text, language_code):
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)

        if text:
            text_input = dialogflow.types.TextInput(
                text=text, language_code=language_code)
            query_input = dialogflow.types.QueryInput(text=text_input)
            response = session_client.detect_intent(
                session=session, query_input=query_input)

            return response.query_result.fulfillment_text
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    #if (fulfillment_text=='provide payment'):
    #    response_text = { "message":  "ok" }
    #    return jsonify(response_text)
    
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)

