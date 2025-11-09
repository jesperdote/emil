import os.path
import datetime
from flask import Flask, jsonify, render_template

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

app = Flask(__name__)

def get_gmail_service():
    """
    Authenticates with the Gmail API and returns a service object.
    Handles the OAuth 2.0 flow and token management.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Make sure your credentials.json is in the same directory
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # The port=0 argument will find a free port to run the local server
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    return build('gmail', 'v1', credentials=creds)

@app.route('/')
def index():
    """Renders the main HTML page."""
    return render_template('index.html')

def _parse_email_date(date_str):
    """Parses a date string from an email header into a timezone-aware datetime object."""
    if not date_str:
        return None
    try:
        # Example format: 'Tue, 17 Oct 2023 10:30:00 -0700 (PDT)'
        # We split on '(' to remove the timezone name if present, as it can vary
        return datetime.datetime.strptime(date_str.split(' (')[0].strip(), '%a, %d %b %Y %H:%M:%S %z')
    except (ValueError, IndexError):
        # Fallback for unexpected formats
        return None

def _format_email_age(parsed_date):
    """Formats the time difference into a human-readable 'age' string."""
    if not parsed_date:
        return "Unknown"
        
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    age = now_utc - parsed_date
    
    seconds = age.total_seconds()
    if seconds < 60:
        return "Just now"

    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    age_str = ""
    if days > 0:
        age_str += f"{int(days)}d "
    if hours > 0:
        age_str += f"{int(hours)}h "
    age_str += f"{int(minutes)}m ago"
    return age_str.strip()

@app.route('/api/emails')
def get_emails():
    """API endpoint to fetch and process unread emails."""
    try:
        service = get_gmail_service()
        
        # Search for unread emails. You can customize the query.
        # For example, to search by subject: 'is:unread subject:"Your Subject Here"'
        results = service.users().messages().list(userId='me', q='is:unread').execute()
        messages = results.get('messages', [])
        
        email_data = []
        if not messages:
            return jsonify([])
        
        for message in messages[:20]: # Limit to the 20 most recent for performance
            msg = service.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
            headers = msg.get('payload', {}).get('headers', [])
            
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            date_str = next((h['value'] for h in headers if h['name'] == 'Date'), None)
            
            parsed_date = _parse_email_date(date_str)
            age_str = _format_email_age(parsed_date)
            
            # Only add emails we could successfully parse
            if parsed_date:
                email_data.append({
                    'subject': subject,
                    'age': age_str
                })

        return jsonify(email_data)

    except HttpError as error:
        error_str = str(error)
        # Check for the specific "API not enabled" error from Google
        if "Gmail API has not been used" in error_str or "accessNotConfigured" in error_str:
            print("\n--- [ACTION REQUIRED] GMAIL API NOT ENABLED ---")
            print("The Gmail API is not enabled for your Google Cloud project.")
            print("Please enable it by visiting the link in the error message below, then restart the application.")
            print("It may take a few minutes for the change to take effect.")
            print(f"Error details: {error_str}")
            print("------------------------------------------------\n")
            return jsonify({"error": "Gmail API is not enabled. See server console for details."}), 500
        else:
            print(f'An HTTP error occurred: {error}')
            return jsonify({"error": str(error)}), 500
    except Exception as e:
        print(f'A general error occurred: {e}')
        # This can happen if credentials.json is missing
        return jsonify({"error": "An internal error occurred. Check server logs."}), 500

if __name__ == '__main__':
    # Running on 0.0.0.0 makes it accessible on your local network
    app.run(host='0.0.0.0', port=5001, debug=True)
