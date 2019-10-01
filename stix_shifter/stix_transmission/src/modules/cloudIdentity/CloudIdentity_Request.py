from ..utils.RestApiClient import RestApiClient
import requests, json
from . import util
from . import CloudIdentity_Token

def authUser(id, pwd, token):
    body = {
        "username": id,
        "password": pwd
    }
    print(token)
    url = util.getUri()+"/v1.0/authnmethods/password/"+util.getRegistry()
    options = {
        'uri': util.getUri()+"/v1.0/authnmethods/password/"+util.getRegistry(),
        'method': "POST",
        'json': 'true',
        'headers': { "Accept": "application/json", "Content-Type": "application/json", "authorization": "Bearer "+token},
        'body': body
    }
    

    resp = requests.post(url, json=options)
    if resp != 200:
        #refreshing token and try again
        authUser(id, pwd, CloudIdentity_Token.getToken())
    print(resp)


def getUsers(token):
    url = util.getUri()+"/v2.0/Users"

    headers = { "Accept": "application/json, text/plain, */*","authorization": "Bearer "+token}
    resp = requests.get(url, headers=headers)

    #print(json.loads(resp.text))
    json_data = resp.json()
    print(json_data)
#Last time user name logged in

def getUser(token, id=None):
    url = util.getUri()+"/v2.0/Users/" + id


    headers = { "Accept": "application/json, text/plain, */*","authorization": "Bearer "+token}
    try:
        res = requests.post(url, headers=headers)

        jsonData = res.json()
        return jsonData
    except Exception as e:
        print("failed")
        print(e)

    #print(json.loads(resp.text))
        

def postReports(token, reportName, FROM, TO, SIZE, SORT_BY, SORT_ORDER, SEARCH_AFTER = None):
    url = util.getUri() + f"/v1.0/reports/{reportName}"

    headers = { "Accept": "application/json, text/plain, */*","Content-Type": "application/json", "authorization": "Bearer "+token}
    body = {
        "FROM": FROM,
        "TO": TO,
        "SIZE": SIZE,
        "SORT_BY": SORT_BY,
        "SORT_ORDER": SORT_ORDER
    }
    if ("after" in reportName):
        body.update(SEARCH_AFTER)

    try:
        res = requests.post(url, json=body, headers=headers)

        jsonData = res.json()
        return jsonData
    except Exception as e:
        print("failed")
        print(e)

def getAdminActivity(token, FROM, TO, SIZE, SORT_BY, SORT_ORDER):
    url = util.getUri() + "/v1.0/reports/admin_activity"
    headers = { "Accept": "application/json, text/plain, */*","Content-Type": "application/json", "authorization": "Bearer "+token}
    body = json.dumps({
        "FROM": FROM,
        "TO": TO,
        "SIZE": SIZE,
        "SORT_BY": SORT_BY,
        "SORT_ORDER": SORT_ORDER
    })

    try:
        res = requests.post(url, data=body, headers=headers)

        jsonData = res.json()
        return jsonData
    except Exception as e:
        print("failed")
        print(e)

def getAuthenticatedTotalLogins(token, FROM, TO):
    url = util.getUri() + "/v1.0/reports/auth_total_logins"
    headers = { "Accept": "application/json, text/plain, */*","Content-Type": "application/json", "authorization": "Bearer "+token}
    body = json.dumps({
        "FROM": FROM,
        "TO": TO,
    })

    try:
        res = requests.post(url, data=body, headers=headers)

        jsonData = res.json()
        print(jsonData)
        return jsonData
    except Exception as e:
        print("failed")
        print(e)

def getAuthenticationTrail(token, FROM, TO, SIZE, SORT_BY, SORT_ORDER):
    url = util.getUri() + "/v1.0/reports/auth_audit_trail"
    headers = { "Accept": "application/json, text/plain, */*","Content-Type": "application/json", "authorization": "Bearer "+token}
    body = json.dumps({
        "FROM": FROM,
        "TO": TO,
        "SIZE": SIZE,
        "SORT_BY": SORT_BY,
        "SORT_ORDER": SORT_ORDER
    })

    try:
        res = requests.post(url, data=body, headers=headers)

        jsonData = res.json()
        print(jsonData)
        return jsonData
    except Exception as e:
        print("failed")
        print(e)


def getAuthFactors(token, params=None):
    url = util.getUri() + f"/v1.0/authnmethods"

    headers = { "Accept": "application/json, text/plain, */*","Content-Type": "application/json", "authorization": "Bearer "+token}

    try:
        res = requests.get(url, params=params, headers=headers)
        jsonData = res.json()
        print(jsonData)
        return jsonData
    except Exception as e:
        print("failed")
        print(e)

def getAuthMethods(token, methodType):
    url = util.getUri() + f"/v1.0/authnconfig/authnmethods/{methodType}/properties"

    headers = { "Accept": "application/json, text/plain, */*","Content-Type": "application/json", "authorization": "Bearer "+token}

    try:
        res = requests.get(url, headers=headers)
        jsonData = res.json()
        print(jsonData)
        return jsonData
    except Exception as e:
        print("failed")
        print(e)

def getAuthenticators(token, params=None):
    url = util.getUri() + f"/v1.0/authenticators"

    headers = { "Accept": "application/json, text/plain, */*","Content-Type": "application/json", "authorization": "Bearer "+token}

    try:
        res = requests.get(url, params=params, headers=headers)
        jsonData = res.json()
        print(jsonData)
        return jsonData
    except Exception as e:
        print("failed")
        print(e)