from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import rust_servers
import rust_remote_commands
import time

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

async def monitor_raid_events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    
    while True:
        log_data = rust_remote_commands.check_raid_events()
        raid_detected, raid_log = rust_remote_commands.is_raid_detected(log_data)
        
        if raid_detected:
            notify_user(user_id, raid_log)
        
        time.sleep(60)

def notify_user(user_id, raid_log):
    message = f"Warning! You are being raided. Raid event detected:\n{raid_log}"
    application.bot.send_message(chat_id=user_id, text=message)

if __name__ == '__main__':
    application = ApplicationBuilder().token("7427697633:AAFa1Zlp87rRGvuYTJ8y8heTxQ4SdNkWhkM").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", player_status))
    application.add_handler(CommandHandler("search", search_server))
    application.add_handler(CommandHandler("monitor raid", monitor_raid_events))

    application.run_polling(allowed_updates=Update.ALL_TYPES)