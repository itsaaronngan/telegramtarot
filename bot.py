import os
import logging
from openai import OpenAI
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, Defaults
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI API key (from environment)
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

# Manually set version number
VERSION = "1.0.0"  # Update this manually whenever a new version is deployed

# Pre-assign menu text and button text
FIRST_MENU = f"<b>Main Menu (Version {VERSION})</b>\n\nUse this bot to receive a 'Thesis, Antithesis, Synthesis' tarot reading."
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
        f"Welcome! I'm your tarot bot (Version {VERSION}). You can get a 'Thesis, Antithesis, Synthesis' tarot reading or ask me anything. Use the menu below.",
        reply_markup=MAIN_MENU_MARKUP,
        parse_mode=ParseMode.HTML
    )

# Define a function to handle the /new command
async def new_reading(update: Update, context: CallbackContext) -> None:
    # Reset the conversation history
    reset_chat_history(context)

    await update.message.reply_text(
        f"Starting a new tarot reading session (Version {VERSION}). You can get a fresh 'Thesis, Antithesis, Synthesis' tarot reading or ask anything. Use the menu below.",
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
            {"role": "system", "content": f"You are a gentle, empathetic, and conversational assistant providing thoughtful follow-up guidance based on a tarot reading. Review the chat history to understand the reading and the user's context. If the user shares something personal or emotional, respond with empathy (e.g., 'I can understand how that might feel') and follow up with gentle, open-ended questions like, 'Do you want to tell me more about what’s going on?' to keep the conversation flowing. Aim to be supportive, curious, and non-judgmental. The conversation history for your reference is: {chat_history}"},
            {"role": "user", "content": user_message}
    )

    # Extract the reply from the response
    reply = completion.choices[0].message.content

    # Add the assistant's reply to chat history
    chat_history.append({"role": "assistant", "content": reply})

    # Update the stored chat history
    context.user_data['chat_history'] = chat_history

    # Send the reply back to the user on Telegram
    await update.message.reply_text(f"{reply}\n\n Use /start or /new to begin a new reading or continue your conversation.",)

# Main function to set up the bot and webhook
def main() -> None:
    # Get the Telegram bot token and webhook URL from environment variables
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # You need to set this environment variable for your webhook URL
   # SECRET_TOKEN = os.getenv('SECRET_TOKEN')  # Optional secret token for verification (from env)

    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).defaults(Defaults(parse_mode=ParseMode.HTML)).build()

    # Set the webhook with optional secret_token
    webhook_data = {
        "url": WEBHOOK_URL,
      #  "secret_token": SECRET_TOKEN,  # Optional: can be None if not using a secret token
        "allowed_updates": ["message", "callback_query"],  # Only process specific updates
        "max_connections": 100,  # Example to increase max allowed connections
    }
    response = requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook", json=webhook_data)

    if response.status_code == 200:
        print("Webhook successfully set!")
    else:
        print(f"Failed to set webhook: {response.text}")

    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('new', new_reading))

    # Register message handler for non-command text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_tap))

    # Run the bot with the webhook (no polling)
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv('PORT', '8443')),
        url_path=TELEGRAM_TOKEN
    )

if __name__ == '__main__':
    main()