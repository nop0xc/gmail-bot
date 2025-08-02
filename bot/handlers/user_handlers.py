import os
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.services import gmail_service
from bot.keyboards import inline

# Load admin IDs from .env file
ADMIN_IDS = [int(admin_id) for admin_id in os.getenv("ADMIN_IDS", "").split(',') if admin_id]

router = Router()

# Middleware to check for admin access on the special command
@router.message(Command("amier#12345r"))
async def protected_command_handler(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("You do not have permission to use this command.")
        return

    await list_accounts_command(message)


@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Bot is running.")

@router.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "This bot helps you check your Gmail inbox.\n\n"
        "Commands:\n"
        "/start - Check if the bot is running.\n"
        "/help - Show this help message.\n"
    )
    if message.from_user.id in ADMIN_IDS:
        help_text += "/amier#12345r - (Admin only) List available Gmail accounts to check."

    await message.answer(help_text)

async def list_accounts_command(message: Message):
    accounts = gmail_service.get_available_accounts()
    if not accounts:
        await message.answer("No Gmail accounts found. Please add credential files to the 'credentials' directory.")
        return

    keyboard = inline.create_accounts_keyboard(accounts)
    await message.answer("Select a Gmail account to check:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("account:"))
async def select_account_callback(callback: CallbackQuery):
    account_name = callback.data.split(":")[1]
    keyboard = inline.create_message_count_keyboard(account_name)
    await callback.message.edit_text(
        f"You selected: {account_name.capitalize()}\n\nHow many messages would you like to see?",
        reply_markup=keyboard
    )
    await callback.answer()

@router.callback_query(F.data.startswith("fetch:"))
async def fetch_messages_callback(callback: CallbackQuery, bot: Bot):
    _, account_name, count_str = callback.data.split(":")
    count = int(count_str)

    await callback.message.edit_text(f"Fetching the last {count} messages for {account_name.capitalize()}...")

    emails = gmail_service.get_latest_messages(account_name, count)

    if isinstance(emails, str):  # Error message returned
        await callback.message.answer(emails)
        return

    if not emails:
        await callback.message.answer("No messages found.")
        return

    response_text = f"**Last {len(emails)} messages for {account_name.capitalize()}:**\n\n"
    for i, email in enumerate(emails, 1):
        response_text += (
            f"**{i}. Subject:** {email['subject']}\n"
            f"   **From:** {email['from']}\n"
            f"   **Date:** {email['date']}\n"
            f"   **Snippet:** {email['snippet']}\n\n"
        )

    # For long messages, Telegram might require splitting them.
    # A simple approach is to send one message.
    if len(response_text) > 4096:
        await callback.message.answer("The message is too long to display. Future versions will have pagination.")
        # Sending a truncated version for now
        await callback.message.answer(response_text[:4090] + "...")
    else:
        await callback.message.answer(response_text)

    await callback.answer()
