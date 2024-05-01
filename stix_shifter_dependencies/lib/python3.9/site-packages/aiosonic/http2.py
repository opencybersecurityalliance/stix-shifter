import asyncio
from typing import TYPE_CHECKING, Awaitable, Optional

import h2.events

from aiosonic.exceptions import MissingEvent
from aiosonic.types import ParsedBodyType
from aiosonic.utils import get_debug_logger

dlogger = get_debug_logger()

if TYPE_CHECKING:
    import aiosonic
    from aiosonic.connection import Connection


class Http2Handler(object):
    def __init__(self, connection: "Connection"):
        """Initialize."""
        assert connection
        self.connection = connection
        h2conn = connection.h2conn
        assert h2conn

        loop = asyncio.get_event_loop()
        h2conn.initiate_connection()

        self.requests = {}

        # This reproduces the error in #396, by changing the header table size.
        # h2conn.update_settings({SettingsFrame.HEADER_TABLE_SIZE: 4096})
        self.writer.write(h2conn.data_to_send())
        self.reader_task = loop.create_task(self.reader_t())

    @property
    def writer(self):
        assert self.connection.writer
        return self.connection.writer

    @property
    def reader(self):
        assert self.connection.reader
        return self.connection.reader

    @property
    def h2conn(self):
        assert self.connection.h2conn
        return self.connection.h2conn

    def cleanup(self):
        """Cleanup."""
        self.reader_task.cancel()

    async def request(
        self, headers: "aiosonic.HeadersType", body: Optional[ParsedBodyType]
    ):
        from aiosonic import HttpResponse

        body = body or b""

        stream_id = self.h2conn.get_next_available_stream_id()
        headers_param = headers.items() if isinstance(headers, dict) else headers

        future: Awaitable[bytes] = asyncio.Future()
        self.requests[stream_id] = {
            "body": body,
            "headers": headers_param,
            "future": future,
            "data_sent": False,
        }
        await future
        res = self.requests[stream_id].copy()
        del self.requests[stream_id]

        response = HttpResponse()
        for key, val in res["headers"]:
            if key == b":status":
                response.response_initial = {"version": b"2", "code": val}
            else:
                response._set_header(key, val)

        if res["body"]:
            response._set_body(res["body"])

        return response

    async def reader_t(self):
        """Reader task."""
        read_size = 16 * 1024

        while True:
            data = await asyncio.wait_for(self.reader.read(read_size), 2)
            events = self.h2conn.receive_data(data)

            if events:
                dlogger.debug(("received events", events))
                try:
                    await self.handle_events(events)
                except Exception:
                    dlogger.debug("--- Some Exception!", exc_info=True)
                    raise
                else:
                    await self.check_to_write()

    async def handle_events(self, events):
        """Handle http2 events."""
        h2conn = self.h2conn

        for event in events:
            if isinstance(event, h2.events.StreamEnded):
                dlogger.debug(f"--- exit stream, id: {event.stream_id}")
                self.requests[event.stream_id]["future"].set_result(
                    self.requests[event.stream_id]["body"]
                )
            elif isinstance(event, h2.events.DataReceived):
                self.requests[event.stream_id]["body"] += event.data

                if (
                    event.stream_id in h2conn.streams
                    and not h2conn.streams[event.stream_id].closed
                    and event.flow_controlled_length
                ):
                    h2conn.increment_flow_control_window(
                        event.flow_controlled_length, event.stream_id
                    )
                dlogger.info(f"Flow increment: {event.flow_controlled_length}")
                if event.flow_controlled_length:
                    h2conn.increment_flow_control_window(event.flow_controlled_length)
            elif isinstance(event, h2.events.ResponseReceived):
                self.requests[event.stream_id]["headers"] = event.headers
            elif isinstance(event, h2.events.SettingsAcknowledged):
                for stream_id, req in self.requests.items():
                    if not req["data_sent"]:
                        await self.send_body(stream_id)
            elif isinstance(
                event,
                (
                    h2.events.WindowUpdated,
                    h2.events.PingReceived,
                    h2.events.RemoteSettingsChanged,
                ),
            ):
                pass
            else:
                raise MissingEvent(f"another event {event.__class__.__name__}")

    async def check_to_write(self):
        """Writer task."""
        h2conn = self.h2conn
        data_to_send = h2conn.data_to_send()

        if data_to_send:
            dlogger.debug(("writing data", data_to_send))
            self.writer.write(data_to_send)

    async def send_body(self, stream_id):
        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i : i + n]

        request = self.requests[stream_id]
        body = request["body"]
        headers = request["headers"]
        self.h2conn.send_headers(
            stream_id,
            headers,  # , end_stream=True if body else False
        )
        to_split = self.h2conn.local_flow_control_window(stream_id)

        for chunk in chunks(body, to_split):
            self.h2conn.send_data(stream_id, chunk)

        request["data_sent"] = True
