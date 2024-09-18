#https://github.com/openai/openai-python?tab=readme-ov-file
#https://pypi.org/project/python-dotenv/

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, InlineQueryHandler, CallbackContext
import os
from uuid import uuid4
import bot_tokens
from openai import OpenAI

openai_client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get(bot_tokens.openai_key),
)

TELEGRAM_TOKEN = bot_tokens.stackoverflow_bot_token

def generate_answer(prompt):
    chat_completion = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    print(chat_completion)
    return chat_completion

async def inline_query(update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return

    # Generate a response using OpenAI
    answers = generate_answer(query)

    results_list = []
    for item in answers:
        result = InlineQueryResultArticle(
            id=str(uuid4()),
            title='Answer',
            input_message_content=InputTextMessageContent(item.text.strip())
        )
        results_list.append(result)

    await update.inline_query.answer(results_list)

def main():
    application = Application.builder().token(bot_tokens.stackoverflow_bot_token).build()

     # on inline queries - show corresponding inline results
    application.add_handler(InlineQueryHandler(inline_query))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
