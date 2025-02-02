from flask_socketio import emit
from app import socketio
from app.services.generator import get_custom_message, stream_data
from loguru import logger


@socketio.on('message')
def handle_message(message):
    logger.info("Client requested data stream.")
    try:
        for chunk in stream_data():
            emit('response', {'message': chunk})
    except Exception as e:
        logger.error(f"Error streaming data: {e}")
        emit('error', {'error': 'Error occurred during streaming.'})
    # try:
    #     print(f"Received message: {message}")
    #     logger.info(f"Received message: {message}")
    #     emit('response', get_custom_message(message))
    # except Exception as e:
    #     print(f"Error processing message: {e}")
    #     logger.info(f"Error processing message: {e}")
    #     emit('response', {'error': 'An error occurred while processing your message'})
