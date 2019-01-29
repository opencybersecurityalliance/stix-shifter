#### Transmission - used to communicate with datasource (QRadar/Splunk). Functionalities: query <query string>, status <search id>, results <search id> <offset> <length>, ping,

Running Query in Splunk: 
```
python main.py transmit splunk '{"host": "", "port": , "cert": "-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----\n\n-----END CERTIFICATE-----"}' '{"auth": {"username": "","password": ""}}' query 'search (url = "example.com") OR ((src_mac = "00-00-5E-00-53-00") OR (dest_mac = "00-00-5E-00-53-00")) earliest="-5minutes" | head 10000| fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
```

`{'success': True, 'search_id': '1547476760.2132'}`

---------------

Getting Results for the query: 
```
python main.py transmit splunk '{"host": "", "port": , "cert": "-----BEGIN PRIVATE KEY-----\n\n-----END PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----\n\n-----END CERTIFICATE-----"}' '{"auth": {"username": "","password": ""}}' results 1547476760.2132 0 10
```

`{'success': True, 'data': [{}]}`