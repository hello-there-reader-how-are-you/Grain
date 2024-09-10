import os
#https://console.cloud.google.com/apis/dashboard?project=gifted-course-430810-q2
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

if not os.path.exists("./models"):
    os.makedirs("./models")
    print("Folder 'models' created.")

    with open(os.path.join("./models", "put_models_here.txt"), 'w') as file:
        file.write("Please put your models in this folder.")

if not os.path.exists("./ignore_me"):
    os.makedirs("./ignore_me")
    print("Folder 'ignore_me' created.")

    with open(os.path.join("ignore_me", "this_is_where_creds_go.txt"), 'w') as file:
        file.write("No touching")

if not os.path.exists("holdover.json"):
    with open("holdover.json", 'w') as file:
        file.write('{"volume":30}')

print("created folders & files")


#break
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/gmail.readonly"]

cred_file = "./ignore_me/credentials.json"
token_file = "./ignore_me/token.json"

creds = None

if os.path.exists(token_file):
    creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(cred_file, SCOPES)
        creds = flow.run_local_server(port=0)
    with open(token_file, "w") as token:
        token.write(creds.to_json())

print("setup completed")


#CMAKE_ARGS="-DGGML_METAL=on" pip install --force-reinstall --upgrade --no-cache-dir  -v "llama_cpp_python==0.2.83"    