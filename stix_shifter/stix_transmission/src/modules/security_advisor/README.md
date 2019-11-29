#### Transmission - used to communicate with datasource (Security Advisor). Functionalities: query <query string>, status <search id>, results <search id> <offset> <length>, ping,

Ping Security Advisor:

```
python3 main.py transmit security_advisor '{"host" :"https://us-south.secadvisor.cloud.ibm.com/findings/v1"}' '{"auth": { "accountID" :"<ACCOUNT ID>" ,"apiKey" : "<API KEY>" }}' ping
```

`{'success': True}`

---

Running Query in Security Advisor:

```
python3 main.py transmit security_advisor '{"host" :"https://us-south.secadvisor.cloud.ibm.com/findings/v1"}' '{"auth": { "accountID" :"<ACCOUNT ID>" ,"apiKey" : "<API KEY>" }}' query "[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z'"
```

`{'success': True, 'search_id': "[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z'"}`

---

Getting Status for the query:

```
python3 main.py transmit security_advisor '{"host" :"https://us-south.secadvisor.cloud.ibm.com/findings/v1"}' '{"auth": { "accountID" :"<ACCOUNT ID>" ,"apiKey" : "<API KEY>" }}' status "[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z'"
```

`{'success': True, 'status': 'COMPLETED', 'progress': '100'}`

---

Getting Results for the query:

```
python3 main.py transmit security_advisor  '{"host" :"https://us-south.secadvisor.cloud.ibm.com/findings/v1"}' '{"auth": { "accountID" :"<ACCOUNT ID>" ,"apiKey" : "<API KEY>" }}' results "[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z'" 0 3
```

`{'success': True, 'data': [{'author_accountId': ' ', 'author_id': 'test_id', 'author_email': ' test@gmail.com', 'name': ' /providers/kubeHunterIBMCloudRemoteCodeExecutor/occurrences/853092', 'id': '853092', 'noteName': ' /providers/kubeHunterIBMCloudRemoteCodeExecutor/notes/kubehunteribmcloud-remote-code-execution', 'updateTime': '2019-10-31T11:15:55.099635Z', 'createTime': '2019-10-31T11:15:55.099615Z', 'shortDescription': 'Kube hunter Remote Code Executor', 'providerId': 'kubeHunterIBMCloudRemoteCodeExecutor', 'providerName': ' /providers/kubeHunterIBMCloudRemoteCodeExecutor', 'longDescription': 'http://5.188.86.29:7000', 'context_accountId': ' ', 'context_resourceName': 'mycluster', 'reportedBy_id': 'kubehunteribmcloud-remote-code-execution', 'reportedBy_title': 'Kubehunter IBMCloud control', 'finding_severity': 'MEDIUM', 'finding_certainty': 'HIGH', 'occurence_count': 1}, {'author_accountId': ' ', 'author_id': 'test_id', 'author_email': ' test@gmail.com', 'name': ' /providers/kubeHunterIBMCloudRemoteCodeExecutor/occurrences/853089', 'id': '853089', 'noteName': ' /providers/kubeHunterIBMCloudRemoteCodeExecutor/notes/kubehunteribmcloud-remote-code-execution', 'updateTime': '2019-10-31T11:11:17.679043Z', 'createTime': '2019-10-31T11:11:17.679013Z', 'shortDescription': 'Kube hunter Remote Code Executor', 'providerId': 'kubeHunterIBMCloudRemoteCodeExecutor', 'providerName': ' /providers/kubeHunterIBMCloudRemoteCodeExecutor', 'longDescription': 'http://5.45.69.149:7000', 'context_accountId': ' ', 'context_resourceName': 'mycluster', 'reportedBy_id': 'kubehunteribmcloud-remote-code-execution', 'reportedBy_title': 'Kubehunter IBMCloud control', 'finding_severity': 'LOW', 'finding_certainty': 'HIGH', 'occurence_count': 1}]}`
