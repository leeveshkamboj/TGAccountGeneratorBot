# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging

from uniborg import Uniborg
import api_key
import os

logging.basicConfig(level=logging.INFO)

# TOKEN = os.environ.get("TOKEN", None)
TOKEN = "1148364659:AAH5GwgPY2xEfTAZ1jnANt0VE0x1wi8Oy4M"
if TOKEN:
    borg = Uniborg('bot', bot_token=TOKEN, plugin_path="stdplugins")
    borg.run_until_disconnected()
else:
    print("Enter Token in config.")
