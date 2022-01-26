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


# Import Pycord stuff
import discord
from discord.ext import commands


@commands.command(
    name="shreya",
    brief="यदि भवान् नरपुङ्गवाः ज्ञातुम् इच्छति ।",
    aliases=["श्रेय"],
    ignore_extra=True
)
@commands.guild_only()
async def shreya(self, ctx: commands.Context) -> None:
    """Send credits."""

    shreya = discord.Embed()
    shreya.title = "**श्रेय**"

    shreya.add_field(name="**निर्माता**", value="गॊऎञ्जी शूऽया", inline=False)
    shreya.add_field(name="**सङ्गणकस्वामी**", value="बाबा यागा", inline=False)

    link = "https://www.github.com/gouenji-shuuya/rudra"
    shreya.add_field(name="**स्रोत**",
                     value=f"[गिटहब]({link}), तन्त्रांशाज्ञापत्र: AGPLv3",
                     inline=False)

    await ctx.send(embed=shreya)
