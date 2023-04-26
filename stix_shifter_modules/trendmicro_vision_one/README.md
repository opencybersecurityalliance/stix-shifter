# Trend Micro Vision One

Trend Micro Vision One collects and correlates data across email, endpoint, servers, cloud workloads, and networks, enabling visibility and analysis that is difficult or impossible to achieve otherwise.

## Supported STIX Mappings

See the [table of mappings](trendmicro_vision_one_supported_stix.md) for the STIX objects and operators supported by this connector.

### Dialects

* endpointActivityData
* messageActivityData

### Trend Micro Vision One API Endpoints:

Ping endpoint: `https://<hostname>:<port>/v2.0/siem/events`
Result endpoint: `https://<hostname>:<port>/v2.0/xdr/search/data`

##### Reference - [Trend Micro Vision One API Documentation](https://automation.trendmicro.com/xdr/api-v2#tag/Search)

### Format for calling stix-shifter from the command line:

python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`

### Pattern expression with STIX attributes

#### STIX patterns

```shell
python main.py translate trendmicro_vision_one query '{}' "[file:name = 'svchost.exe'] START t'2020-06-17T14:20:00Z' STOP t'2020-08-18T14:30:00Z'"
```

#### Translated query

```json
{
    "queries": [
        "{\"offset\": 0, \"from\": 1592403600, \"to\": 1597761000, \"query\": \"file_name:\\\"svchost.exe\\\"\", \"source\": \"messageActivityData\"}"
    ]
}
```

#### Above translated query is passed as parameter to STIX transmission module

##### Transmit Search Call

```shell
export SS_CONNECTION='{"host":"xxx","port":443,"options":{"timeout":20}}'
export SS_AUTH='{"auth":{"token":"xxx"}}'
python main.py transmit "trendmicro_vision_one" ${SS_CONNECTION} ${SS_AUTH} query '{"query": "file:name = 'svchost.exe'", "start_time": "2020-06-17T14:20:00.000Z", "end_time": "2020-08-18T14:30:00.000Z"}'
```

#### Transmit Search Output
```json
{
    "success": true,
    "search_id": "{\"query\": \"file:name = svchost.exe\", \"start_time\": \"2020-06-17T14:20:00.000Z\", \"end_time\": \"2020-08-18T14:30:00.000Z\"}"
}
```

##### Transmit Results Call

```shell
export SS_CONNECTION='{"host":"xxx","port":443,"options":{"timeout":20}}'
export SS_AUTH='{"auth":{"token":"xxx"}}'
python main.py transmit trendmicro_vision_one ${SS_CONNECTION} ${SS_AUTH} results '{"offset":0,"fields":[],"from":1617245718,"to":1618368918,"source":"endpointActivityData","query":"hostName:*"}' 0 5
```

#### Transmit Results Output

##### endpointActivityData

```json
{
  "data": {
    "logs": [
      {
        "dpt": null,
        "dst": "",
        "endpointGuid": "35fa11da-a24e-40cf-8b56-baf8828cc15e",
        "endpointHostName": "User1",
        "endpointIp": [
          "fe80::f8e9:b28:a7a5:4b89",
          "10.10.58.51",
          "::1",
          "127.0.0.1"
        ],
        "eventTime": 1621481928000,
        "eventTimeDT": "2021-05-20T03:38:48+00:00",
        "hostName": "",
        "logonUser": [
          "sam"
        ],
        "objectCmd": "",
        "objectFileHashSha1": "",
        "objectFilePath": "c:\\users\\desktop.ini",
        "objectIp": "",
        "objectPort": null,
        "objectRegistryData": "",
        "objectRegistryKeyHandle": "",
        "objectRegistryValue": "",
        "objectSigner": null,
        "objectSignerValid": null,
        "objectUser": "",
        "parentCmd": "c:\\windows\\system32\\fodhelper.exe",
        "parentFileHashSha1": "84c1de94e002de58009973f5dd16241d286201a5",
        "parentFilePath": "c:\\windows\\system32\\fodhelper.exe",
        "processCmd": "c:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe -nop -noni -w hidden -c $x=$((gp hkcu:software\\microsoft\\windows update).update); powershell -nop -noni -w hidden -enc $x",
        "processFileHashSha1": "1b3b40fbc889fd4c645cc12c85d0805ac36ba254",
        "processFilePath": "c:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe",
        "request": "",
        "spt": null,
        "src": "",
        "srcFileHashSha1": "",
        "srcFilePath": "",
        "tags": null,
        "uuid": "229af9fa-258f-453b-9068-09db85d0d8f1",
        "searchDL": "SDL"
      }
    ],
    "total_count": 7675,
    "offset": 7674
  }
}
```

##### messageActivityData

```json
{
    "data": {
        "logs": [
            {
                "mail_message_sender": "o365mc@aaa.bbb.com",
                "mail_message_recipient": [
                    "xdrwbtest@aaa.bbb.com"
                ],
                "mail_message_subject": "Message Center Major Change Update Notification",
                "mailbox": "xdrwbtest@aaa.bbb.com",
                "mail_urls": [],
                "source_domain": "aaa.bbb.com",
                "source_ip": "207.46.55.222",
                "mail_message_delivery_time": "2021-04-13T08:30:56.000Z",
                "mail_message_id": "<89ca86fa053847de8bd45aeb658a4d36-JFBVALKQOJXWILKNK4YVA7CPGM3DKTLFONZWCZ3FINSW45D=@aaa.bbb.com>",
                "mail_unique_id": "AAkALgAAAAAAHYQDEapmECqAC-EWg0AjjRQbr_p-0W8obYXAAA",
                "mail_attachments": [],
                "mail_internet_headers": [
                    {
                        "Value": "o365mc@aaa.bbb.com",
                        "HeaderName": "Return-Path"
                    },
                    {
                        "Value": "spf=pass (sender IP is 207.46.55.222) smtp.mailfrom=aaa.bbb.com;compauth=pass reason=100",
                        "HeaderName": "Authentication-Results"
                    }
                ],
                "searchDL": "CAS",
                "eventTime": 1618302656000
            }
        ]
    }
}
```

### Trend Micro Vision One response to STIX object (STIX attributes)

#### STIX observable output

##### endpointActivityData

```json
{
    "type": "bundle",
    "id": "bundle--9a76f81f-f2d5-4d3e-92dd-5359cf77b956",
    "spec_version": "2.0",
    "objects": [
        {
            "id": "identity--b1898903-f26b-43fb-982e-4b35cb35f060",
            "name": "name",
            "type": "identity",
            "identity_class": "individual",
            "created": "2021-06-28T08:58:24.239Z",
            "modified": "2021-06-28T08:58:24.239Z"
        },
        {
            "id": "observed-data--ab261396-0c22-468b-8bfc-53becb3223fc",
            "type": "observed-data",
            "created_by_ref": "identity--b1898903-f26b-43fb-982e-4b35cb35f060",
            "created": "2021-06-28T08:58:29.505Z",
            "modified": "2021-06-28T08:58:29.505Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "10.10.58.51"
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "127.0.0.1"
                },
                "2": {
                    "type": "ipv6-addr",
                    "value": "fe80::f8e9:b28:a7a5:4b89"
                },
                "3": {
                    "type": "ipv6-addr",
                    "value": "::1"
                },
                "4": {
                    "type": "user-account",
                    "account_login": [
                        "sam"
                    ]
                },
                "5": {
                    "type": "process",
                    "command_line": "c:\\windows\\system32\\ping.exe 127.0.0.1 -n 10 ",
                    "binary_ref": "6"
                },
                "6": {
                    "type": "file",
                    "name": "ping.exe",
                    "parent_directory_ref": "7",
                    "hashes": {
                        "SHA-1": "02dba0a590629deb688b743173496ce664c535ff"
                    }
                },
                "7": {
                    "type": "directory",
                    "path": "c:\\windows\\system32"
                },
                "8": {
                    "type": "process",
                    "command_line": "c:\\windows\\system32\\cmd.exe",
                    "binary_ref": "9"
                },
                "9": {
                    "type": "file",
                    "name": "cmd.exe",
                    "parent_directory_ref": "10",
                    "hashes": {
                        "SHA-1": "3ce71813199abae99348f61f0caa34e2574f831c"
                    }
                },
                "10": {
                    "type": "directory",
                    "path": "c:\\windows\\system32"
                },
                "11": {
                    "type": "ipv4-addr",
                    "value": "127.0.0.1"
                }
            },
            "first_observed": "2021-05-18T03:56:52.801Z",
            "last_observed": "2021-05-18T03:56:52.801Z",
            "number_observed": 1
        }
    ]
}
```

##### messageActivityData

```json
{
  "type": "bundle",
  "id": "bundle--9ab37dda-9c99-48fe-91ab-be55691b0f9d",
  "spec_version": "2.0",
  "objects": [
    {
      "id": "identity--966c214b-0976-443a-8c1a-bd0684d9c9d6",
      "name": "name",
      "type": "identity",
      "identity_class": "individual",
      "created": "2021-06-28T09:11:32.022Z",
      "modified": "2021-06-28T09:11:32.022Z"
    },
    {
      "id": "observed-data--da94602d-78ca-4ac0-a52d-1ff0cb99d796",
      "type": "observed-data",
      "created_by_ref": "identity--966c214b-0976-443a-8c1a-bd0684d9c9d6",
      "created": "2021-06-28T09:11:36.775Z",
      "modified": "2021-06-28T09:11:36.775Z",
      "objects": {
        "0": {
          "type": "email-addr",
          "value": "o365mc@aaa.bbb.com"
        },
        "1": {
          "type": "email-message",
          "sender_ref": "0",
          "is_multipart": true,
          "to_refs": [
            "2"
          ],
          "subject": "Message Center Major Change Update Notification",
          "date": "2021-04-13T08:30:56.000Z",
          "additional_header_fields": {
            "Return-Path": "o365mc@aaa.bbb.com",
            "Authentication-Results": "spf=pass (sender IP is 207.46.55.222) smtp.mailfrom=aaa.bbb.com;compauth=pass reason=100",
            "Message-ID": "<89ca86fa053847de8bd45aeb658a4d36-JFBVALKQOJXWILKNK4YVA7CPGM3DKTLFONZWCZ3FINSW45D=@aaa.bbb.com>"
          }
        },
        "2": {
          "type": "email-addr",
          "value": "xdrwbtest@aaa.bbb.com"
        },
        "3": {
          "type": "domain-name",
          "value": "aaa.bbb.com"
        },
        "4": {
          "type": "ipv4-addr",
          "value": "207.46.55.222"
        },
        "5": {
          "type": "network-traffic",
          "src_ref": "4",
          "protocols": [
            "tcp"
          ]
        }
      },
      "first_observed": "2021-04-13T08:30:56.000Z",
      "last_observed": "2021-04-13T08:30:56.000Z",
      "number_observed": 1
    }
  ]
}
```

### Limitations

#### messageActivityData

* Does not support `NOT` operator.
* Does not support using `AND` and `OR` operators simultaneously.
* Does not support using multiple criteria in one field.