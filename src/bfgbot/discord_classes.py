class Discord_Handle:
    global_name: str = None
    discord_id: str = None

    def __init__(self, discord_id: str, global_name: str):
        self.discord_id = discord_id
        self.global_name = global_name
