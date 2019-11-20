#### Transmission - used to communicate with datasource (Security Advisor). Functionalities: query <query string>, status <search id>, results <search id> <offset> <length>, ping,

Ping Security Advisor: 

```
python3 main.py transmit security_advisor  {} '{ "ibmCloudAccountID" :"", "ibmCloudApiKey" : "", "saAPIEndpoint" :"https://us-south.secadvisor.cloud.ibm.com/findings/v1/" }'  ping
```

`{'success': True}`

---------------

Running Query in Security Advisor:

```
python3 main.py transmit security_advisor  {} '{ "ibmCloudAccountID" :"", "ibmCloudApiKey" : "", "saAPIEndpoint" :"https://us-south.secadvisor.cloud.ibm.com/findings/v1/" }'  query "[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000']"
```

`{'success': True, 'search_id': "[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000']"}`

---------------

Getting Status for the query: 

```
python3 main.py transmit security_advisor  {} '{ "ibmCloudAccountID" :"", "ibmCloudApiKey" : "", "saAPIEndpoint" :"https://us-south.secadvisor.cloud.ibm.com/findings/v1/" }'  status  "[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000']"
```

`{'success': True, 'status': 'COMPLETED', 'progress': '100'}`

---------------

Getting Results for the query: 

```
python3 main.py transmit security_advisor  {} '{ "ibmCloudAccountID" :"", "ibmCloudApiKey" : "", "saAPIEndpoint" :"https://us-south.secadvisor.cloud.ibm.com/findings/v1/" }'  results  "[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000']" 0 3
```

`{'success': True, 'data': [{'author_account_id': '', 'author_email': '', 'author_id': '', 'author_kind': 'user', 'context_account_id': ' ', 'context_resource_name': 'mycluster', 'context_resource_type': 'cluster', 'create_time': '2019-10-31T11:15:55.099615Z', 'create_timestamp': 1572520555100, 'description': 'file hash and url', 'finding_next_steps_0_title': 'file hash and url', 'finding_severity': 'MEDIUM', 'id': '853092', 'insertion_timestamp': 1572520555100, 'kind': 'FINDING', 'long_description': 'http://5.188.86.29:7000', 'message': 'fdc3e15d2bc80b092f69f89329ff34b7b828be976e5cbe41e3c5720f7896c140', 'name': ' /providers/kubeHunterIBMCloudRemoteCodeExecutor/occurrences/853092', 'note_name': ' /providers/kubeHunterIBMCloudRemoteCodeExecutor/notes/kubehunteribmcloud-remote-code-execution', 'provider_id': 'kubeHunterIBMCloudRemoteCodeExecutor', 'provider_name': ' /providers/kubeHunterIBMCloudRemoteCodeExecutor', 'remediation': ' Test Remeidation', 'reported_by_id': 'kubehunteribmcloud-remote-code-execution', 'reported_by_title': 'Kubehunter IBMCloud control', 'short_description': 'Kube hunter Remote Code Executor', 'update_time': '2019-10-31T11:15:55.099635Z', 'update_timestamp': 1572520555100, 'update_week_date': '2019-W44-4'}]}`