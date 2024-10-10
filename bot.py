import os
from openai import OpenAI
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Initialize OpenAI API key (from Heroku config vars or environment)
client = OpenAI()

# Define a function to handle the /start command
def start(update, context):
    update.message.reply_text("Hello! I'm your AI-powered bot. Ask me anything!")

# Define a function to handle text messages
def handle_message(update, context):
    user_message = update.message.text

    # Send the user's message to OpenAI API (ChatGPT)
    completion = client.chat.completions.create(
        model="gpt-4o",  # Model you provided
        messages=[
            {"role": "system", "content": "You are a helpful assistant in a telegram chatbot, keep your responses brief and prompt for additional input and confirmations"},
            {"role": "user", "content": user_message}
        ]
    )

    # Extract the reply from the response (using your provided structure)
    reply = completion.choices[0].message

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
    updater.idle()  # Keep the bot running

if __name__ == '__main__':
    main()