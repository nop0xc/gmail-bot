# Telegram Gmail Bot

This is a Telegram bot that allows you to securely check the latest emails from one or more Gmail accounts directly from a Telegram chat.

## Features

- **Multi-Account Support**: Check emails from multiple Gmail accounts.
- **Secure**: Uses OAuth 2.0 for authentication. Your password is not stored. Access is restricted to read-only.
- **Persistent Login**: Stays logged in using refresh tokens, so you don't have to re-authenticate.
- **Admin Protection**: Access to view emails is protected by a special command restricted to admin user IDs.
- **Simple Interface**: Uses inline keyboards for easy navigation.

## Prerequisites

- Python 3.8+
- A Telegram Bot Token. You can get one from [BotFather](https://t.me/botfather).
- One or more Gmail accounts you want to monitor.

## Setup Instructions

1.  **Clone the Repository**
    ```bash
    git clone <repository_url>
    cd gmail-telegram-bot
    ```

2.  **Create a Virtual Environment (Recommended)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    -   There is a `.env` file in the root of the project.
    -   Open the `.env` file and add your Telegram Bot Token and your numeric Telegram User ID.
    ```env
    BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
    ADMIN_IDS=YOUR_ADMIN_ID1,YOUR_ADMIN_ID2
    ```
    -   You can find your User ID by messaging a bot like [@userinfobot](https://t.me/userinfobot).
    -   You can add multiple comma-separated `ADMIN_IDS`.

5.  **Generate Gmail Credentials**
    -   This is the most important step. You need to generate a credential file for **each** Gmail account you want to connect.
    -   Follow the detailed instructions in the `credentials/README.md` file to generate your `token.json` files.
    -   Place the generated token files (e.g., `personal_account.json`, `work_account.json`) inside the `credentials` directory.

## Usage

1.  **Run the Bot**
    ```bash
    python main.py
    ```
    If everything is set up correctly, you will see a "Bot started" message in your console.

2.  **Interact with the Bot on Telegram**
    -   Find your bot on Telegram and send the `/start` command. It should reply with "Bot is running."
    -   Send the `/help` command for a list of commands.
    -   If you are an admin, send the special command `amier#12345r`. The bot will display a list of your configured Gmail accounts.
    -   Click on an account, then select whether you want to see the last 10 or 50 messages. The bot will fetch and display them for you.

## Security

-   **Never share your `client_secret.json` file, your `.env` file, or any of the `token.json` files in the `credentials` directory.**
-   The bot only requests `readonly` access to your Gmail account, meaning it can only read emails and cannot send, delete, or modify anything.
-   It is recommended to run this bot on a secure, private server.
-   If this code is part of a larger git repository, make sure to add `.env` and `credentials/` to your `.gitignore` file.
