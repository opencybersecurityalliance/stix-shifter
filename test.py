import asyncio
import sys

from stix_shifter.stix_transmission.stix_transmission import StixTransmission
from stix_shifter.stix_translation.stix_translation import StixTranslation
from downloads.datasource_config import configurations, connections


def print_log(*msg):
    print(*msg)
    pass

async def main(count):
    module_name = 'mysql' # stix_bundle mysql aws_athena aws_cloud_watch_logs
    query_data = "[ipv4-addr:value = '127.0.0.1']"
    # query_data = "[ipv4-addr:value LIKE '%'] START t'2020-05-03T08:43:10.003Z' STOP t'2021-06-29T10:43:10.003Z'"
    # query_data = "[ipv4-addr:value LIKE '%']"

    connection = connections[module_name]
    configuration = configurations[module_name]

    translation = StixTranslation() 
    transmission = StixTransmission(module_name, connection, configuration)

    # ping
    ping = await transmission.ping_async()
    print_log('Ping', ping)
    

    result = translation.translate(module=module_name, translate_type='query', options=connection['options'], data_source=module_name, data=query_data)
    print_log('Source query', result)

    if 'queries' in result:
        
        result = await transmission.query_async(result['queries'][0])
        if result.get('success'):
            search_id = result.get('search_id')
            print_log('SEARCH-ID', search_id)

            complete = False
            while not complete:
                result = await transmission.status_async(search_id)
                if result.get('success') and result.get('status') == 'COMPLETED':
                    complete = True
                if result.get('error'):
                    print('Status', result)
                    complete = True

                asyncio.sleep(2)
            
            result = await transmission.results_async(search_id, 0, 100)
            print('Results', result)

            delete = await transmission.delete_async(search_id)
            print('Delete', delete)

    print(count, "Result:", result)


async def async_call(n):
    return await asyncio.wait([main(c) for c in range(n)])

if __name__ == "__main__":
    import time
    s = time.perf_counter()

    loop = asyncio.get_event_loop() 
    loop.run_until_complete(async_call(1))

    elapsed = time.perf_counter() - s
    print(f"{elapsed:0.2f} seconds.")