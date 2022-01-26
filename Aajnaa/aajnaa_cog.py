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

# Import all commands
from .Apanjikrta.apanjikrta import apanjikrta
from .Nirikshana.nirikshana import nirikshana
from .Panjikrta.panjikrta import panjikrta
from .Shreya.shreya import shreya
from .Vivarana.vivarana import vivarana


class Aajnaa(commands.Cog):
    """आज्ञा सूची"""

    # Initialise the cog class.
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    # End of __init__()

    # Bring functions in class scope by way of assignment.
    register = panjikrta
    deregister = apanjikrta
    inspection = nirikshana
    about = vivarana
    credits = shreya
# End of Aajnaa class.


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Aajnaa(bot))
# End of setup.


# End of file.
