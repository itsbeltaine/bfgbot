import os
from bfgbot.bfg_bot import BFG_Bot
from bfgbot.bfg_bot_db_client import BFG_Bot_DB_Parameters
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")

params = BFG_Bot_DB_Parameters(
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)

client = BFG_Bot(params=params, guild=GUILD)
client.run(TOKEN)
