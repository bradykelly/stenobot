# Solaris - A Discord bot designed to make your server a safer and better place.
# Copyright (C) 2020  Ethan Henderson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Ethan Henderson
# parafoxia@carberra.xyz

import discord
from os import getenv
from typing import Final
from dotenv import load_dotenv

load_dotenv()

MAX_PREFIX_LEN = 5

MAX_MEMBER_ROLES = 3
MAX_EXCEPTION_ROLES = 3
MIN_TIMEOUT = 1
MAX_TIMEOUT = 60
MAX_GATETEXT_LEN = 250
MAX_WGTEXT_LEN = 1000
MAX_WGBOTTEXT_LEN = 500

MIN_POINTS = 5
MAX_POINTS = 99
MIN_STRIKES = 1
MAX_STRIKES = 9


class Config:
    try:
        # Load production token.
        with open(getenv("TOKEN", "")) as f:
            token = f.read()
    except FileNotFoundError:
        # Load development token.
        token = getenv("TOKEN", "")

    TOKEN: Final = token
    DEFAULT_PREFIX: Final = getenv("DEFAULT_PREFIX", "->")
    HUB_GUILD_ID: Final = int(getenv("HUB_GUILD_ID", ""))
    HUB_COMMANDS_CHANNEL_ID: Final = int(getenv("HUB_COMMANDS_CHANNEL_ID", ""))
    HUB_RELAY_CHANNEL_ID: Final = int(getenv("HUB_RELAY_CHANNEL_ID", ""))
    HUB_STDOUT_CHANNEL_ID: Final = int(getenv("HUB_STDOUT_CHANNEL_ID", ""))