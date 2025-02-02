import os
from dotenv import load_dotenv

def load_app_env():
    """Load environment variables from a .env file."""
    
    flask_env = os.getenv("FLASK_ENV")

    #print('flask_env '+ flask_env)
    if flask_env == 'development':
        load_dotenv(dotenv_path='/mnt/secrets-store/sca-genai-assistant-api')
        model_id = os.getenv("document_model_id")
        api_key = os.getenv("api_key")
        # Fix low vulnerability issue found in SAST scan. Comment the print line
        # print('dev model_id '+ model_id + ' api_key '+ api_key)
    else:
        load_dotenv()