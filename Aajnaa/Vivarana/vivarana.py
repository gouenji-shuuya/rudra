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


# Import Pycord stuff
import discord
from discord.ext import commands


@commands.command(
    name="vivarana",
    brief="यदि भवान् साङ्ख्यिक्यः इच्छति ।",
    aliases=["विवरण"],
    ignore_extra=True
)
@commands.guild_only()
@commands.has_permissions(manage_guild=True, manage_messages=True)
async def vivarana(self, ctx: commands.Context, yn: str = None) -> None:
    """Send bot stats."""
    uptime = "जीवनकाल : " + str(datetime.now() - self.bot.boot_time)
    uptime = uptime.replace("days", "day").replace("day", "दिन")

    if yn == "y" and (await self.bot.is_owner(ctx.author)):
        get_channel = self.bot.get_channel
        fetch_channel = self.bot.fetch_channel
    else:
        get_channel = ctx.guild.get_channel
        channel_ids = set(channel.id for channel in ctx.guild.channels)

        async def fetch_channel(channel_id: int) -> discord.abc.GuildChannel:
            if channel_id not in channel_ids:
                raise ValueError("Channel not in guild.")

            return await ctx.guild.fetch_channel(channel_id)
        # End of fetch_channel()

    about_cache = ""
    for channel_id, ttl_cache in self.bot.ttl_msg_caches.items():
        if (chann := get_channel(channel_id)) is not None:
            about_cache += (f"{chann.mention} : {ttl_cache.ttl} सॅकण्ड : "
                            f"{len(ttl_cache.keys())} सन्देश\n")
        else:
            try:
                chann = await fetch_channel(channel_id)
            except ValueError:
                pass
            except Exception:
                about_cache += (f"{channel_id} : {ttl_cache.ttl} सॅकण्ड : "
                                f"{len(ttl_cache.keys())} सन्देश\n")
            else:
                about_cache += (f"{chann.mention} : {ttl_cache.ttl} सॅकण्ड : "
                                f"{len(ttl_cache.keys())} सन्देश\n")

    await ctx.send(uptime + "\n\n" + about_cache)
# End of vivarana().


# End of file.
