# Proofpoint

## Supported STIX Mappings

See the [table of mappings](proofpoint_supported_stix.md) for the STIX objects and operators supported by this connector.

### API Endpoints

REST Web Service APIs: https://help.proofpoint.com/Threat_Insight_Dashboard/API_Documentation/SIEM_API

### Format for making STIX translation calls via the CLI

`python3 main.py <translator_module> <query or result> <STIX identity object> <data>`

This example input pattern:

'python3 main.py translate "proofpoint" query '{}' "[x-proofpoint:threatstatus = 'active' AND x-proofpoint:threatstatus = 'cleared'] START t'2021-09-29T06:00:00.00Z' STOP t'2021-09-29T06:30:00.00Z'"'

will return
```
{
    "queries": [
        "threatStatus=cleared&threatStatus=activeinterval=2021-09-29T06:00:00.00Z/2021-09-29T06:30:00.00Z"
    ]
}
```
## Converting from Proofpoint events STIX

Proofpoint data to STIX mapping is defined in `to_stix_map.json`

This example Proofpoint data:

python3 main.py transmit proofpoint '{"host":"<hostname>"}' '{"auth":{"principal":"<principal>","secret":"<secret>"}}' results "threatStatus=falsePositive&threatStatus=active&threatStatus=cleared&interval=2021-10-06T09:00:00Z/2021-10-06T10:00:00Z=" 1 2

Will return the following STIX observable:
   {
    "success": true,
    "data": [
            {
            "spamScore": 0,
            "phishScore": 0,
            "threatsInfoMap": [
                {
                    "threatID": "f5faf4e8cc8617d40fa2062bc53adb476d66c90ed85ccdfad56dbf6a913617cc",
                    "threatStatus": "cleared",
                    "classification": "malware",
                    "threatUrl": "https://threatinsight.proofpoint.com/a7929edb-9295-4c75-8767-8a8ddf8a5807/threat/email/f5faf4e8cc8617d40fa2062bc53adb476d66c90ed85ccdfad56dbf6a913617cc",
                    "threatTime": "2021-09-29T07:30:46.000Z",
                    "threat": "http://theteflacademy.co.uk",
                    "campaignID": null,
                    "threatType": "url"
                }
            ],
            "messageTime": "2021-10-06T09:30:39.000Z",
            "impostorScore": 0.0,
            "malwareScore": 0,
            "cluster": "hcltechnologies_hosted",
            "subject": null,
            "quarantineFolder": null,
            "quarantineRule": null,
            "policyRoutes": [
                "default_inbound"
            ],
            "modulesRun": [
                "smtpsrv",
                "av",
                "zerohour",
                "spf",
                "dkimv",
                "sandbox",
                "banner",
                "dmarc",
                "pdr",
                "urldefense"
            ],
            "messageSize": 4305,
            "headerFrom": "header <xxx@gmail.com>",
            "headerReplyTo": null,
            "fromAddress": [
                "from@gmail.com"
            ],
            "ccAddresses": [],
            "replyToAddress": [],
            "toAddresses": [],
            "xmailer": null,
            "messageParts": [
                {
                    "disposition": "inline",
                    "sha256": "eb4f9cc9dd8e84166f4e711f0196e87063daa379f8a6a9daddef700536a887d3",
                    "md5": "98180d02ca5eb2d4646928543b53e8ae",
                    "filename": "text.txt",
                    "sandboxStatus": null,
                    "oContentType": "text/plain",
                    "contentType": "text/plain"
                },
                {
                    "disposition": "inline",
                    "sha256": "0a7f71ca3e9d1203e2857e51ae0d099b976e724828496592e86ce6fb083f7f0c",
                    "md5": "e4ad4da3a624b996a1c04a95a0e6588c",
                    "filename": "text.html",
                    "sandboxStatus": null,
                    "oContentType": "text/html",
                    "contentType": "text/html"
                }
            ],
            "completelyRewritten": true,
            "id": "5569b4b2-f0cc-eab7-bf8d-e54d5dcbcd01",
            "QID": "1969UFnu029601",
            "GUID": "ZNMbDB0FdlMIB8xRaL1ytpktHOGb9bb6",
            "sender": "xxx@gmail.com",
            "recipient": [
                "xxx@presentfortesting.com"
            ],
            "senderIP": "209.85.208.46",
            "messageID": ""
        }
        ]
        }

python3 main.py execute proofpoint proofpoint '{"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "proofpoint", "identity_class": "system"}' '{"host":"<hostname>"}' '{"auth":{"principal":"<principal>","secret":"<secret>"}}' "[x-proofpoint:threatstatus = 'active'] START t'2021-09-29T06:00:00.00Z' STOP t'2021-09-29T06:30:00.00Z'"



```json
{
    "type": "bundle",
    "id": "bundle--65b8b0e8-3e97-4749-bc42-75b98842e32b",
    "spec_version": "2.0",
    "objects": [
        {
            "id": "identity--d06281b8-b746-447b-bc22-15eaf23dee91",
            "name": "proofpoint_async",
            "type": "identity",
            "identity_class": "system",
            "created": "2021-06-29T03:27:48.694Z",
            "modified": "2021-06-29T03:27:48.694Z"
        },
        {
            "id": "observed-data--495f50ac-b43f-4e9f-952c-38c88d2b8cf9",
            "type": "observed-data",
            "created_by_ref": "identity--d06281b8-b746-447b-bc22-15eaf23dee91",
            "created": "2021-10-04T06:39:15.034Z",
            "modified": "2021-10-04T06:39:15.034Z",
            "objects": {
                "0": {
                    "type": "url",
                    "value": "https://www.mozilla.org/en-US/firefox"
                },
                "1": {
                    "type": "x-proofpoint-msgevents",
                    "userAgent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
                    "ID": "448cceab-52ce-4638-9ad2-843c9b038c7b",
                    "senderIP": "7",
                    "GUID": "IEXA9uKty7y0XtTtXfEGlXdg1pZcutRU"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "34.239.248.48"
                },
                "3": {
                    "type": "network-traffic",
                    "src_ref": "2"
                },
                "4": {
                    "type": "email-addr",
                    "value": "0100017c3019caeb-8d083606-04bf-41ff-9d24-85682bff3328-000000@amazonses.com"
                },
                "5": {
                    "type": "email-message",
                    "sender_ref": "4",
                    "to_refs": "6"
                },
                "6": {
                    "type": "email-addr",
                    "value": "xxx@abc.com"
                },
                "7": {
                    "type": "ipv4-addr",
                    "value": "54.240.11.32"
                }
            },
            "first_observed": "2021-10-04T06:39:15.034Z",
            "last_observed": "2021-10-04T06:39:15.034Z",
            "number_observed": 1
        }
    ]
}

```
