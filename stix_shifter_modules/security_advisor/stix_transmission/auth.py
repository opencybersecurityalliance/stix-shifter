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