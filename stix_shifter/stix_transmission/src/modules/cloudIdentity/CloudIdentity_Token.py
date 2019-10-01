from . import util
from ..utils.RestApiClient import RestApiClient
import requests, json


def getToken():
    options = {
        'uri': util.getUri()+"/v2.0/endpoint/default/token",
        'client_id': util.getid(),
        'client_secret': util.getSecret(),
        'grant_type': "client_credentials"
    }
    resp = requests.post(util.getUri()+"/v2.0/endpoint/default/token", data=options)
    json_data = json.loads(resp.text)
    print(json_data)
    token = json_data['access_token']
    return token

    