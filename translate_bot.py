#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Don't forget to enable inline mode with @BotFather

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
from html import escape
from uuid import uuid4
import requests
import json

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler

# import from the parent directory
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)
import bot_tokens

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# LibreTranslate API URL
TRANSLATE_API_URL = 'https://libretranslate.com/translate'


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Welcome! Send me a message, and I will translate it for you.')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text('Welcome! Send me a message, and I will translate it for you.')

def translate_message(text: str, target_lang: str = 'en') -> str:
    headers = {
    'Content-Type': 'application/json',
    }

    params = {
        'q': str,
        'source': 'auto',  # Automatically detect the source language
        'target': target_lang,
        'format': 'text'
    }

    response = requests.post(TRANSLATE_API_URL, json=params, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('translatedText', 'Translation error!')
    else:
        return f'Error in translation API! {response.status_code} {response.reason}'
    
# Function to handle incoming messages
async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query
    if not query:  # empty query should not be handled
        return

    # Default target language is English ('en')
    translated_text = translate_message(query, target_lang='en')
    print(translated_text)

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=translated_text,
            input_message_content=InputTextMessageContent(translated_text),
        )
    ]

    await update.inline_query.answer(results)

# Function to handle errors
def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f'Update {update} caused error {context.error}')


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_tokens.auto_eng_bot_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on inline queries - show corresponding inline results
    application.add_handler(InlineQueryHandler(inline_query))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
    #print(translate_message('hello', target_lang='en'))