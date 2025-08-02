from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_accounts_keyboard(accounts: list[str]):
    """
    Creates an inline keyboard with a button for each Gmail account.
    """
    buttons = []
    for account in accounts:
        button = InlineKeyboardButton(
            text=account.capitalize(),
            callback_data=f"account:{account}"
        )
        buttons.append([button])  # Each button on a new row

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def create_message_count_keyboard(account_name: str):
    """
    Creates an inline keyboard to select the number of messages to fetch.
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="Last 10 messages",
                callback_data=f"fetch:{account_name}:10"
            )
        ],
        [
            InlineKeyboardButton(
                text="Last 50 messages",
                callback_data=f"fetch:{account_name}:50"
            )
        ]
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
