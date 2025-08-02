# How to get Gmail API Credentials

To use this bot, you need to authorize it to access your Gmail accounts. You'll need to generate a credential file for **each** Gmail account you want to connect.

Follow these steps to generate the necessary `token.json` file for each account.

## Step 1: Enable the Gmail API

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project or select an existing one.
3.  In the search bar, look for "Gmail API" and enable it for your project.

## Step 2: Create OAuth 2.0 Credentials

1.  Go to the "Credentials" page in the APIs & Services section of the console.
2.  Click on "Create Credentials" and select "OAuth client ID".
3.  If prompted, configure the consent screen.
    *   Choose "External" for the user type.
    *   Fill in the required fields (app name, user support email, developer contact information). You can use dummy information for your personal use.
    *   For scopes, you don't need to add any here.
    *   For test users, add the Gmail address(es) you want to authorize.
4.  Once the consent screen is configured, go back to "Credentials".
5.  Create the OAuth client ID:
    *   Select "Desktop app" as the application type.
    *   Give it a name (e.g., "Gmail Bot Client").
    *   Click "Create".
6.  A window will pop up with your client ID and client secret. Click "Download JSON" to download the `client_secret.json` file. **Do not share this file with anyone.**

## Step 3: Generate the Token File

This is the most important step. You will use the `client_secret.json` file to generate a `token.json` file that grants the bot access to your Gmail account.

Google provides "quickstart" guides for their APIs that include a script to handle this authorization flow.

1.  **Follow the Python Quickstart guide from Google:** [Google API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)
2.  When you follow the guide, it will ask you to download a `credentials.json` file. **This is the `client_secret.json` file you downloaded in the previous step.** Rename your downloaded file to `credentials.json` and place it in the same directory as the quickstart script.
3.  Run the quickstart script. It will open a browser window and ask you to log in to your Gmail account and grant permissions.
4.  After you grant permission, the script will create a `token.json` file in the same directory. This file contains your access and refresh tokens.

## Step 4: Add the Token to the Bot

1.  Take the `token.json` file you just generated.
2.  Rename it to something descriptive, for example, `personal_account.json` or `work_account.json`. The name of the file (before `.json`) will be used as the account name in the bot.
3.  Place this renamed file inside this `credentials` directory.
4.  Repeat steps 3 and 4 for every Gmail account you want to add to the bot.

Now you are ready to run the bot!
