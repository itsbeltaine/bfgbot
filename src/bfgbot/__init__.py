import os
from bfgbot.bfg_bot import BFG_Bot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = BFG_Bot(GUILD)
client.run(TOKEN)