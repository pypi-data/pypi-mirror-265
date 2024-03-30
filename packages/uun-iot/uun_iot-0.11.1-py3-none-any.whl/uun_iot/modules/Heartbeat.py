import logging
from datetime import datetime
from typing import Callable, Dict, List

import psutil
import requests
from uun_iot.typing import IModule
from uun_iot.utils import get_iso_timestamp

from ..events import EventRegister

logger = logging.getLogger(__name__)


def register_heartbeat(ev: EventRegister):
    class Heartbeat(IModule):
        """
        Ping server in short periods to let server know if the gateway is online and
        send a little info about the gateway.

        Args:
            uucmd: function ``(dto_in) -> requests.Response``, the function takes
                an argument with data to be sent to the heartbeat uuCmd endpoint. It
                returns the reponse formed using :class:`requests.Response`.
        """

        id = "heartbeat"

        def __init__(self, uucmd: Callable[[Dict], requests.Response]):
            self.online = False
            self._uucmd = uucmd

        @ev.on("tick")
        def on_tick(self):
            """Determine online status and send a little information about gateway to uuApp.

            The online status is determined using ``self._uucmd`` uuCmd. The information sent includes

                - boot timestamp (in ISO timestamp)
                - CPU usage in percent
                - RAM usage in percent

            Executed on each timer tick.
            """
            boot_timestamp = datetime.fromtimestamp(psutil.boot_time())
            dto_in = {
                "bootTimestamp": get_iso_timestamp(boot_timestamp),
                "cpuUsage": psutil.cpu_percent(),
                "ramUsage": psutil.virtual_memory().percent,
            }

            response = self._uucmd(dto_in)
            if response:
                if response.status_code >= 200 and response.status_code < 300:
                    if not self.online:
                        logger.info("online")
                        self.online = True
            else:
                if self.online:
                    logger.warning("offline")
                    self.online = False

    return Heartbeat
