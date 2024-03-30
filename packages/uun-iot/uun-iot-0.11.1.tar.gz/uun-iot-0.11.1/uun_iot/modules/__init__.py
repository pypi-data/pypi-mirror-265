"""Initialize modules."""
import logging
from typing import Dict

from uun_iot.UuAppClient import UuAppClient

from ..events import EventRegister
from .Heartbeat import register_heartbeat
from .SocketServer import register_socketServer

# from .BaseHealthCheck import BaseHealthCheck

logger = logging.getLogger(__name__)


def init(ev: EventRegister, config: Dict, uuclient: UuAppClient):
    gconfig = config["gateway"] if "gateway" in config else config
    modules = []

    # Heartbeat
    uucmd_path_heartbeat = (
        config.get("uuApp", {}).get("uuCmdList", {}).get("gatewayHeartbeat", None)
    )
    if uucmd_path_heartbeat:
        Heartbeat = register_heartbeat(ev)

        def cmd_heartbeat(dto_in):
            uucmd = config["uuApp"]["uuCmdList"]["gatewayHeartbeat"]
            resp, exc = uuclient.post(uucmd, dto_in, log_level=logging.DEBUG)
            if exc is not None:
                return False
            return resp

        modules.append(Heartbeat(cmd_heartbeat))

    # SocketServer
    #handlers = ev.get_handlers("external", subevent=True, module=True)
    try:
        SocketServer = register_socketServer(ev)
        modules.append(SocketServer(gconfig))
        logger.info("socket server successfuly initialized")
    except ValueError as er:
        logger.info("socket server was not initialized: %s", str(er))

    return modules
