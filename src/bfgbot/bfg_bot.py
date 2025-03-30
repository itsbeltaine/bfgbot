import discord
from bfgbot.bfg_bot_db_client import BFG_Bot_DB_Client, BFG_Bot_DB_Parameters
from bfgbot.morceaux_robots_repository import morceaux_robots_repository
from bfgbot.discord_classes import Discord_Handle
from discord.ext import commands
from typing import List


class BFG_Bot(discord.Client):

    def __init__(self, params: BFG_Bot_DB_Parameters, guild: str):
        self.guild_name = guild
        self.db_client = BFG_Bot_DB_Client(params)
        super().__init__(intents=self.getIntents())

    async def on_ready(self):
        server = discord.utils.get(self.guilds, name=self.guild_name)
        print(
            f"{self.user} has connected to Discord in the following server:\n!"
            f"{server.name}(id: {server.id})"
        )

        members = "\n - ".join([member.name for member in server.members])
        print(f"Server members: \n - {members}")

    async def on_message(self, message: discord.Message):
        if message.author == self.user or message.author.bot:
            return
        
        channelsToListenIn = ["bfg-bot"]

        if message.channel.name not in channelsToListenIn:
            return
        
        if message.content.startswith("!help"):
            await self.on_help(message)

        if message.content.startswith("!robot"):
            await self.on_robot(message)
    
    async def on_help(self, message: discord.Message):
        await message.channel.send(
"""# BFG Bot Help Manual
**!help** - Tu viens de le faire, dummy.
**!robot** - Tu donnes des morceaux de robot! 
    Ex: !robot @BFG-Bot @BFG-Bot2 3
""")

    async def on_robot(self, message: discord.Message):
        content = message.content.replace("!robot", "").strip()
        args = content.split(" ")

        morceaux = None

        for arg in args:
            try: 
                morceaux = int(arg)
            except:
                continue
        
        if morceaux is None or morceaux <= 0:
            await message.channel.send("Pas capable de savoir combien de morceaux tu veux envoyer!")

        mentions: List[str] = []
        repo = morceaux_robots_repository(self.db_client)
        for mention in message.mentions:
            if mention.bot:
                continue

            if mention.id == message.author.id:
                continue

            repo.add_morceaux_robots(
                Discord_Handle(message.author.id, message.author.global_name),
                Discord_Handle(mention.id, mention.global_name),
                morceaux,
            )
            mentions.append(f"<@{mention.id}>")

        mentions_string = ", ".join(mentions)
        await message.channel.send(f"<@{message.author.id}> a envoyé {morceaux} morceaux de robot à {mentions_string}!")

    @staticmethod
    def getIntents() -> discord.Intents:
        intents = discord.Intents.default()
        intents.members = True
        intents.guilds = True
        intents.messages = True
        intents.reactions = True
        intents.presences = True
        intents.guild_messages = True
        intents.message_content = True
        return intents
