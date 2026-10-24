from stix_shifter_utils.utils.base_entry_point import BaseEntryPoint
import asyncio


class EntryPoint(BaseEntryPoint):

    def __init__(self, connection={}, configuration={}, options={}):
        super().__init__(connection, configuration, options)
        self.set_async(True)

        if connection:
            self.setup_transmission_basic(connection, configuration)

        self.add_dialect('default', default=True)

    def get_translated_queries(self, data, query, options={}):
        # This returns the raw query, bypassing the STIX parsing
        return [query]


    async def create_results_connection(self, query, offset, length, metadata=None):
        # Wrap the async call in asyncio.run
        return await (super().create_results_connection(query, offset, length, metadata))

    async def ping_connection(self):
        # Wrap the async call in asyncio.run
        return await self.transmission.ping_connection()