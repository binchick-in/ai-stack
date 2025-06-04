import os
import json

from google_auth_oauthlib.flow import InstalledAppFlow

oauth_key = os.getenv("GOOGLE_OAUTH_KEY", "")
parsed_oauth_key = json.loads(oauth_key)

SCOPES = ["https://www.googleapis.com/auth/calendar"]  # Replace this with the scope(s) you need.

flow = InstalledAppFlow.from_client_config(parsed_oauth_key, SCOPES)
creds = flow.run_local_server(port=0)
print(creds.to_json())
