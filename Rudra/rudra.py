###############################################################################

# Rudra is a Discord autodelete bot.
# Copyright (C) 2022  Gouenji Shuuya

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# The online repository may be found at <github.com/gouenji-shuuya/rudra>.

###############################################################################


# Import standard library dependencies.
from datetime import datetime
import os
import pickle
import traceback
import sys

# Import external dependencies.
from cachetools import TTLCache

# Import Pycord stuff.
import discord
from discord.ext import tasks
from discord.ext.commands import (
    Bot, Context, CommandError, CommandOnCooldown, MissingPermissions,
    UserInputError, CommandNotFound
)

# Import helper class.
from Vinaashaka.vinaashaka import Vinaashaka


class Rudra(Bot):
    """Subclassing because why not :)"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.owner = kwargs["owner"]

        # Set boot time
        self.boot_time = datetime.now()

        # Dictionary of TTL caches (Channel ID -> TTL Cache map).
        self.ttl_msg_caches = {}  # TTL caches: Objects removed after a time.

        filenames = (i for i in os.listdir("./Dattaamshanidhi")
                     if i.endswith(".pickle"))
        for filename in filenames:
            with open(f"./Dattaamshanidhi/{filename}", "rb") as file:
                setting = pickle.load(file)
                self.ttl_msg_caches[setting["channel_id"]] = TTLCache(
                    maxsize=float("inf"),
                    ttl=setting["time"],         # timestamp() gives Unix time.
                    timer=(lambda: int(datetime.now().timestamp()))
                )

        # Start the task loops.
        self.check_history_and_delete_missed.start()
        self.delete_messages.start()
    # End of __init__().

    def clear_ttl_cache(self) -> None:
        for channel_id, ttl_cache in self.ttl_msg_caches.items():
            ttl_cache.expire()
    # End of clear_ttl_cache()

    @tasks.loop(hours=6)
    async def check_history_and_delete_missed(self):
        """
        Cleanup / save messages which we missed by fetching history every 6h.
        Useful when the bot restarts.
        """
        for channel_id in list(self.ttl_msg_caches.keys()):

            # Get the channel.
            channel = self.get_channel(channel_id)
            if channel is None:
                try:
                    channel = await self.fetch_channel(channel_id)
                except (discord.NotFound, discord.Forbidden):
                    # Can't access channel.
                    continue
                except Exception:
                    continue

            ttl_cache = self.ttl_msg_caches[channel_id]
            kaala = ttl_cache.ttl

            # Check messages in channel history.
            async for msg in channel.history(limit=None, oldest_first=True):
                msg_id = msg.id

                # Ignore pinned messages or msgs already in cache.
                # This is CRITICAL, we must NOT go ahead for msgs in cache,
                # otherwise due to reassignment, the older object gets deleted
                # and thus the message will be deleted when praarambha() runs.
                # This may also result in nuking the entire channel!
                # Also, we don't want to delete pinned messages.
                if msg.pinned or msg_id in ttl_cache:
                    continue

                msg_created_at_unix = msg.created_at.timestamp()
                mortal = Vinaashaka(msg)  # Msg will die soon(tm).

                # If time already elapsed, mark for deletion.
                # Destructor of Vinaashaka will take care.
                if (datetime.now().timestamp() - msg_created_at_unix) > kaala:
                    del mortal
                    continue

                # Message is neither pinned, nor entire time is elapsed.
                # So add into the cache, but also change the expiry time.
                ttl_cache[msg_id] = mortal
                ttl_cache._TTLCache__getlink(msg_id).expires = (
                    msg_created_at_unix + kaala
                )
            # End of async iterator's for loop.
        # End of channel_id for loop.

        await self.delete_messages()  # Finally, do the cleanup.
    # End of check_history_and_delete_missed()

    @tasks.loop(seconds=15)
    async def delete_messages(self):
        """Cleanup expired messages every 15 seconds."""
        self.clear_ttl_cache()
        await Vinaashaka.praarambha(self)
    # End of delete_messages()

    async def on_ready(self) -> None:
        print("Logged in successfully as:")
        print(self.user.name)
        print(self.user.id)
        print("-" * 80)
    # End of on_ready().

    async def on_message(self, message: discord.Message) -> None:
        # Add to TTL Cache.
        if (channel_id := message.channel.id) in self.ttl_msg_caches:
            self.ttl_msg_caches[channel_id][message.id] = Vinaashaka(message)

        # If it is a command, process it. process_commands() has bot check too.
        # Must process after adding to cache, to avoid re-adding command msg to
        # cache, as it will cause deletion of object and then adding a new
        # object, which will cause deletion of message.
        await self.process_commands(message)
    # End of on_message().

    async def on_command_error(self, ctx: Context, err: CommandError) -> None:
        err_types = (CommandOnCooldown, MissingPermissions, CommandOnCooldown,
                     UserInputError, CommandNotFound)
        if not isinstance(err, err_types):
            except_str = (
                "Ignoring exception in command " + ctx.command.name + "\n\n"
                + "".join(traceback.format_exception(type(err), err,
                                                     err.__traceback__))
                + "-"*79
            )
            print(except_str, file=sys.stderr)
    # End of on_command_error().
# End of Rudra.


# End of file.
