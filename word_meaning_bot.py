import logging

from collections import defaultdict
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import requests

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=False),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Enter the word you need the explanation for.")

async def explain_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Explain the meaning of a word."""
    meaning = get_meaning(update.message.text)
    await update.message.reply_text(meaning, parse_mode='HTML')
    # words = update.message.text.split()
    # if words.count == 0:
    #     await update.message.reply_text("Please enter a word.")
    # else:
    #     meaning = get_meaning(words[0])
    #     await update.message.reply_text(meaning)

def get_meaning(word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return format_respone2(data)
    else:
        return f"Sorryy, I couldn't find the meaning of '{word}'."

def format_respone(data):
    print(data)
    meaning = data[0]['meanings'][0]['definitions'][0]['definition']
    audio = data[0]['phonetics'][0]['audio']
    result = '\n'.join([meaning, audio])
    print(result)
    return result

def format_respone2(data):
    meanings = defaultdict(list)
    meainig_key = 'meanings'
    if meainig_key in data[0]:
        for meaning in data[0][meainig_key]:
            part_of_speech = meaning['partOfSpeech']
            for index, definition in enumerate(meaning['definitions']):
                if index > 3:
                    break
                meaning_text = definition['definition']
                if 'example' in definition:
                    example = '\n<i>example: ' + definition['example'] + "</i>"
                else:
                    example = ''
                
                meanings
                meanings[part_of_speech].append({
                    'meaning': meaning_text,
                    'example': example
                })
    
    parts_text = {}
    for part_of_speech, value in meanings.items():
        parts_text[part_of_speech] = '\n'.join([f"\t<b>{index+1}</b>. {item['meaning']}{item['example']}" for index, item in enumerate(value)])

    final = ''
    if  data[0]['phonetics'] and 'text' in data[0]['phonetics'][0]:
        phonetic = data[0]['phonetics'][0]['text']
    else:
        phonetic = None
    if data[0]['phonetics'] and 'audio' in data[0]['phonetics'][0]:
        audio = data[0]['phonetics'][0]['audio']
    else:
        audio = None
    
    if phonetic is not None:
        final = f'<b>Phonetics:</b> {phonetic}'
    else:
        final = ''
    for part, data in parts_text.items():
        final += '\n\n<b><u>' + part + '</u></b>\n\n' + data
    final += f'\n\n{audio}'

    return  final

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6410746366:AAFGKGscSYnaYVpOjrgQUGx7TgOwOsqyDak").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, explain_word))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()