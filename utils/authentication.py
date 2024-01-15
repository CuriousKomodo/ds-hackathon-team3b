import os

from dotenv import load_dotenv
import base64

load_dotenv()
api_token = os.getenv('API_TOKEN')
email = os.getenv('EMAIL')

def authenticate(email, api_token):
    auth_string = f"{email}:{api_token}"
    encoded_auth_string = base64.b64encode(auth_string.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_auth_string}",
        "Content-Type": "application/json"
    }
    return headers
