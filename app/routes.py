from flask import Flask,jsonify, render_template,Blueprint
from app.services.generator import get_custom_message
from flask_socketio import SocketIO, emit
from loguru import logger

api_routes = Blueprint('api', __name__)

@api_routes.route('/')
def index():
    try:
        logger.info("Index API called")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in Index API: {e}")
        return jsonify({'error': str(e)}), 500

@api_routes.route('/custom/<string:message>', methods=['GET'])
def custom_message(message):
    try:
        logger.info("Custom Message API called")
        return get_custom_message(message)
    except Exception as e:
        logger.error(f"Custom Message  in Index API: {e}")
        return jsonify({'error': str(e)}), 500
    

