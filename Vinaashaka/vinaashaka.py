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
import sys

# Import Pycord stuff.
import discord
from discord.ext import commands


class Vinaashaka():
    """Interface for deleting messages."""

    # Channel ID -> oldest and latest message ID range.
    # If the latest message's time has elapsed, the messages which are older
    # than that will also have necessarily elapsed their time.
    # Oldest message ID is saved for optimisation. We can have older pinned
    # messages, so if we fetch entire history we will have superflous messages.
    channel_msg_range = {}

    def __init__(self, message: discord.Message) -> None:
        self.message = message
    # End of __init__().

    def __del__(self) -> None:
        """
        This destructor won't make an API call to delete the message.
        The class method will take care of actual message deletion in guild.
        This just sets the IDs in the class variable for static method's use.
        """
        msg_id = self.message.id
        channel_id = self.message.channel.id
        channel_msg_range = self.__class__.channel_msg_range  # Reference.

        if channel_id in channel_msg_range:
            if channel_msg_range[channel_id]["oldest"] > msg_id:
                # We have an older message.
                channel_msg_range[channel_id]["oldest"] = msg_id
            elif channel_msg_range[channel_id]["latest"] < msg_id:
                # We have a newer message.
                channel_msg_range[channel_id]["latest"] = msg_id
        else:
            channel_msg_range[channel_id] = {
                "oldest": msg_id,
                "latest": msg_id
            }
    # End of __del__().

    @classmethod
    async def praarambha(cls, bot: commands.Bot) -> None:
        """Delete messages in the range saved in channel_msg_range."""
        for channel_id in list(cls.channel_msg_range.keys()):

            msg_range = cls.channel_msg_range[channel_id]
            after = discord.Object(msg_range["oldest"] - 1)  # Oldest inclusive
            before = discord.Object(msg_range["latest"] + 1)  # Latest msg ^.

            # Get the channel.
            channel = bot.get_channel(channel_id)
            if channel is None:
                try:
                    channel = await bot.fetch_channel(channel_id)
                except (discord.NotFound):
                    # Channel deleted / Not Found.
                    del cls.channel_msg_range[channel_id]
                    continue
                except Exception as e:
                    print((str(e) + "\n"), file=sys.stderr)
                    continue

            try:
                await channel.purge(limit=None, check=(lambda m: not m.pinned),
                                    before=before, after=after)
            except discord.NotFound:
                # Channel deleted / Not Found.
                del cls.channel_msg_range[channel_id]
            else:
                del cls.channel_msg_range[channel_id]
    # End of praarambha().
# End of Vinaashaka.


# End of file.
