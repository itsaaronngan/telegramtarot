import os
import logging
import json
import requests
from openai import OpenAI
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler, Defaults

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI API key (from environment)
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

# Manually set version number
VERSION = "1.0"  # Update this manually whenever a new version is deployed

tarotsystem_prompt = f"""
   
    ## Instructions
    Create a 3 card Thesis, Antithesis, Synthesis tarot reading with a total of 500 words. Follow the sample structure exactly. Use casual conversational gentle tone. Promote conversation and in depth exploration.

    ## Tone, Style, and Language
    Avoid white juju and overly positive language that is overly vague/shallow. Avoid self-help buzzwords. Instead of using words like "transformation" use "transmutation", instead of "manifest" make references to "taking action" Use a gentle, empathetic, and respectful tone. Avoid overly formal language. If appropriate, reference the complexity inherant in life: e.g. happiness cannot be appreciated without sorrow.

    [Structure]
    ### Your Tarot Reading: [Card 1], [Card 2], [Card 3]    

	### Thesis/Antithesis/Synthesis Reading
    [gentle 50 word introduction explaining the basics of the "thesis, antithesis, synthesis" reading style and the purpose of the reading.   	avoid: greetings such as "hi there" or "hello there", excitement, overenthusiasm, chipper.]

    # Your Reading [short simple expressive title based on reading and context if available]
    ## Thesis - [Card Name] - [card expressive name]
    [Para 1]
    [Para 2]
    [Para 3]
    ## Antithesis - [Card Name] - [card expressive name]
    [Para 1]
    [Para 2]
    [Para 3]

    ## Synthesis - [Card Name] - [card expressive name]
    [Para 1]
    [Para 2]
    [Para 3]
 
    # Conclusion
    [Conclusion Paragraph - Overall reading interpretation and subtle relation to real life .]
    [/Structure]
    
    ---- [separator line]
    
    [Opening for discussion/conversation - based on the tarot reading prompt the reader for input or to ask questions to more deeply engage with the tarot reading]
    """

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

def split_message(message, chunk_size=4000):
    return [message[i:i + chunk_size] for i in range(0, len(message), chunk_size)]



def send_discord_message(message):
    discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    """
    Sends a message to a Discord channel using a webhook.
    """
       # Split the message into chunks for Discord (using the same chunking method)
    chunks = split_message(message)
    headers = {"Content-Type": "application/json"}
    
    for chunk in chunks:
        data = {"content": chunk}
        response = requests.post(discord_webhook_url, data=json.dumps(data), headers=headers)
        
        if response.status_code != 204:
            print(f"Failed to send message: {response.status_code}, {response.text}")

# Function to reset the conversation history
def reset_chat_history(context: CallbackContext) -> None:
    """Clears the conversation history for a fresh session."""
    context.user_data['chat_history'] = []

# Define a function to handle the /start command
async def start(update: Update, context: CallbackContext) -> None:
    # Reset the conversation history
    reset_chat_history(context)

    welcome_message = f"Welcome! I'm your tarot bot (Version {VERSION}). You can get a 'Thesis, Antithesis, Synthesis' tarot reading or ask me anything. Use the menu below."
    await update.message.reply_text(
        welcome_message,
        reply_markup=MAIN_MENU_MARKUP,
        parse_mode=ParseMode.HTML
    )
    send_discord_message(f"User {update.message.from_user.first_name} started the bot.\n\n{welcome_message}")

# Define a function to handle the /new command
async def new_reading(update: Update, context: CallbackContext) -> None:
    # Reset the conversation history
    reset_chat_history(context)

    new_reading_message = f"Starting a new tarot reading session (Version {VERSION}). You can get a fresh 'Thesis, Antithesis, Synthesis' tarot reading or ask anything. Use the menu below."
    await update.message.reply_text(
        new_reading_message,
        reply_markup=MAIN_MENU_MARKUP,
        parse_mode=ParseMode.HTML
    )
    send_discord_message(f"User {update.message.from_user.first_name} started a new reading.\n\n{new_reading_message}")

async def handle_tarot_reading(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # Use callback query to get the user's info
    user_first_name = query.from_user.first_name
    logger.info(f"User {user_first_name} requested a tarot reading.")

    # Send a request to OpenAI ChatGPT API for a tarot reading
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": tarotsystem_prompt},
        ]
    )

    # Extract the tarot reading from the response
    tarot_reading = completion.choices[0].message.content

    # Store the tarot reading in user_data for later reference
    context.user_data['tarot_reading'] = tarot_reading

    # Add the tarot reading to chat history
    context.user_data['chat_history'].append({"role": "assistant", "content": tarot_reading})

    # Split the tarot reading into chunks of 4096 characters
    chunks = split_message(tarot_reading)

    # Send each chunk separately to avoid Telegram's message length limit
    for chunk in chunks:
        await query.message.reply_text(
            f"<b>Your Tarot Reading:</b>\n\n{chunk}",
            reply_markup=READING_MENU_MARKUP,
            parse_mode=ParseMode.HTML
        )
    
    # Send the tarot reading to Discord in chunks
    for chunk in chunks:
        send_discord_message(f"User {user_first_name} received the following tarot reading chunk:\n\n{chunk}")

    await query.answer()

# Function to handle follow-up questions after the tarot reading
async def handle_followup_questions(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data

    if data == ASK_QUESTIONS_BUTTON:
        followup_message = "Please ask any follow-up questions you have about the tarot reading."
        await query.message.reply_text(followup_message)
        send_discord_message(f"User {query.from_user.first_name} asked for follow-up questions.\n\n{followup_message}")
    elif data == HELP_BUTTON:
        help_message = "This bot provides a tarot reading using the 'Thesis, Antithesis, Synthesis' framework. After the reading, you can ask questions for further insights!"
        await query.message.reply_text(help_message)
        send_discord_message(f"User {query.from_user.first_name} asked for help.\n\n{help_message}")

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
        ]
    )

    # Extract the reply from the response
    reply = completion.choices[0].message.content

    # Add the assistant's reply to chat history
    chat_history.append({"role": "assistant", "content": reply})

    # Update the stored chat history
    context.user_data['chat_history'] = chat_history

    # Send the reply back to the user on Telegram
    await update.message.reply_text(f"{reply}\n\n Use /start or /new to begin a new reading or continue your conversation.")
    send_discord_message(f"User {update.message.from_user.first_name} said: {user_message}\n\nBot replied: {reply}")

# Main function to set up the bot and webhook
def main() -> None:
    # Get the Telegram bot token and webhook URL from environment variables
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # You need to set this environment variable for your webhook URL

    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).defaults(Defaults(parse_mode=ParseMode.HTML)).build()

    # Set the webhook with optional secret_token
    webhook_data = {
        "url": WEBHOOK_URL,
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
        url_path=TELEGRAM_TOKEN,  # This specifies the path for webhook
        webhook_url=f"https://{os.getenv('HEROKU_APP_NAME')}.herokuapp.com/{TELEGRAM_TOKEN}"  # Full webhook URL
    )

if __name__ == '__main__':
    main()