import sys

from stix_shifter.stix_transmission.stix_transmission import StixTransmission
from stix_shifter.stix_translation.stix_translation import StixTranslation
from downloads.datasource_config import configurations, connections


def print_log(*msg):
    print(*msg)
    print('\n')
    pass

def main(count):
    module_name = 'qradar' # stix_bundle, aws_athena, aws_cloud_watch_logs, qradar
    query_data = "[ipv4-addr:value = '127.0.0.1']"
    # query_data = "[ipv4-addr:value LIKE '%'] START t'2020-05-03T08:43:10.003Z' STOP t'2021-06-29T10:43:10.003Z'"
    # query_data = "[ipv4-addr:value LIKE '%']"

    connection = connections[module_name]
    configuration = configurations[module_name]

    translation = StixTranslation() 
    transmission = StixTransmission(module_name, connection, configuration)

    # ping
    ping = transmission.ping()
    print_log('Ping', ping)
    

    result = translation.translate(module=module_name, translate_type='query', options=connection['options'], data_source=module_name, data=query_data)
    print_log('Source query', result)

    if 'queries' in result:
        
        result = transmission.query(result['queries'][0])
        if result.get('success'):
            search_id = result.get('search_id')
            print_log('SEARCH-ID', search_id)

            complete = False
            while not complete:
                result =  transmission.status(search_id)
                print_log('Status', result)
                if result.get('success') and result.get('status') == 'COMPLETED':
                    complete = True
                time.sleep(2)
            
            result =  transmission.results(search_id, 0, 100)
            print_log('Results', result)

            delete =  transmission.delete(search_id)
            print_log('Delete', delete)

    print_log(count, "Result:", result)


if __name__ == "__main__":
    import time
    s = time.perf_counter()

    main(1)

    elapsed = time.perf_counter() - s
    print(f"{elapsed:0.2f} seconds.")