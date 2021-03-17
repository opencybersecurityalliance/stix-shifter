import requests
import os

class Auth():
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def obtainAccessToken(self):

        if(not self.apiKey):
            raise Exception("Authorizaion Failed")

        iamTokenURL = os.getenv('IAM_URL', 'https://iam.cloud.ibm.com/identity/token')
        requestBody = "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={}&response_type=cloud_iam".format(self.apiKey)

        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        try :
            response = requests.post(iamTokenURL, requestBody.replace(":", "%3A"), headers=header)
        except Exception as e:
            raise Exception("Authorizaion Failed" + str(e))

        if( response.json().get("access_token") ):
            return response.json()["access_token"]

        else:
            raise Exception("Authorizaion Failed")

    def find_location(self, accountID, host):
        if host == "":
            adminApiUrl = os.getenv('ADMIN_API_URL', 'https://compliance.cloud.ibm.com/admin/v1')
            headers = {"Authorization": "Bearer {0}".format(self.obtainAccessToken())}
            resp = requests.get("{0}/accounts/{1}/settings".format(adminApiUrl, accountID), headers=headers)
            current_location_id = resp.json()["location"]["id"]
            resp = requests.get("{0}/locations/{1}".format(adminApiUrl, current_location_id), headers=headers)
            return "{0}/v1".format(resp.json()["si_findings_endpoint_url"])
        else:
            return host
