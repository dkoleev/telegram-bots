#pip install torch
#pip install transformers

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CallbackContext, InlineQueryHandler
from transformers import pipeline
import bot_tokens
from uuid import uuid4

# Initialize the transformer model
nlp = pipeline("text-generation", model="facebook/bart-large")  # or another model of your choice

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am your bot. Ask me anything!')

async def inline_query(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    #response = nlp(user_message, max_length=50)[0]['generated_text']
    response = nlp(user_message, max_length=50)
    print(response)
    
    results_list = []
    for item in response:
        result = InlineQueryResultArticle(
            id=str(uuid4()),
            title='Answer',
            input_message_content=InputTextMessageContent(item['generated_text'])
        )
        results_list.append(result)

    await update.inline_query.answer(results_list)

def main() -> None:
    application = Application.builder().token(bot_tokens.stackoverflow_bot_token).build()

     # on inline queries - show corresponding inline results
    application.add_handler(InlineQueryHandler(inline_query))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
