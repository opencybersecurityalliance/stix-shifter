import requests
import urllib.parse

class SecurityAdvisorAuth():

    def __init__(self, apiKey):
        self.apiKey = apiKey

        if( not self.apiKey ):
            raise Exception("No valid credentials found in Environment")

    def obtainAccessToken(self):
        iamTokenURL = 'https://iam.cloud.ibm.com/identity/token'
        
        requestBody = "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey="+ self.apiKey +"&response_type=cloud_iam"

        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        try :
            response = requests.post(iamTokenURL, requestBody.replace(":", "%3A")  , headers=header)
            
        except Exception as e:
            raise Exception( " Error during obtaining IAM token" + str(e) )

        if( response.json().get("access_token") ):
            return response.json()["access_token"]

        else:
            print(response.json())
            raise Exception("Not able to retrieve Access Token")