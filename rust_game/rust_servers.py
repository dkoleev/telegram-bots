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
