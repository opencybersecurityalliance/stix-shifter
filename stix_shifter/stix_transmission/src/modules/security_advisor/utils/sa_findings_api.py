import os
import requests


def getOccurnece(accountID , accessToken , providerID ,host ) :

    url = host + accountID +"/providers/" + providerID + "/occurrences"
    header = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer '  + accessToken,
    }

    try :
        r = requests.get(url,headers= header)
        if( r.status_code == 200 ):
            res = r.json()
            return(res["occurrences"])

        else :
            print("status -" + str(r.status_code))
            print("Status not 200", r.json() )
    except Exception as e :
        print("some error occured getting Occurence!!", str(e))


def getProviders(accountID , accessToken , host):

    url = host  + accountID + "/providers"
    header = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization' : 'Bearer '  + accessToken ,
    }

    try :
        r = requests.get(url,headers= header)
        if( r.status_code == 200 ):
            res = r.json()
            return(res)

        else :
            print("status -" + str(r.status_code))
            print("Status is not 200!", r.json() )
    except Exception as e :
        print("some error occured getting all Providers!!", str(e))

def get_all_occurences(accountID , accessToken, host  ):

    providers  = getProviders(accountID, accessToken , host)
    providers = providers["providers"]

    list1 = []
    for i in range(0, len(providers)):
        id  = providers[i]["id"]
        list1.append(id)

    all_occ = []

    for provider in list1:
        occ = getOccurnece( accountID, accessToken , provider, host )
        for elem in occ:
            all_occ.append(elem)

    return all_occ

