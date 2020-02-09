 # /index.py

from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json
from google.protobuf.json_format import MessageToJson
import dbconnect

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# run Flask app
if __name__ == "__main__":
    app.run() 

@app.route('/pay',methods=['GET'])
def pay():
    return "payment successfull..."

@app.route('/processPayment',methods=['GET'])
def processPayment():
    param=request.args.get('myparam1')
    return render_template('paymentInterface.html',p1=param)     

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
                "fulfillmentText":'[[{"type":"printForm"}]]',

                "fulfillmentMessages": [{"simpleResponses": {"simpleResponses": [   {
                "displayText": "provide payment"
        }]}}]
    }
    return jsonify(reply)

def placementData(data): 
    #data = request.get_json(silent=True,force=True)
    #result = data.get("queryResult")
    #parameters = result.get("parameters")
    year=data['queryResult']['parameters']['years']
    #year = parameters.get("year")
    if(year in dbconnect.getYears()):
    #if year == '2019':
        data=str(dbconnect.getPlacementRecord(year))
        
        #data='{"company":"TCS","number":"170"},{"company":"Cognizant","number":"70"},{"company":"Incture","number":"11"}'
        
        reply = {
                    "fulfillmentText":'[[{"type":"placement"}],'+data+"]",

                    "fulfillmentMessages": [{"simpleResponses": {"simpleResponses": [   {
                    "displayText": "loading"
            }]}}]
        }
        return jsonify(reply)

    else:
        data='{"details":"Record not available"}'
        reply = {
                    "fulfillmentText":'[[{"type":"notFound"}],'+data+"]",

                    "fulfillmentMessages": [{"simpleResponses": {"simpleResponses": [   {
                    "displayText": "Record not available"
            }]}}]
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

            return response
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    response = detect_intent_texts(project_id, "unique", message, 'en')   
    #print(fulfillment_text)
    
    response=MessageToJson(response)
    response=json.loads(response) 
    #print(response['queryResult']['intent'])
    #print(response['queryResult']['fulfillmentMessages'][0]['simpleResponses']['simpleResponses'])
    #fulfillment_text1=json.loads(fulfillment_text)
    #if (fulfillment_text1[0]['type']=='placement' or fulfillment_text1[0]['type']=='printForm'):
    #    response_text = { "message":  fulfillment_text1, "type":"custom"}
    #    print(fulfillment_text1[0]['type'])
    #    return jsonify(response_text)
    
    if(len(response['queryResult']['intent'])==0):
        fulfillment_text=response['queryResult']['fulfillmentText']
        response_text = { "message":  fulfillment_text, "type":"default"}
        return jsonify(response_text)
    else:
        if(response['queryResult']['intent']['displayName']=="placement statistics" or response['queryResult']['intent']['displayName']=="print forms"):
            fulfillment_text=response['queryResult']['fulfillmentText']
            fulfillment_text=json.loads(fulfillment_text)
            response_text = { "message":  fulfillment_text, "type":"custom"}
            return jsonify(response_text)  
        else: 
            fulfillment_text=response['queryResult']['fulfillmentText']
            response_text = { "message":  fulfillment_text, "type":"default"}
            return jsonify(response_text)


     
    


