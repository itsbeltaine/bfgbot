from bfgbot.discord_classes import Discord_Handle


class user_totals:
    discord_handle: Discord_Handle
    total: int
    total_given: int
    total_received: int

    def __init__(
        self,
        discord_handle: Discord_Handle,
        total: int,
        total_given: int,
        total_received: int,
    ):
        self.discord_handle = discord_handle
        self.total = total
        self.total_given = total_given
        self.total_received = total_received
