import logging
import os
import selectors
import socket
import threading
import time
from typing import Callable, Dict, Optional, Tuple

from ..events import EventRegister, TSubEvent
from .Module import Module

logger = logging.getLogger(__name__)


class SocketCmdError(Exception):
    """General exception raised when trying to execute received command."""


class InvalidMsg(SocketCmdError):
    """Received ill-formed command."""


class CommandNotRegistered(SocketCmdError):
    """Command name was not registered using @on("external")."""


class CommandFailed(SocketCmdError):
    """While executing command handler, an exception occured."""


def register_socketServer(ev: EventRegister):
    class SocketServer(Module):
        id = "socket"
        #: path to socket, a command server socket
        socket_path: str

        #: pipe used for notifying socket server to shut down
        _ping_socket_pipe: Tuple[int, int]

        #: dict with handlers associated to commands
        # _handlers: Dict[TSubEvent, Callable]

        def __init__(self, config: dict):
            super().__init__(config=config)

            self._path = None
            try:
                self._path = self._config_manager("path")
            except KeyError as e:
                raise ValueError("No path specified.") from e

            try:
                os.unlink(self._path)
            except OSError as e:
                if os.path.exists(self._path):
                    raise ValueError("Could not create socket.") from e

            # self._handlers = handlers
            self._ping_socket_pipe = os.pipe()

        @ev.on("start")
        def start(self, evs):
            """Start a socket command server."""
            if not self._path:
                return

            runev, _ = evs
            sel = selectors.DefaultSelector()

            pipe_r, _ = self._ping_socket_pipe
            # write to ping_socket_pipe_w to cause sel.select() to fire,
            # effectively aborting waiting for new connection (via accept())
            sel.register(pipe_r, selectors.EVENT_READ, lambda pipe, mask: None)

            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.bind(self._path)
            os.chmod(self._path, 0o600)
            sock.listen(1)
            sock.setblocking(False)
            sel.register(sock, selectors.EVENT_READ, self._accept_connection)
            logger.debug("Opening socket server at '%s'", self._path)

            def serve():
                with sock:
                    while runev.is_set():
                        logger.debug("Socket server: waiting...")
                        events = sel.select()
                        logger.debug("Socket server: received new event")
                        for key, mask in events:
                            callback = key.data
                            callback(key.fileobj, mask)

            threading.Thread(target=serve).start()

        @ev.on("stop")
        def stop(self):
            """Stop socket server. Clear runev first."""
            if not self._path:
                return
            _, pipe_w = self._ping_socket_pipe
            os.write(pipe_w, b"!")

        def _parse_cmd(self, msg: str) -> Optional[str]:
            """Parse and execute external command.

            Args:
                msg:  in format 'cmd_name<space>arguments'

            Raises:
                ValueError: msg is an invalid command
            """
            try:
                cmd, arg = msg.split(" ", maxsplit=1)
            except ValueError as e:
                raise InvalidMsg(
                    "A space delimiter must be present to destinguish command name"
                    " and its arguments."
                ) from e

            handlers = ev.get_handlers("external", subevent=True, module=True)
            if handlers is None or cmd not in handlers:
                raise CommandNotRegistered(f"Command '{cmd}' was not registered.")

            # currently, only a single module command origin is supported
            # for _, callback in self._handlers[cmd].items():
            callback = handlers[cmd]
            try:
                out = callback((cmd, arg))
            except Exception as e:
                logger.error(
                    "Exception occured in @external.%s for message '%s': %s",
                    cmd,
                    msg,
                    repr(e),
                )
                raise CommandFailed(repr(e)) from e

            # if isinstance(out, str):
            #    out = out.encode("utf-8")
            logger.debug("External command '%s' processed.", cmd)
            return out

        def _accept_connection(self, sock: socket.socket, mask):
            conn, _ = sock.accept()  # sock is ready to accept, this will not block
            logger.debug("A client connected to socket.")
            with conn:  # automatically closes conn
                # expected time [s] to write to socket by client, close it after timeout
                conn.settimeout(1)
                with conn.makefile(mode="rw", encoding="utf-8") as conn_file:
                    try:
                        # read a single line of input
                        line = conn_file.readline()
                        logger.debug("read '%s'", line.strip())
                        response = ""
                        try:
                            cmd_output = self._parse_cmd(line.strip("\n\r"))
                            if cmd_output is None:
                                response = "0"
                            else:
                                response = "0 " + cmd_output
                        except InvalidMsg:
                            response = "1 Invalid message!"
                        except CommandNotRegistered:
                            response = "1 Unknown command!"
                        except CommandFailed as e:
                            response = f"1 Command failed! Exception: {str(e)}"

                        try:
                            conn_file.write(response + "\n")
                            conn_file.flush()
                            logger.debug("Written: '%s'", response)
                        except BrokenPipeError:
                            logger.info(
                                "Error while writing to socket. The receiver maybe was"
                                " not waiting for response?"
                            )

                    except TimeoutError:
                        logger.debug(
                            "Socket connection from client accepted but no command was"
                            " written or could not deliver command output. Did you"
                            " forget to end the command with a newline?"
                        )

    return SocketServer
