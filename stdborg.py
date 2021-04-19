# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import os


class Config(object):
    LOGGER = True
    # Get this value from my.telegram.org! Please do not steal
    TOKEN = os.environ.get("TOKEN", None)
    DB_URI = os.environ.get("DATABASE_URL", None)
    
class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True


import logging

from uniborg import Uniborg

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("TOKEN", None)
if TOKEN:
    borg = Uniborg('bot', bot_token=TOKEN, plugin_path="stdplugins")
    borg.run_until_disconnected()
else:
    print("Enter Token in config.")
