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
from discord.ext import commands


@commands.command(
    name="nirikshana",
    brief="यदि भवान् सन्देशस्य विनाशाय निरिक्षणम् इच्छति ।",
    aliases=["निरिक्षण"],
    ignore_extra=True
)
@commands.guild_only()
@commands.has_permissions(manage_guild=True, manage_messages=True)
async def nirikshana(self, ctx: commands.Context) -> None:
    """To force check for messages and delete if older."""

    await ctx.send("अस्तु...")

    try:
        await self.bot.check_history_and_delete_missed()

    except Exception as e:
        await ctx.send(f"```\n{e}\n```")
        await ctx.send("👎")
        raise

    else:
        await ctx.send("👍")
# End of nirikshana().


# End of file.
