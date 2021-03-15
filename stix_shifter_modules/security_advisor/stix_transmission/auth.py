import requests

class Auth():
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def obtainAccessToken(self):

        if(not self.apiKey):
            raise Exception("Authorizaion Failed")

        iamTokenURL = 'https://iam.cloud.ibm.com/identity/token'
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

    def validate_location(self, accountID, host):
        headers = {"Authorization": "Bearer {0}".format(self.obtainAccessToken())}
        resp = requests.get("https://dev.compliance.test.cloud.ibm.com/admin/v1/accounts/{0}/settings".format(accountID), headers=headers)
        current_location_id = resp.json()["location"]["id"]
        resp = requests.get("https://dev.compliance.test.cloud.ibm.com/admin/v1/locations/{0}".format(current_location_id), headers=headers)
        actual_service_url = resp.json()["si_findings_endpoint_url"]
        if "{0}/v1".format(actual_service_url) != host:
            raise ValueError("The service URL you specified is incorrect for the location selected for the account. The correct URL is: {0}/v1".format(actual_service_url))