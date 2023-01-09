from .base_connector import BaseConnector
import time


class BaseJsonConnector(BaseConnector):

    async def create_results_stix_connection(self, entry_point, search_id, offset, length, data_source, metadata=None):
        stats = []
        if metadata:
            result = await entry_point.create_results_connection(search_id, offset, length, metadata)
        else:
            result = await entry_point.create_results_connection(search_id, offset, length)
        stats.append({'action': 'transmission', 'time': int(time.time()*1000)})
        metadata = None
        if 'metadata' in result:            
            metadata = result['metadata']
            del result['metadata']
        if result.get('success'):
            data = result['data']
            data = data[:length]
            result = await entry_point.translate_results(data_source, data)
            stats.append({'action': 'translation', 'time': int(time.time()*1000)})
        result['stats'] = stats
        if metadata:
            result['metadata'] = metadata
        return result
