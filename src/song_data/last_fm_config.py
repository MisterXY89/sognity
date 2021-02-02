
import os
from os.path import join, dirname
from dotenv import load_dotenv

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)
LAST_FM_API_KEY = os.getenv('LAST_FM_API_KEY')
LAST_FM_SHARED_SECRET = os.getenv('LAST_FM_SHARED_SECRET')
