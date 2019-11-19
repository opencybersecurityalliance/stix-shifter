import requests

def apiCall(header, url) :
    try :
        response = requests.get(url, headers= header)
        if(response.status_code == 200):
            response = response.json()
            return(response)
        else :
            raise Exception("Status Code in getting " + url + response.status_code)
    except Exception as e:
        raise Exception("Exception in getting response of " + url + str(e))

def get_all_occurences(accountID , accessToken, host):

    header = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer '  + accessToken,
    }

    url = host  + accountID + "/providers"
    all_providers  = apiCall(header , url)
    all_providers = all_providers["providers"]

    list_provider_ids = []
    for i in range(0, len(all_providers)):
        id  = all_providers[i]["id"]
        list_provider_ids.append(id)

    all_occurences = []

    for provider in list_provider_ids:

        url = host + accountID +"/providers/" + provider + "/occurrences"
        occurences = apiCall(header, url)
        occurences = occurences["occurrences"]

        for occurence in occurences:
            all_occurences.append(occurence)

    return all_occurences

