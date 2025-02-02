
from loguru import logger
import time

def get_custom_message(message) -> str:
    """Generate a response with a custom message."""
    return {'message': f'Hello, you sent: {message}'}

def stream_data():
    """ Generator to emit data progressively """
    for i in range(5):
        time.sleep(1)
        yield f"Data chunk {i}"
        logger.info(f"Sending data chunk {i}")