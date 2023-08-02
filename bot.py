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

# Import Pycord stuff.
import discord

# Import main class.
from Rudra.rudra import Rudra


# Set intents.
only_imp_intent = discord.Intents.none()
only_imp_intent.guild_messages = True
only_imp_intent.guilds = True
discord_cache_flags = discord.MemberCacheFlags.from_intents(only_imp_intent)


# Set up the bot.
bot = Rudra(command_prefix="hhm ", intents=only_imp_intent,
            member_cache_flags=discord_cache_flags,
            owner=os.environ["OWNER_DEVANAGARI"])

bot.load_extension("Aajnaa.aajnaa_cog")


bot.run(os.environ["TOKEN_BOT"])
print("Logged out.")  # After run completes.


# End of file.
