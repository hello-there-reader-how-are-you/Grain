#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


cred_file = "./ignore_me/credentials.json"
token_file = "./ignore_me/token.json"

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


class mailbox():
    def __init__(self):
        self.creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        self.service = build("gmail", "v1", credentials=self.creds)

    
    def most_recent_ten(self):
        results = self.service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        
        for message in messages:
            msg = self.service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['Subject']).execute()
            headers = msg['payload']['headers']
            subject = next(header['value'] for header in headers if header['name'] == 'Subject')
            print(subject)

    def emails_today(self):
        # Get the current date and the start of today
        now = datetime.datetime.now(datetime.timezone.utc)
        start_of_today = datetime.datetime(now.year, now.month, now.day)

        # Convert to RFC3339 timestamp format for Gmail API query
        start_of_today_str = start_of_today.isoformat() + 'Z'  # Z indicates UTC time

        # Call the Gmail API to get messages received from the start of today
        query = f'after:{start_of_today_str}'
        results = self.service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        
        if not messages:
            print('No messages found.')
            return 'No messages found.'

        titles = []
        for message in messages:
            msg = self.service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['Subject']).execute()
            headers = msg['payload']['headers']
            subject = next(header['value'] for header in headers if header['name'] == 'Subject')
            titles.append(subject)
        
        return titles
    

    def unread(self):
        # Get the current date and the date 5 days ago
        now = datetime.datetime.now(datetime.timezone.utc)
        five_days_ago = now - datetime.timedelta(days=5)

        # Convert to RFC3339 timestamp format for Gmail API query
        five_days_ago_str = five_days_ago.strftime("%Y-%m-%d")
        # Call the Gmail API to get unread messages received in the last 5 days
        query = f'is:unread after:{five_days_ago_str}'
        results = self.service.users().messages().list(userId='me', maxResults=499, q=query).execute()

        messages = results.get('messages', [])

        if not messages:
            print('No unread messages found.')
            return 'No unread messages found.'

        titles = []
        for message in messages:
            msg = self.service.users().messages().get(userId='me', id=message['id'], format='metadata', metadataHeaders=['Subject']).execute()
            headers = msg['payload']['headers']
            subject = next(header['value'] for header in headers if header['name'] == 'Subject')
            titles.append(subject)

        return titles


