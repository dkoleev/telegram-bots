from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, InlineQueryHandler, CallbackContext, CommandHandler, CallbackQueryHandler
import requests
import logging
import bot_tokens

BOT_TOKEN = bot_tokens.stackoverflow_bot_token

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define the function to handle inline queries
async def inline_query(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return

    # Fetch information from Stack Overflow
    response = requests.get(f'https://api.stackexchange.com/2.3/search?order=desc&sort=relevance&intitle={query}&site=stackoverflow')
    results = response.json().get('items', [])

    results_list = []
    for item in results:
        title = item.get('title')
        link = item.get('link')
        result = InlineQueryResultArticle(
            id=item.get('question_id'),
            title=title,
            input_message_content=InputTextMessageContent(f'Question: {title}\nLink: {link}')
        )
        results_list.append(result)

    await update.inline_query.answer(results_list)

# Define the main function to set up the bot
def main():
    application = Application.builder().token(bot_tokens.stackoverflow_bot_token).build()

     # on inline queries - show corresponding inline results
    application.add_handler(InlineQueryHandler(inline_query))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
