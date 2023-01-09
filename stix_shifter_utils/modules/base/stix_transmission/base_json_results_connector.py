import time
from .base_results_connector import BaseResultsConnector

class BaseJsonResultsConnector(BaseResultsConnector):
    async def create_results_stix_connection(self, entry_point, search_id, offset, length, data_source, metadata=None):
        stats = []
        if metadata:
            result = await entry_point.create_results_connection(search_id, offset, length, metadata)
        else:
            result = await entry_point.create_results_connection(search_id, offset, length)
        metadata = None
        if 'metadata' in result:            
            metadata = result['metadata']
            del result['metadata']
        stats.append({'action': 'transmission', 'time': int(time.time()*1000)})
        if result.get('success'):
            data = result['data']
            data = data[:int(length)]
            result = await entry_point.translate_results(data_source, data)
            stats.append({'action': 'translation', 'time': int(time.time()*1000)})
        result['stats'] = stats
        if metadata:
            result['metadata'] = metadata
        return result
