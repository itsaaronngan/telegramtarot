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

# Function to reset the conversation history
def reset_chat_history(context: CallbackContext) -> None:
    """Clears the conversation history for a fresh session."""
    context.user_data['chat_history'] = []

# Define a function to handle the /start command
async def start(update: Update, context: CallbackContext) -> None:
    # Reset the conversation history
    reset_chat_history(context)

    await update.message.reply_text(
        "Welcome! I'm your tarot bot. You can get a 'Thesis, Antithesis, Synthesis' tarot reading or ask me anything. Use the menu below.",
        reply_markup=MAIN_MENU_MARKUP,
        parse_mode=ParseMode.HTML
    )

# Define a function to handle the /new command
async def new_reading(update: Update, context: CallbackContext) -> None:
    # Reset the conversation history
    reset_chat_history(context)

    await update.message.reply_text(
        "Starting a new tarot reading session. You can get a fresh 'Thesis, Antithesis, Synthesis' tarot reading or ask anything. Use the menu below.",
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
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a tarot reader giving a 'Thesis, Antithesis, Synthesis' reading. Keep the responses brief and clear. After your reading, inform the user they can either continue chatting or use /start or /new to begin a new reading."},
            {"role": "user", "content": "I'd like a tarot reading."}
        ]
    )

    # Extract the tarot reading from the response
    tarot_reading = completion.choices[0].message.content

    # Store the tarot reading in user_data for later reference
    context.user_data['tarot_reading'] = tarot_reading

    # Add the tarot reading to chat history
    context.user_data['chat_history'].append({"role": "assistant", "content": tarot_reading})

    # Send the tarot reading back to the user on Telegram
    await query.message.reply_text(
        f"<b>Your Tarot Reading:</b>\n\n{tarot_reading}\n\nYou can continue chatting, or use /start or /new to begin a new reading.",
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
        await query.message.reply_text("This bot can give you a tarot reading using the 'Thesis, Antithesis, Synthesis' spread. You can also ask questions for deeper insight.")
    
    await query.answer()

# Function to handle text messages and follow-up questions
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    logger.info(f"User {update.message.from_user.first_name} said: {user_message}")

    # Retrieve the stored chat history
    chat_history = context.user_data.get('chat_history', [])

    # Add the user's message to chat history
    chat_history.append({"role": "user", "content": user_message})

    # Send the user's message and previous chat history to OpenAI ChatGPT API for a response
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are a helpful assistant providing follow-up guidance based on a tarot reading. Review the chat history to understand the tarot reading and the context. Before responding analyse the user message and identify whether to ask for more information, or be supportive, or provide balanced non-judgemental feedback. Responding gently and conversationally. The conversation history for your reference is: {chat_history}"},
            {"role": "user", "content": user_message}
        ]
    # Extract the reply from the response
    reply = completion.choices[0].message.content

    # Add the assistant's reply to chat history
    chat_history.append({"role": "assistant", "content": reply})

    # Update the stored chat history
    context.user_data['chat_history'] = chat_history

    # Send the reply back to the user on Telegram
    await update.message.reply_text(f"{reply}\n\nYou can continue chatting, or use /start or /new to begin a new reading.")

# Main function to set up the bot
def main() -> None:
    # Get the Telegram bot token from environment variables (set this in Heroku)
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('new', new_reading))  # Added handler for /new command

    # Register message handler for non-command text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_tap))

    # Start polling for updates from Telegram
    application.run_polling()

if __name__ == '__main__':
    main()