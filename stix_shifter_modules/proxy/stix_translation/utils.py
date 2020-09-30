import json


def unwrap_connection_options(options):
    proxy_params = options.get('proxy')
    if type(proxy_params) == str:
        if len(proxy_params):
            proxy_params = json.loads(proxy_params)
        else:
            proxy_params = {}
    return proxy_params['connection'], proxy_params['configuration']
