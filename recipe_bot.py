import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import bot_tokens

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

API_KEY = 'e806a7fd5326406fa9284cf020e8c8c7'

def find_recipes(ingredients):
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients}&number=5&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        recipes = response.json()
        return recipes
    else:
        return None

async def start(update: Update, context):
    await update.message.reply_text(
        "Hello! I'm a Recipe Finder Bot. Send me a list of ingredients separated by commas, and I'll find some recipes for you!"
    )

async def get_recipes(update: Update, context):
    ingredients = update.message.text
    recipes = find_recipes(ingredients)
    
    if recipes:
        for recipe in recipes:
            title = recipe['title']
            image = recipe['image']
            await update.message.reply_text(f"Recipe: {title}\n{image}")
    else:
        await update.message.reply_text("Sorry, I couldn't find any recipes. Please try again.")

def main():
    application = ApplicationBuilder().token(bot_tokens.recipe_top_bot_token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_recipes))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
