import asyncio

from stix_shifter_utils.utils.error_response import ErrorResponder

def run_in_thread(callable, *args, **kwargs):
    loop = None
    connector = 'unsupplied connector name'
    if kwargs:
        connector = kwargs.get('connector', None)
        if connector and isinstance(connector, str):
            kwargs.pop('connector')

    try:
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        return loop.run_until_complete(callable(*args, **kwargs))
    
    except Exception as ex:
        return_obj = dict()
        ErrorResponder.fill_error(return_obj, error=ex, connector=connector)
        return return_obj