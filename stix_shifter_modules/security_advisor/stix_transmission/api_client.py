import os

from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import RestApiClientAsync


class APIClient():
    IAM_URL = os.getenv('IAM_URL', 'https://iam.cloud.ibm.com/identity/token')
    ADMIN_API_URL = os.getenv('ADMIN_API_URL', 'https://compliance.cloud.ibm.com/admin/v1')

    
    def __init__(self, connection, configuration):
        self.auth = configuration.get("auth")
        self.apiKey = self.auth.get("apiKey")

        host_port = connection.get('host') + ':' + str(connection.get('port', ''))

        self.client_auth = RestApiClientAsync(self.IAM_URL,
            None,
            headers,
            None,
            cert_verify=connection.get('selfSignedCert', True),
            sni=connection.get('sni', None)
        )

        self.client_admin = RestApiClientAsync(host_port,
            None,
            headers,
            url_modifier_function,
            cert_verify=connection.get('selfSignedCert', True),
            sni=connection.get('sni', None)
        )

    def obtainAccessToken(self):
        if(not self.apiKey):
            raise Exception("Authorizaion Failed")
        iamTokenURL = self.IAM_URL
        requestBody = "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={}&response_type=cloud_iam".format(self.apiKey)
        header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        try :
            response = self.client_auth.call_api(iamTokenURL, '', data=requestBody.replace(":", "%3A"), headers=header)
        except Exception as e:
            raise Exception("Authorizaion Failed" + str(e))
        if( response.json().get("access_token") ):
            return response.json()["access_token"]
        else:
            raise Exception("Authorizaion Failed")


    def find_location(self, accountID, host):
        try:
            if host == "":
                adminApiUrl = self.ADMIN_API_URL
                headers = {"Authorization": "Bearer {0}".format(self.obtainAccessToken())}
                resp = requests.get("{0}/accounts/{1}/settings".format(adminApiUrl, accountID), headers=headers)
                current_location_id = resp.json()["location"]["id"]
                resp = requests.get("{0}/locations/{1}".format(adminApiUrl, current_location_id), headers=headers)
                return "{0}/si/findings/v1".format(resp.json()["main_endpoint_url"])
            else:
                return host
        except Exception as e:
            raise Exception(f"error occurred while getting location for {accountID} from ADMIN API {adminApiUrl}: {str(e)}")

    """
    Takes in accountID accessToken host time and returns all the findings in the account
    :param accountID: accountID of the user
    :type accountID: str
    :param accessToken: token passed as authorization in apiCall
    :type accessToken: str
    :param host: security_advisor findings api host
    :type host: str
    :param time: interval in which findings need to be returned if None then all the findings will be returned
    :type time: str
    :return: findings
    :rtype: dict
    """
    def get_all_occurences( params, time):

        header = {
            'Content-Type': 'application/graphql',
            'Accept': 'application/json',
            'Authorization' : 'Bearer '  + params["accessToken"],
        }

        body = '{ occurrences(kind:"FINDING") {author { accountId , id , email } name id noteName updateTime createTime shortDescription providerId providerName longDescription context {accountId region resourceType resourceName resourceId resourceCrn serviceName serviceCrn} reportedBy {id title url } finding {severity certainty networkConnection {client {address port} server {address port} direction protocol} nextSteps {title url} dataTransferred {clientBytes clientPackets serverBytes serverPackets}}}}'
        if( time ):
            body = '{ occurrences(kind:"FINDING"' + time + ') {author { accountId , id , email } name id noteName updateTime createTime shortDescription providerId providerName longDescription context {accountId region resourceType resourceName resourceId resourceCrn serviceName serviceCrn} reportedBy {id title url } finding {severity certainty networkConnection {client {address port} server {address port} direction protocol} nextSteps {title url} dataTransferred {clientBytes clientPackets serverBytes serverPackets}}}}'
        
        url = params["host"] + "/" + params["accountID"] + "/graph"
        try :
            response = requests.post(url, data= body,headers= header)

            if(response.status_code == 200):
                response = response.json()
                return response["data"]["occurrences"]
            else :
                raise Exception("Status Code in getting " + url + str(response.status_code))
        except Exception as e:
            raise Exception("Exception in getting response of " + url + str(e))