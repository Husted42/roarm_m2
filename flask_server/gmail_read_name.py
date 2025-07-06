import os.path
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Locate credentials file
# TODO : Global variable - Update the path to your credentials file
credential_file = f"{Path.home()}/Documents/CLIENT_SECRETS_copy.json"

def get_header(headers, name):
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return "No subject found"

def read_gmail_header(credential_file=credential_file):
    """Lists the subject of the latest email in the user's Gmail inbox."""
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credential_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().list(userId="me", labelIds=["INBOX"], maxResults=1).execute()
        messages = results.get("messages", [])

        if not messages:
            print("No messages found.")
            return

        for message in messages:
            msg = service.users().messages().get(userId="me", id=message["id"], format="metadata", metadataHeaders=["Subject"]).execute()
            headers = msg.get("payload", {}).get("headers", [])
            subject = get_header(headers, "Subject")

    except HttpError as error:
        print(f"An error occurred: {error}")

    return subject