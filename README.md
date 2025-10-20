# YouTube OAuth 2.0 Token Generator

A simple Python script to generate `token.json` for YouTube Data API v3 authentication.

## Purpose

This tool generates OAuth 2.0 authentication tokens that can be used with YouTube API applications. The generated `token.json` file contains your access token and refresh token for authenticated YouTube API access.

## Features

- Simple OAuth 2.0 authentication flow
- Automatic token refresh for expired tokens
- Validates existing tokens
- Clean command-line interface
- No upload functionality - focuses solely on token generation

## Prerequisites

1. Python 3.6 or higher
2. Google Cloud Project with YouTube Data API v3 enabled
3. OAuth 2.0 credentials (client_secret.json)

## Setup Instructions

### 1. Create a Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3:
   - Navigate to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"

### 2. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Configure the OAuth consent screen if prompted:
   - User Type: External (for personal use) or Internal (for organization)
   - Fill in required fields (App name, User support email, Developer contact)
   - Add the scope: https://www.googleapis.com/auth/youtube.upload
   - Add your email as a test user (if using External)
4. Create OAuth client ID:
   - Application type: Desktop app
   - Name: Give it a descriptive name (e.g., "YouTube Token Generator")
   - **IMPORTANT**: Add authorized redirect URI:
     * Click "ADD URI" under "Authorized redirect URIs"
     * Enter: http://localhost:4200/
     * Make sure to include the trailing slash
5. Download the credentials JSON file
6. Rename it to `client_secret.json` and place it in the same directory as `generate_token.py`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install google-auth-oauthlib google-auth
```

## Usage

Simply run the script:

```bash
python generate_token.py
```

The script will:
1. Check if `client_secret.json` exists
2. Check if `token.json` already exists and is valid
3. If no valid token exists:
   - Open your browser for OAuth authorization
   - Ask you to sign in with your Google account
   - Request permission to access YouTube on your behalf
   - Save the token to `token.json`
4. If a valid token exists:
   - Verify it and display confirmation

## First Run Authentication

When you run the script for the first time:

1. A browser window will open automatically on http://localhost:4200
2. Sign in with your Google account
3. Grant the requested permissions for YouTube access
4. The browser will show a success message
5. The script will save your credentials in `token.json`
6. Future runs will verify the token is still valid

## Files

### Required (you must provide):
- `client_secret.json`: Your OAuth 2.0 client credentials from Google Cloud Console

### Generated:
- `token.json`: OAuth credentials with access and refresh tokens (auto-generated on first run)

## Important Notes

1. **Security**: Keep `client_secret.json` and `token.json` secure - they contain sensitive authentication information
2. **Version Control**: Add to `.gitignore` if using version control:
   ```
   client_secret.json
   token.json
   ```
3. **Token Scopes**: The generated token has YouTube upload scope (`https://www.googleapis.com/auth/youtube.upload`)
4. **Token Refresh**: Tokens are automatically refreshed when expired
5. **Port**: The script uses port 4200 for the OAuth callback

## Troubleshooting

### "client_secret.json not found"
- Make sure you've downloaded the OAuth credentials from Google Cloud Console
- Rename the file to `client_secret.json`
- Place it in the same directory as `generate_token.py`

### Browser doesn't open
- Manually navigate to the URL shown in the console
- Complete the authorization in your browser

### "Redirect URI mismatch" error
This error occurs when the redirect URI is not properly configured.

**Solution:**
1. Go to Google Cloud Console → APIs & Services → Credentials
2. Click on your OAuth 2.0 Client ID
3. Under "Authorized redirect URIs", add: `http://localhost:4200/`
4. **Important**: Include the trailing slash (/)
5. Click "Save"
6. Wait a few minutes for changes to propagate
7. Try running the script again

### Authentication Issues
- Delete `token.json` and re-run the script to re-authenticate
- Check that your OAuth consent screen is properly configured
- Ensure your email is added as a test user (for External apps in testing mode)
- Verify the YouTube Data API v3 is enabled in your project

### Token expires quickly
- This is normal for test/development apps
- The script automatically refreshes expired tokens using the refresh token
- Re-run the script to refresh the token

## Using the Generated Token

Once you have `token.json`, you can use it in your YouTube API applications:

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load the token
creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# Build the YouTube service
youtube = build('youtube', 'v3', credentials=creds)

# Now you can make API calls
# Example: list your channels
channels = youtube.channels().list(part='snippet', mine=True).execute()
```

## License

This script is provided as-is for educational and personal use.

