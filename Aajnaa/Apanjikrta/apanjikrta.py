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
import os

# Import Pycord stuff
import discord
from discord.ext import commands


@commands.command(
    name="apanjikrta",
    brief="यदि भवान् सन्देशस्य स्वविनाशम् न इच्छति ।",
    aliases=["अपञ्जिकृत"],
    ignore_extra=True
)
@commands.guild_only()
@commands.has_permissions(manage_guild=True, manage_messages=True)
async def apanjikrta(
    self,
    ctx: commands.Context,
    channel: discord.TextChannel = None
) -> None:
    """Stop message autodeletion in the channel."""

    if channel is None or channel.id not in self.bot.ttl_msg_caches:
        await ctx.send("किम् भवान् मूर्खत्वस्य प्रदर्शनम् करोति?")
        return

    del self.bot.ttl_msg_caches[channel.id]

    try:
        os.remove(f"./Data/{channel.id}.pickle")
    except FileNotFoundError:
        pass

    await ctx.send("अस्तु।")
# End of apanjikrta().


# End of file.
