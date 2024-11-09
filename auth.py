import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly",  # calendar api
          "https://www.googleapis.com/auth/drive.metadata.readonly",  # drive api
          "https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/drive.readonly",
          "https://www.googleapis.com/auth/drive.file"
        ]

def authenticate() -> Credentials: 
    """Authenticate this device with the google cloud api

    Returns:
        Credentials: the credentials obtained from authentication
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    cur_path = os.path.dirname(__file__)
    if os.path.exists(f"{cur_path}{os.path.sep}token.json"):
        creds = Credentials.from_authorized_user_file(f"{cur_path}{os.path.sep}token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                f"{cur_path}{os.path.sep}credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(f"{cur_path}{os.path.sep}token.json", "w") as token:
            token.write(creds.to_json())
    return creds