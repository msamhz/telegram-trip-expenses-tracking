import json
import logging
import os
import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize the bot
TOKEN = os.getenv('API_KEY')
if not TOKEN:
    raise ValueError("No API_KEY environment variable set")

bot = Bot(token=TOKEN)

# Define command handler for /start
async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello World")

# Create the application
application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler('start', start))

# Initialize the application and the bot
async def initialize():
    await application.initialize()
    await bot.initialize()

def lambda_handler(event, context):
    """Handle incoming webhook from Telegram"""
    try:
        # Log the entire event for debugging
        logging.info("Received event: %s", json.dumps(event, indent=2))

        # Check if 'body' is in the event
        if 'body' not in event:
            raise ValueError("Event does not contain 'body'")

        # Process the incoming update
        body = json.loads(event['body'])
        update = Update.de_json(body, bot)
        
        # Initialize the application and bot and process the update using asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(initialize())
        loop.run_until_complete(application.process_update(update))
        
        return {
            'statusCode': 200,
            'body': json.dumps('Webhook processed')
        }
    except Exception as e:
        logging.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing webhook: {str(e)}")
        }