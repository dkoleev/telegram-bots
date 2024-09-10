from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from mcrcon import MCRcon
import rust_servers
import rust_remote_commands

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I am your Rust bot. What do you want to do?")

# Command to allow users to search for servers
async def search_server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        search_term = " ".join(context.args)  # The search term is entered by the user
        servers = rust_servers.get_rust_servers(search_term)

        if servers:
            message = "Here are some matching servers:\n"
            for server in servers[:5]:  # Limit to 5 results
                name = server['attributes']['name']
                players = server['attributes']['players']
                max_players = server['attributes']['maxPlayers']
                address = server['attributes']['ip']
                port = server['attributes']['port']
                message += f"Name: {name}\nPlayers: {players}/{max_players}\nIP: {address}:{port}\n\n"
        else:
            message = "No servers found for your search term."
    else:
        message = "Please provide a search term."

    await update.message.reply_text(message)

# Example command function for checking player status
async def player_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = rust_remote_commands.send_rcon_command("status")
    await update.message.reply_text(f"Server status:\n{response}")

if __name__ == '__main__':
    application = ApplicationBuilder().token("7427697633:AAFa1Zlp87rRGvuYTJ8y8heTxQ4SdNkWhkM").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", player_status))
    application.add_handler(CommandHandler("search", search_server))

    application.run_polling(allowed_updates=Update.ALL_TYPES)