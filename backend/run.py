import sys
import os
from dotenv import load_dotenv

# Get the directory where run.py is located
basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from .env file in the Api directory
load_dotenv(os.path.join(basedir, '.env'))

sys.path.insert(0, basedir)

from app.init import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)