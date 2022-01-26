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
import pickle

# Import external dependencies.
from cachetools import TTLCache

# Import Pycord stuff
import discord
from discord.ext import commands


@commands.command(
    name="panjikrta",
    brief="यदि भवान् सन्देशस्य स्वविनाशम् इच्छति ।",
    aliases=["पञ्जिकृत"],
    ignore_extra=True
)
@commands.guild_only()
@commands.has_permissions(manage_guild=True, manage_messages=True)
async def panjikrta(
    self,
    ctx: commands.Context,
    channel: discord.TextChannel = None,
    msg_life_in_seconds_int: int = None
) -> None:
    """Start message autodeletion in the channel."""

    if channel is None or msg_life_in_seconds_int is None:
        await ctx.send("किम् भवान् मूर्खत्वस्य प्रदर्शनम् करोति?")
        return

    if msg_life_in_seconds_int < 60:
        await ctx.send("सन्देशस्य न्यूनतम जीवनकाल = ६० सॅकण्ड।")
        return

    if msg_life_in_seconds_int > 1209600:
        await ctx.send("सन्देशस्य अधिकतम जीवनकाल = १२०९६०० सॅकण्ड।")
        return

    self.bot.ttl_msg_caches[channel.id] = TTLCache(
        maxsize=float("inf"),
        ttl=msg_life_in_seconds_int,
        timer=(lambda: int(datetime.now().timestamp()))  # Unix time.
    )
    setting = {"channel_id": channel.id, "time": msg_life_in_seconds_int}

    with open(f"./Dattaamshanidhi/{channel.id}.pickle", "wb") as file:
        pickle.dump(setting, file)

    await ctx.send("अस्तु!")
# End of panjikrta().


# End of file.
