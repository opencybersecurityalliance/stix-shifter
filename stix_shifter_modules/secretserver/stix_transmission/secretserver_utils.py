import json

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
        response = requests.request("POST", self.event_url, headers=headers, data=payload)
        if response.status_code == 403:
            print("Your password has expired. Please login to change it.")
            print("Unable to fetch the records")
            exit(0)
        json_data = response.text
        data = json.loads(json_data)
        collection = []
        updateResponse = {}
        userCollection = {}
        field = data['columns']
        print("Fetching the user details")
        for obj in data['rows']:
            obj = dict(zip(field, obj))
            updateResponse.update(obj)
            id = obj['ItemId']
            secret_server_user_urlr=self.user_detail+"/%s"%id
            payload = {}
            response = requests.request("GET", secret_server_user_urlr, headers=headers, data=payload)
            userDetails = json.loads(response.text)
            userData = userDetails['items']
            for item in userData:
                if (item['fieldName'] == 'Server'):
                    userCollection[str(item['fieldName'])] = str(item['itemValue'])

            updateResponse.update(userCollection)
            collection.append(updateResponse)

        json_data = json.dumps(collection)
        resp = json.loads(json_data)
        return resp







