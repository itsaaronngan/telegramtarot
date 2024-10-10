import os
import logging
from openai import OpenAI
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI API key (from Heroku config vars or environment)
client = OpenAI()

# Pre-assign menu text and button text
FIRST_MENU = "<b>Main Menu</b>\n\nUse this bot to interact with OpenAI's GPT model."
HELP_BUTTON = "Help"
ASK_GPT_BUTTON = "Ask GPT"

# Build keyboards
MAIN_MENU_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton(ASK_GPT_BUTTON, callback_data=ASK_GPT_BUTTON),
    InlineKeyboardButton(HELP_BUTTON, callback_data=HELP_BUTTON)
]])

# Define a function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Hello! I'm your AI-powered bot. You can ask me anything or use the menu below.",
        reply_markup=MAIN_MENU_MARKUP,
        parse_mode=ParseMode.HTML
    )

# Function to handle text messages and send them to OpenAI API
def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    logger.info(f"User {update.message.from_user.first_name} said: {user_message}")

    # Send the user's message to OpenAI API (ChatGPT)
    completion = client.chat.completions.create(
        model="gpt-4o",  # The model you're using
        messages=[
            {"role": "system", "content": "You are a helpful assistant in a telegram chatbot so keep your responses brief and keep on asking what is needed."},
            {"role": "user", "content": user_message}
        ]
    )

    # Extract the reply from the response
    reply = completion.choices[0].message

    # Send the reply back to the user on Telegram
    update.message.reply_text(reply)

# Function to handle inline button clicks
def button_tap(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data

    if data == ASK_GPT_BUTTON:
        query.message.reply_text("Please type your question for GPT.")
    elif data == HELP_BUTTON:
        query.message.reply_text("This bot can answer your questions using OpenAI's GPT model. Simply type a message or use the Ask GPT button!")

    query.answer()

# Main function to set up the bot
def main() -> None:
    # Get the Telegram bot token from environment variables (set this in Heroku)
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    # Create the Updater and Dispatcher
    updater = Updater(token=TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler('start', start))

    # Register message handler for non-command text messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Register callback query handler for inline buttons
    dispatcher.add_handler(CallbackQueryHandler(button_tap))

    # Start polling for updates from Telegram
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()