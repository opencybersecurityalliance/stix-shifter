import requests
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


