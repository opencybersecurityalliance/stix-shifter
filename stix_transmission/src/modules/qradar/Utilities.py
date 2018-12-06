import sys
import json


# This function prints out the response from an endpoint in a consistent way.
def pretty_print_response(response):
    print(response.code)
    parsed_response = json.loads(response.read().decode('utf-8'))
    print(json.dumps(parsed_response, indent=4))
    return


# this function prints out information about a request that will be made
# to the API.
def pretty_print_request(client, path, method, headers=None):
    ip = client.get_server_ip()
    base_uri = client.get_base_uri()

    header_copy = client.get_headers().copy()
    if headers is not None:
        header_copy.update(headers)

    url = 'https://' + ip + base_uri + path
    print('Sending a ' + method + ' request to:')
    print(url)
    print('with these headers:')
    print(header_copy)
    print()


# this function sets up data to be used by a sample. If the data already exists
# it prefers to use the existing data.
def data_setup(client, path, method, params=[]):
    response = client.call_api(path, method, params=params)
    if (response.code == 409):
        print("Data already exists, using existing data")
    elif(response.code >= 400):
        print("An error occurred setting up sample data:")
        pretty_print_response(response)
        sys.exit(1)
    return response