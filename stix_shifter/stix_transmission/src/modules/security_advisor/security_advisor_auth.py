import os
import requests


class SecurityAdvisorAuth():

    def __init__(self, apiKey):
        self.apiKey = apiKey

        if( not self.apiKey ):
            raise Exception("No valid credentials found in Environ.")

    def obtainAccessToken(self):
        iamTokenURL = 'https://iam.cloud.ibm.com/identity/token'
        
        requestBody = 'grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey&apikey=' + self.apiKey +'&response_type=cloud_iam'
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        try :
            r = requests.post(iamTokenURL, requestBody, headers=header)
        except Exception as e:
            print('Error during obtaining IAM token', str(e))
            return

        return r.json()["access_token"]