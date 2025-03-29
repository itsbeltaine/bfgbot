from bfgbot.bfg_bot_db_client import BFG_Bot_DB_Client
from bfgbot.discord_classes import Discord_Handle


class morceaux_robots_repository:

    def __init__(self, dbclient: BFG_Bot_DB_Client):
        self.db_client = dbclient

    def add_morceaux_robots(
        self, giver: Discord_Handle, receiver: Discord_Handle, morceaux: int
    ):
        self.db_client.add_morceaux_robots(giver, receiver, morceaux)
