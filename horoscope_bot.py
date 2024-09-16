import logging
import requests
from html import escape
from uuid import uuid4
from telegram.constants import ParseMode
from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, InlineQueryHandler

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

horoscope_url = 'https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! Enter /horoscope command and select your zodiac sign.",
        reply_markup=ForceReply(selective=False),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def horoscope_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Aries ♈", callback_data="Aries"),
            InlineKeyboardButton("Taurus ♉", callback_data="Taurus"),
            InlineKeyboardButton("Gemini ♊", callback_data="Gemini"),
        ],
        [
            InlineKeyboardButton("Cancer ♋", callback_data="Cancer"),
            InlineKeyboardButton("Leo ♌", callback_data="Leo"),
            InlineKeyboardButton("Virgo ♍", callback_data="Virgo"),
        ],
        [
            InlineKeyboardButton("Libra ♎", callback_data="Libra"),
            InlineKeyboardButton("Scorpio ♏", callback_data="Scorpio"),
            InlineKeyboardButton("Sagittarius ♐", callback_data="Sagittarius"),
        ],
        [
            InlineKeyboardButton("Capricorn ♑", callback_data="Capricorn"),
            InlineKeyboardButton("Aquarius ♒", callback_data="Aquarius"),
            InlineKeyboardButton("Pisces ♓", callback_data="Pisces"),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def button_press_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    horoscope =  get_daily_horoscope(query.data, 'today')
    await query.edit_message_text(text=horoscope, parse_mode=ParseMode.HTML)

def get_daily_horoscope(sign: str, day: str) -> dict:
    """Get daily horoscope for a zodiac sign.
    Keyword arguments:
    sign:str - Zodiac sign
    day:str - Date in format (YYYY-MM-DD) OR TODAY OR TOMORROW OR YESTERDAY
    Return:dict - JSON data
    """
    params = {"sign": sign, "day": day}
    response = requests.get(horoscope_url, params)
    if response.status_code == 200:
        data = response.json()
        date = data['data']['date']
        horoscope = data['data']['horoscope_data']
        formatted_result = f"<i>Horoscope for</i> <b>{sign.capitalize()}</b>:\n\n {horoscope}"
        return formatted_result
    else:
        return "Sorry, I couldn't fetch the horoscope for that day."
    

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query."""
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id="1",
            title="Caps",
            input_message_content=InputTextMessageContent(query.upper()),
        )
    )
    await update.inline_query.answer(results)

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the inline query. This is run when you type: @botusername <query>"""
    query = update.inline_query.query

    results = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="♈ Aries",
            input_message_content=InputTextMessageContent(get_daily_horoscope('Aries', 'today'), parse_mode=ParseMode.HTML),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="♉ Taurus",
            input_message_content=InputTextMessageContent(get_daily_horoscope('Taurus', 'today'), parse_mode=ParseMode.HTML),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="♊ Gemini",
            input_message_content=InputTextMessageContent(get_daily_horoscope('Gemini', 'today'), parse_mode=ParseMode.HTML),
        ),

        InlineQueryResultArticle(
            id=str(uuid4()),
            title="♋ Cancer",
            input_message_content=InputTextMessageContent(get_daily_horoscope('Cancer', 'today'), parse_mode=ParseMode.HTML),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="♌ Leo",
            input_message_content=InputTextMessageContent(get_daily_horoscope('Leo', 'today'), parse_mode=ParseMode.HTML),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="♍ Virgo",
            input_message_content=InputTextMessageContent(get_daily_horoscope('Virgo', 'today'), parse_mode=ParseMode.HTML),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="♎ Libra",
            input_message_content=InputTextMessageContent(get_daily_horoscope('Libra', 'today'), parse_mode=ParseMode.HTML),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="♏ Scorpio",
            input_message_content=InputTextMessageContent(get_daily_horoscope('Scorpio', 'today'), parse_mode=ParseMode.HTML),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="♐ Sagittarius",
            input_message_content=InputTextMessageContent(get_daily_horoscope('Sagittarius', 'today'), parse_mode=ParseMode.HTML),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="♑ Capricorn",
            input_message_content=InputTextMessageContent(get_daily_horoscope('Capricorn', 'today'), parse_mode=ParseMode.HTML),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="♒ Aquarius",
            input_message_content=InputTextMessageContent(get_daily_horoscope('Aquarius', 'today'), parse_mode=ParseMode.HTML),
        ),
        InlineQueryResultArticle(
            id=str(uuid4()),
            title="♓ Pisces",
            input_message_content=InputTextMessageContent(get_daily_horoscope('Pisces', 'today'), parse_mode=ParseMode.HTML),
        ),
    ]

    await update.inline_query.answer(results)

def main() -> None:
    application = Application.builder().token(bot_tokens.today_horoscope_bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("horoscope", horoscope_command))
    application.add_handler(CallbackQueryHandler(button_press_handler))

     # on inline queries - show corresponding inline results
    application.add_handler(InlineQueryHandler(inline_query))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()