import discord


class BFG_Bot(discord.Client):

    def __init__(self, guild):
        self.guild_name = guild
        super().__init__(intents=self.getIntents())

    async def on_ready(self):
        server = discord.utils.get(self.guilds, name=self.guild_name)
        print(
            f"{self.user} has connected to Discord in the following server:\n!"
            f"{server.name}(id: {server.id})"
        )

        members = "\n - ".join([member.name for member in server.members])
        print(f"Server members: \n - {members}")

    async def on_message(self, message):
        if message.author == self.user:
            return

        print(f"{message.channel}")
        print(f"{message}")

        channelsNameToListen = ["bot-commands"]
        if message.channel.name in channelsNameToListen:

            response = ""

            response = "thanks man"
            
            print(f"{message.author} à écrit dans #{message.channel}!")
            print(f"Lue le message suivant: {message.content}")
            if response:
                await message.channel.send(response)

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
    
