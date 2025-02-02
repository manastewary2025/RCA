""" IBM Confidential
    6949XXX 
    © Copyright IBM Corp. 2023 
"""
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os
from service.agentWorkflowService import take_single_action, take_single_action_stream, test_stream
import json
from envLoader.envLoader import load_app_env

app = Flask(__name__)
# cors = CORS(app)
# Fix for DAST scan vulnerability - CORS Misconfiguration
allowed_origins = ['https://ibm-supplychainensemble.com', 'http://localhost:3000']
cors = CORS(app, origins=allowed_origins, supports_credentials=True,
     methods=['GET', 'POST'],  # Limit to required HTTP methods
     allow_headers=['Authorization', 'Content-Type']  # Allow only essential headers
)
app.config['CORS_HEADERS'] = 'Content-Type'
# Fix for IAST and DAST scan vulnerabilities
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Fix for DAST scan vulnerability - Session ID in URL Rewrite
# app.config.update(
#     SESSION_COOKIE_SECURE=True,       # Only send cookies over HTTPS
#     SESSION_COOKIE_HTTPONLY=True,     # Prevent JavaScript access to cookies
#     SESSION_COOKIE_SAMESITE='Lax'     # Restrict cookies to same-site requests (or use 'Strict' if possible)
# )


# sock = Sock(app)
# Fix for DAST scan vulnerability - CSP: Wildcard Directive
@app.after_request
def set_csp_header(response):
    # Set Content Security Policy header
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' https://trusted.com; "
        "style-src 'self' https://styles.com "
        "img-src 'self' https://image.com; "
        "font-src 'self' https://ibm-supplychainensemble.com; "
        "connect-src 'self' https://ibm-supplychainensemble.com wss://ibm-supplychainensemble.com https://genaitemp.s3.amazonaws.com; "
    )

    response.headers.pop('Server', None)
    print('mock: testing after_request')
    
    return response

socketio = SocketIO(app,debug=True,cors_allowed_origins=allowed_origins,manage_session=False)
# socketio = SocketIO(app)


load_app_env()

model_id = os.getenv("document_model_id")
api_key = os.getenv("api_key")
# Fix low vulnerability issue found in SAST scan. Comment the print line
# print('dev model_id '+ model_id + ' api_key '+ api_key)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('chatmessage_stream')
def handle_chat_message(data):
    question = data["question"]
    mock = ""
    if "mock" in data:
        mock = data["mock"]
        print('mock: ' + mock)
    print('received message: ' + question)
    def generate(in_question: str):
        print('input: ' + in_question)
        for chat_response in take_single_action_stream(question):
            response = {
                "statusCode": 200,
                "body": {
                    "question": in_question,
                    "response": chat_response,
                    "mock": mock
                }
            }
            # emit('chatmessage_stream', response)
            # print(chat_response['data'].length)
            emit('chatmessage_stream', json.loads(json.dumps(response, default=str)))
    generate(question)
        


@app.route('/reply', methods=['POST'])
def reply():
    question = request.get_json()["question"]
    print(question)
    # agent = create_sca_agent()
    # chat_response = agent.run(question)
    chat_response = take_single_action(question)
    response = {
        "statusCode": 200,
        "body": {
            "question": question,
            "response": chat_response,
        }
    }
    return jsonify(response)

@app.route('/healthz')
def healthz():
    return "OK", 200

@app.route('/readiness')
def readiness():
    return "Ready", 200