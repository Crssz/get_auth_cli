#!/usr/bin/env python3
"""
YouTube OAuth 2.0 Token Generator
This script generates token.json for YouTube Data API v3 authentication
"""

import os
import sys

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at https://console.developers.google.com/.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

TOKEN_FILE = 'token.json'


def generate_token():
    """
    Generate and save OAuth 2.0 token for YouTube API authentication.
    """
    creds = None
    
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(TOKEN_FILE):
        print(f"Found existing {TOKEN_FILE}")
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
            print("Token refreshed successfully!")
        else:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                print(f"Error: {CLIENT_SECRETS_FILE} not found!")
                print("Please download your OAuth 2.0 credentials from Google Cloud Console")
                print("and save it as 'client_secret.json' in the same directory as this script.")
                sys.exit(1)
            
            print(f"Starting OAuth 2.0 authorization flow...")
            print("A browser window will open for you to authorize the application.")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=4200)
            
            print("\nAuthorization successful!")
        
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        
        print(f"\n✓ Token saved successfully to {TOKEN_FILE}")
        print(f"✓ Scopes: {', '.join(SCOPES)}")
        print(f"\nYou can now use this token file with your YouTube API applications.")
    else:
        print(f"✓ Token is valid and up to date!")
        print(f"✓ Token file: {TOKEN_FILE}")
        print(f"✓ Scopes: {', '.join(SCOPES)}")


def main():
    print("=" * 60)
    print("YouTube OAuth 2.0 Token Generator")
    print("=" * 60)
    print()
    
    try:
        generate_token()
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
    
    print()
    print("=" * 60)


if __name__ == '__main__':
    main()

