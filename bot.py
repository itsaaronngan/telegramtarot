import os
import logging
from openai import OpenAI
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI API key (from environment)
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

# Pre-assign menu text and button text
FIRST_MENU = "<b>Main Menu</b>\n\nUse this bot to receive a 'Thesis, Antithesis, Synthesis' tarot reading."
ASK_READING_BUTTON = "Tarot Reading"
ASK_QUESTIONS_BUTTON = "Ask Questions"
HELP_BUTTON = "Help"

# Build keyboards
MAIN_MENU_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton(ASK_READING_BUTTON, callback_data=ASK_READING_BUTTON),
    InlineKeyboardButton(HELP_BUTTON, callback_data=HELP_BUTTON)
]])

READING_MENU_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton(ASK_QUESTIONS_BUTTON, callback_data=ASK_QUESTIONS_BUTTON),
]])

# Define a function to handle the /start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Welcome! I'm your tarot bot. You can get a 'Thesis, Antithesis, Synthesis' tarot reading or ask me anything. Use the menu below.",
        reply_markup=MAIN_MENU_MARKUP,
        parse_mode=ParseMode.HTML
    )

async def handle_tarot_reading(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # Use callback query to get the user's info
    user_first_name = query.from_user.first_name
    logger.info(f"User {user_first_name} requested a tarot reading.")

    # Send a request to OpenAI ChatGPT API for a tarot reading
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a tarot reader giving a 'Thesis, Antithesis, Synthesis' reading. Keep the responses brief and clear."},
            {"role": "user", "content": "I'd like a tarot reading."}
        ]
    )

    # Extract the tarot reading from the response
    tarot_reading = completion.choices[0].message.content

    # Send the tarot reading back to the user on Telegram
    await query.message.reply_text(
        f"<b>Your Tarot Reading:</b>\n\n{tarot_reading}",
        reply_markup=READING_MENU_MARKUP,
        parse_mode=ParseMode.HTML
    )
    await query.answer()

# Function to handle follow-up questions after the tarot reading
async def handle_followup_questions(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data

    if data == ASK_QUESTIONS_BUTTON:
        await query.message.reply_text("Please ask any follow-up questions you have about the tarot reading.")
    elif data == HELP_BUTTON:
        await query.message.reply_text("This bot provides a tarot reading using the 'Thesis, Antithesis, Synthesis' framework. After the reading, you can ask questions for further insights!")

    await query.answer()

# Function to handle inline button clicks
async def button_tap(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data

    if data == ASK_READING_BUTTON:
        await handle_tarot_reading(update, context)
    elif data == ASK_QUESTIONS_BUTTON:
        await query.message.reply_text("Please ask any follow-up questions you have about the tarot reading.")
    elif data == HELP_BUTTON:
        await query.message.reply_text("This bot provides a tarot reading using the 'Thesis, Antithesis, Synthesis' framework. After the reading, you can ask questions for further insights!")

    await query.answer()

# Function to handle text messages and follow-up questions
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    logger.info(f"User {update.message.from_user.first_name} said: {user_message}")

    # Send the user's message to OpenAI ChatGPT API for a response
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant providing follow-up guidance based on a tarot reading. The tarot reading is here: {tarot_reading}. (tarot reading ends)"},
            {"role": "user", "content": user_message}
        ]
    )

    # Extract the reply from the response
    reply = completion.choices[0].message.content

    # Send the reply back to the user on Telegram
    await update.message.reply_text(reply)

# Main function to set up the bot
def main() -> None:
    # Get the Telegram bot token from environment variables (set this in Heroku)
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler('start', start))

    # Register message handler for non-command text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_tap))

    # Start polling for updates from Telegram
    application.run_polling()

if __name__ == '__main__':
    main()