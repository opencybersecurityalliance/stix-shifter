#### Translation - used to convert queries (Stix - QRadar/Splunk) and results (Stix - QRadar/Splunk)

To Translate Query (Stix to Splunk): `python main.py translate splunk query {} "[domain-name:value = 'www.convertunits.com']"`

Translated (Splunk): 
```
{'queries': 'search (url = "www.convertunits.com") earliest="-5minutes" | head 10000 | fields src_ip,
src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol', 'parsed_stix': 
[{'attribute': 'domain-name:value', 'comparison_operator': '=', 'value': 'www.convertunits.com'}]}
```

---------------

To Translate Result (Splunk to Stix): 
```
python main.py translate "splunk" "results" '{"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "Splunk", "identity_class": "events"}' '[{"src_ip": "169.250.0.1", "src_port": "1220", "src_mac": "aa:bb:cc:dd:11:22", "dest_ip": "127.0.0.1", "dest_port": "1120", "dest_mac": "ee:dd:bb:aa:cc:11", "file_hash": "741ad92448fd12a089a13c6de49fb204e4693e1d3e9f7715471c292adf8c6bef", "user": "sname", "url": "https://wally.fireeye.com/malware_analysis/analyses?maid=1", "protocol": "tcp", "_bkt": "main~44~6D3E49A0-31FE-44C3-8373-C3AC6B1ABF06", "_cd": "44:12606114", "_indextime": "1546960685", "_raw": "Jan 08 2019 15:18:04 192.168.33.131 fenotify-2.alert: CEF:0|FireEye|MAS|6.2.0.74298|MO|malware-object|4|rt=Jan 08 2019 15:18:04 Z src=169.250.0.1 dpt=1120 dst=127.0.0.1 spt=1220 smac=AA:BB:CC:DD:11:22 dmac=EE:DD:BB:AA:CC:11 cn2Label=sid cn2=111 fileHash=41a26255d16d121dc525a6445144b895 proto=tcp request=http://qa-server.eng.fireeye.com/QE/NotificationPcaps/58.253.68.29_80-192.168.85.128_1165-2119283109_T.exe cs3Label=osinfo cs3=Microsoft Windows7 Professional 6.1 sp1 dvchost=wally dvc=10.2.101.101 cn1Label=vlan cn1=0 externalId=1 cs4Label=link cs4=https://wally.fireeye.com/malware_analysis/analyses?maid=1 cs2Label=anomaly cs2=misc-anomaly cs1Label=sname cs1=FE_UPX;Trojan.PWS.OnlineGames \n", "_serial": "0", "_si": ["splunk3-01.internal.resilientsystems.com", "main"], "_sourcetype": "fe_cef_syslog", "_time": "2019-01-08T15:18:04.00000:00", "event_count": 1}]' -x
```

Translated (Stix Results): 
```
{
    "type": "bundle",
    "id": "bundle--5b20bc1d-fc7e-479f-a067-7c9d40877436",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "Splunk",
            "identity_class": "events"
        },
        {
            "id": "observed-data--3b88587a-1413-48c4-afb8-fa74c082d6bd",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "169.250.0.1"
                },
                "1": {
                    "type": "network-traffic",
                    "src_ref": "0",
                    "src_port": 1220,
                    "dst_ref": "4",
                    "dst_port": 1120,
                    "protocols": [
                        "tcp"
                    ]
                },
                "2": {
                    "type": "network-traffic",
                    "src_port": 1220,
                    "src_ref": "3",
                    "dst_port": 1120,
                    "dst_ref": "5",
                    "protocols": [
                        "tcp"
                    ]
                },
                "3": {
                    "type": "mac-addr",
                    "value": "aa:bb:cc:dd:11:22"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "127.0.0.1"
                },
                "5": {
                    "type": "mac-addr",
                    "value": "ee:dd:bb:aa:cc:11"
                },
                "6": {
                    "type": "file",
                    "hashes": {
                        "SHA-256": "741ad92448fd12a089a13c6de49fb204e4693e1d3e9f7715471c292adf8c6bef"
                    }
                },
                "7": {
                    "type": "user-account",
                    "account_login": "sname",
                    "user_id": "sname"
                },
                "8": {
                    "type": "url",
                    "value": "https://wally.fireeye.com/malware_analysis/analyses?maid=1"
                },
                "9": {
                    "type": "domain-name",
                    "value": "wally.fireeye.com"
                },
                "10": {
                    "type": "artifact",
                    "payload_bin": "SmFuIDA4IDIwMTkgMTU6MTg6MDQgMTkyLjE2OC4zMy4xMzEgZmVub3RpZnktMi5hbGVydDogQ0VGOjB8RmlyZUV5ZXxNQVN8Ni4yLjAuNzQyOTh8TU98bWFsd2FyZS1vYmplY3R8NHxydD1KYW4gMDggMjAxOSAxNToxODowNCBaIHNyYz0xNjkuMjUwLjAuMSBkcHQ9MTEyMCBkc3Q9MTI3LjAuMC4xIHNwdD0xMjIwIHNtYWM9QUE6QkI6Q0M6REQ6MTE6MjIgZG1hYz1FRTpERDpCQjpBQTpDQzoxMSBjbjJMYWJlbD1zaWQgY24yPTExMSBmaWxlSGFzaD00MWEyNjI1NWQxNmQxMjFkYzUyNWE2NDQ1MTQ0Yjg5NSBwcm90bz10Y3AgcmVxdWVzdD1odHRwOi8vcWEtc2VydmVyLmVuZy5maXJlZXllLmNvbS9RRS9Ob3RpZmljYXRpb25QY2Fwcy81OC4yNTMuNjguMjlfODAtMTkyLjE2OC44NS4xMjhfMTE2NS0yMTE5MjgzMTA5X1QuZXhlIGNzM0xhYmVsPW9zaW5mbyBjczM9TWljcm9zb2Z0IFdpbmRvd3M3IFByb2Zlc3Npb25hbCA2LjEgc3AxIGR2Y2hvc3Q9d2FsbHkgZHZjPTEwLjIuMTAxLjEwMSBjbjFMYWJlbD12bGFuIGNuMT0wIGV4dGVybmFsSWQ9MSBjczRMYWJlbD1saW5rIGNzND1odHRwczovL3dhbGx5LmZpcmVleWUuY29tL21hbHdhcmVfYW5hbHlzaXMvYW5hbHlzZXM/bWFpZD0xIGNzMkxhYmVsPWFub21hbHkgY3MyPW1pc2MtYW5vbWFseSBjczFMYWJlbD1zbmFtZSBjczE9RkVfVVBYO1Ryb2phbi5QV1MuT25saW5lR2FtZXMgCg=="
                }
            },
            "x_splunk_spl": {
                "user": "sname"
            },
            "created": "2019-01-08T15:18:04.000Z",
            "modified": "2019-01-08T15:18:04.000Z",
            "first_observed": "2019-01-08T15:18:04.000Z",
            "last_observed": "2019-01-08T15:18:04.000Z",
            "number_observed": 1
        }
    ]
}
```