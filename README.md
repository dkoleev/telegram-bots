# telegram-bots

To create a Telegram bot for the game *Rust*, you'll need to use the [Telegram Bot API](https://core.telegram.org/bots) and create a bot using a programming language like Python, which has good support for interacting with Telegram via libraries like `python-telegram-bot`. You can also integrate the bot with the *Rust* server to fetch data, manage users, or issue commands.

Here’s a simple step-by-step guide to help you create a basic bot:

### 1. Set up the Telegram bot

1. Go to Telegram and search for "BotFather" (the official Telegram bot for managing bots).
2. Start a chat with BotFather and send `/start`.
3. To create a new bot, send `/newbot` and follow the prompts.
4. Once the bot is created, you’ll get a **Token** that you'll need for authentication.

### 2. Set up your Python environment

If you don’t have Python installed, download and install it from [python.org](https://www.python.org/). You’ll also need the [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot) library:

```bash
pip install python-telegram-bot
```

### 3. Write the basic bot code

Here’s a simple bot that responds to the `/start` command:

```python
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Function that will be called when the /start command is used
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I am your Rust bot. What do you want to do?")

# Main function to run the bot
if __name__ == '__main__':
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN_HERE").build()

    # Add command handler
    application.add_handler(CommandHandler("start", start))

    # Start the bot
    application.run_polling()
```

### 4. Integrate with Rust

*Rust* server has RCON (Remote Console) support, which allows external programs to interact with the server. To interact with a *Rust* server, you can use the RCON protocol via the `mcrcon` library for Python.

Install it with:

```bash
pip install mcrcon
```

Here’s an example of how to send commands to a *Rust* server using RCON:

```python
from mcrcon import MCRcon

# Connect to the Rust server via RCON
def send_rcon_command(command: str):
    with MCRcon("YOUR_SERVER_IP", "YOUR_RCON_PASSWORD") as mcr:
        response = mcr.command(command)
        return response

# Example command function for checking player status
async def player_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    response = send_rcon_command("status")
    await update.message.reply_text(f"Server status:\n{response}")

# Add this new command handler to the bot
application.add_handler(CommandHandler("status", player_status))
```

### 5. Extend functionality

You can add more commands like:
- `/ban playername` – To ban a player from the server.
- `/unban playername` – To unban a player.
- `/broadcast message` – To broadcast a message to all players.

For each command, you would send the corresponding RCON command through your `send_rcon_command` function.

### 6. Run the bot

To run the bot, simply execute your Python script:

```bash
python telegram_bot.py
```

### Optional: Deploy the bot on a server
If you want your bot to be online 24/7, you can deploy it to a server (like AWS, DigitalOcean, or a VPS).

---

This is just a basic implementation. You can extend it by adding features like player statistics, automatic reminders, or game-related functionalities. Would you like help with adding specific features?

# Get servers' list
To implement a server-seeking feature for Rust in your Telegram bot, you would need to retrieve a list of available Rust servers, either from an external API or by manually adding servers to a database or file. Depending on how you want this to work, here are a few approaches:

1. Use an External API for Rust Servers
There are several APIs that provide information on public Rust servers, such as BattleMetrics or Rust Servers. These APIs can help you fetch server details and let users search for servers directly via your bot.

Here’s an example using the BattleMetrics API:

Step-by-Step Implementation:
Sign up and get an API key from the service you're using, like BattleMetrics.

Install an HTTP library to make API requests. For example, you can use requests:

bash
Copy code
pip install requests
Make an API request to fetch a list of Rust servers based on user search criteria (like location, name, etc.).

Here’s how to fetch Rust server details using Python:

python
Copy code
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Function to fetch server details from an external API
def get_rust_servers(search_term):
    url = f"https://api.battlemetrics.com/servers?filter[search]={search_term}&filter[game]=rust"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        servers = data['data']
        return servers
    else:
        return []

# Command to allow users to search for servers
async def search_server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        search_term = " ".join(context.args)  # The search term is entered by the user
        servers = get_rust_servers(search_term)

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

# Main function to run the bot
if __name__ == '__main__':
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN_HERE").build()

    # Add the /search command handler
    application.add_handler(CommandHandler("search", search_server))

    # Start the bot
    application.run_polling()
2. Manual Server List (Local Database or File)
If you want to manually add servers to the bot and allow users to search through them, you could store server information in a JSON file, a database, or even in memory (for simple use cases).

Example Using a JSON File:
json
Copy code
// servers.json
[
    {
        "name": "My Rust Server",
        "ip": "192.168.1.100",
        "port": 28015,
        "players": 35,
        "maxPlayers": 100
    },
    {
        "name": "Another Rust Server",
        "ip": "192.168.1.101",
        "port": 28016,
        "players": 50,
        "maxPlayers": 150
    }
]
Python Code:
python
Copy code
import json

# Load servers from a JSON file
def load_servers():
    with open('servers.json') as file:
        return json.load(file)

# Function to search servers by name
def search_local_servers(search_term):
    servers = load_servers()
    return [server for server in servers if search_term.lower() in server['name'].lower()]

# Command to search through local servers
async def search_server(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        search_term = " ".join(context.args)  # The search term entered by the user
        servers = search_local_servers(search_term)

        if servers:
            message = "Here are some matching servers:\n"
            for server in servers:
                name = server['name']
                players = server['players']
                max_players = server['maxPlayers']
                ip = server['ip']
                port = server['port']
                message += f"Name: {name}\nPlayers: {players}/{max_players}\nIP: {ip}:{port}\n\n"
        else:
            message = "No servers found with that name."
    else:
        message = "Please provide a search term."

    await update.message.reply_text(message)

# Add the command handler to the bot's main function
application.add_handler(CommandHandler("search", search_server))
3. Features You Can Add:
Sort servers by player count, ping, or location.
Filter servers based on criteria (PVP, modded, etc.).
Save favorite servers so users can quickly access them.
4. Run the Bot:
Run the bot as you normally would with the command:

bash
Copy code
python telegram_bot.py
With this setup, your bot will allow users to search for Rust servers either via an external API or through a local database.
