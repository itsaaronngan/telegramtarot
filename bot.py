import os
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Initialize OpenAI API key (from Heroku config vars or environment)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define a function to handle the /start command
def start(update, context):
    update.message.reply_text("Hello! I'm your AI-powered bot. Ask me anything!")

# Define a function to handle text messages
def handle_message(update, context):
    user_message = update.message.text

    # Send the user's message to OpenAI API (ChatGPT)
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Replace 'gpt-4' with 'gpt-3.5-turbo' if necessary
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ]
    )

    # Extract the reply from the response
    reply = response['choices'][0]['message']['content']

    # Send the reply back to the user on Telegram
    update.message.reply_text(reply)

# Main function to set up the bot
def main():
    # Get the Telegram bot token from environment variables (set this in Heroku)
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    # Create an Updater object to handle updates from Telegram
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handler for the /start command
    dispatcher.add_handler(CommandHandler('start', start))

    # Add message handler for all text messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start polling for updates from Telegram
    updater.start_polling()

    # Keep the bot running​⬤