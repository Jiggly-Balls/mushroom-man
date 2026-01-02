from __future__ import annotations

import datetime
import logging
from typing import TYPE_CHECKING

from discord.ext import commands

from mushroom_man.backend.cache import Cache
from mushroom_man.core.meta import get_version

if TYPE_CHECKING:
    from discord import Intents


logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self, *, intents: Intents) -> None:
        super().__init__(command_prefix=[], intents=intents)
        self.version: str = get_version() or "Unkown"
        self._connected: bool = False

    async def __temp_sync(self) -> None:  # pyright:ignore[reportUnusedFunction]
        synced_global = await self.tree.sync()
        # synced_guild = await self.tree.sync(
        #     guild=discord.Object(SYNC_GUILD_ID)
        # )

        global_cmds = len(synced_global)
        # guild_cmds = len(synced_guild)
        logger.info(f"Synced {global_cmds} global commands.")
        # logger.info(f"Synced {guild_cmds} guild commands.")
        logger.warning("Comment out `Bot.__temp_sync` method call.")

    async def on_ready(self) -> None:
        Cache.last_reconnect = (
            f"<t:{round(datetime.datetime.now().timestamp())}:R>"
        )

        # await self.__temp_sync()

        if not self._connected:
            self._connected = True
            logging.info(f"Logged in as :: {self.user}")
            logging.info("Your life is meaningless.")
        else:
            logging.info("Reconnect.")
