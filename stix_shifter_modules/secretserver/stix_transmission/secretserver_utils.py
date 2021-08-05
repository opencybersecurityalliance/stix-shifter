import json
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
import requests


class SecretServerApiClient(object):

    def __init__(self,url):
        self.auth_token_url = url

    def get_events(self):
        payload = "{\"name\": \"Secret Server Events Logs\", \"parameters\": [{\"name\": \"startDate\", \"value\": '%s'} , {\"name\":\"endDate\",\"value\": '%s'}]}" %(
        self.startDate, self.endDate)
        headers = {

            'Authorization': self.accessToken,
            'Content-Type': 'application/json'
        }
        print("Fetching the event details")
        endpoint = "SecretServer/api/v1/reports/execute"
        response = RestApiClient.call_api(self, endpoint, 'POST', headers=headers, data=payload, urldata=None,
                                          timeout=None)
        if response.code == 403:
            print("Your password has expired. Please login to change it.")
            print("Unable to fetch the records")
            exit(0)
        collection=[]
        json_data = response.response.text
        eventData = json.loads(json_data)
        col = eventData['columns']
        for obj in eventData['rows']:
            obj = dict(zip(col, obj))
            collection.append(obj)
        return collection


    def get_Secret(self):
        eventDetail = SecretServerApiClient.get_events(self)
        secretIdList = []
        secretCollection = []
        for obj in eventDetail:
            item=(obj['ItemId'])
            secretIdList.append(item)
        unique=set(secretIdList)
        for id in unique:
            secret_server_user_url = self.secret_detail + "/%s" % id
            headers = {
                'Authorization': self.accessToken,
                'Content-Type': 'application/json'
            }
            payload = {}
            response = RestApiClient.call_api(self, secret_server_user_url, 'GET', headers=headers, data=payload, urldata=None,
                                                  timeout=None)

            secretCollection.append(response.response.text)
        json_data = json.dumps(secretCollection)
        collection = json.loads(json_data)
        return collection

    def get_response(self):
        eventDetail = SecretServerApiClient.get_events(self)
        secretDetail = SecretServerApiClient.get_Secret(self)
        updateSecret = []
        secretCollection = {}
        updateCollection = []
        for obj in secretDetail:
            next = json.loads(obj)
            updateSecret.append(next)
        for item in eventDetail:
            for getId in updateSecret:
                if (item['ItemId'] == getId['id']):
                    data = getId['items']
                    for secret in data:
                        if (secret['fieldName'] == 'Server'):
                            secretCollection[str(secret['fieldName'])] = str(secret['itemValue'])
                            item.update(secretCollection)
                            updateCollection.append(item)
        return updateCollection
