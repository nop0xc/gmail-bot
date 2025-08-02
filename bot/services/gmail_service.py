import os
import glob
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CREDENTIALS_DIR = "credentials"
# We only need to read emails, so we use the readonly scope.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_available_accounts():
    """
    Scans the credentials directory for available account token files.
    The account name is derived from the filename (e.g., 'personal.json').
    """
    if not os.path.exists(CREDENTIALS_DIR):
        return []
    token_files = glob.glob(os.path.join(CREDENTIALS_DIR, '*.json'))
    # Exclude client_secret.json, if present
    token_files = [f for f in token_files if 'client_secret' not in os.path.basename(f)]
    # Return just the account name part of the file
    return [os.path.basename(f).replace('.json', '') for f in token_files]

def get_gmail_service(account_name: str):
    """
    Creates a Gmail API service object for a given account.
    Handles token refresh.
    """
    creds = None
    token_path = os.path.join(CREDENTIALS_DIR, f"{account_name}.json")

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    # This part of the code is more for completeness; in the bot's flow,
    # we expect the token files to be present.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token for {account_name}: {e}")
                return None
        else:
            # This flow should not be triggered in production.
            # The user must generate tokens beforehand.
            print(f"Token for {account_name} not found or invalid. Please generate it first.")
            return None

        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred building the service: {error}")
        return None

def get_latest_messages(account_name: str, count: int = 10):
    """
    Fetches the most recent 'count' emails from the specified Gmail account.
    """
    service = get_gmail_service(account_name)
    if not service:
        return f"Could not connect to Gmail for account: {account_name}. Please check the credentials."

    try:
        # Get the list of messages
        results = service.users().messages().list(userId='me', maxResults=count).execute()
        messages = results.get('messages', [])

        if not messages:
            return "No new messages found."

        email_list = []
        for message_info in messages:
            msg = service.users().messages().get(userId='me', id=message_info['id']).execute()
            headers = msg['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')
            snippet = msg['snippet']

            email_list.append({
                'subject': subject,
                'from': sender,
                'date': date,
                'snippet': snippet
            })
        return email_list

    except HttpError as error:
        return f"An error occurred fetching emails: {error}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
