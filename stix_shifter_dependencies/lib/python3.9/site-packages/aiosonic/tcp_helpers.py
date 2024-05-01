"""Helper methods to tune a TCP connection"""

import socket
from contextlib import suppress
from typing import Optional  # noqa

__all__ = ("tcp_keepalive", "tcp_nodelay")


if hasattr(socket, "SO_KEEPALIVE"):

    def tcp_keepalive(sock: socket.socket) -> None:
        if sock is not None:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

    def keepalive_flags() -> int:
        return socket.SOL_SOCKET | socket.SO_KEEPALIVE


else:

    def tcp_keepalive(sock: socket.socket) -> None:  # pragma: no cover
        pass

    def keepalive_flags():
        return 0


def tcp_nodelay(sock: socket.socket, value: bool) -> None:
    if sock is None:
        return

    if sock.family not in (socket.AF_INET, socket.AF_INET6):
        return

    value = bool(value)

    # socket may be closed already, on windows OSError get raised
    with suppress(OSError):
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, value)
