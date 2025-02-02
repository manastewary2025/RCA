from flask import Flask, jsonify
from flask_socketio import SocketIO
from loguru import logger
import sys

app = Flask(__name__)
app.config.from_object('app.config.Config')  # Load configuration
socketio = SocketIO()

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    socketio.init_app(app)
    
    # Loguru setup
    logger.remove()  # Remove the default logger
    logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")

    logger.info("Flask app initialized")

    from app.routes import api_routes
    app.register_blueprint(api_routes)
    
    @app.errorhandler(404)
    def not_found_error(error):
        logger.error(f"404 Error: {error}")
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"500 Error: {error}")
        return jsonify({'error': 'Internal server error'}), 500

    from app.sockets import handle_message  # Import Socket.IO event handlers

    return app

