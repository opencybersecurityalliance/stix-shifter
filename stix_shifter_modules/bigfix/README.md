# BigFix

## Supported STIX Mappings

See the [table of mappings](bigfix_supported_stix.md) for the STIX objects and operators supported by this connector.


## BigFix Relevance Query with XML schema:

The actual relevance query is wrapped around by XML tag `<QueryText> query string </QueryText>` while calling the BigFix api-

```
<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="BESAPI.xsd"> 
	<ClientQuery>
	<ApplicabilityRelevance>true</ApplicabilityRelevance>
	<QueryText>( name of it | "n/a", process id of it as string | "n/a", sha256 of image file of it | "n/a", pathname of image file of it | "n/a" ) of processes</QueryText>
	<Target>
		<CustomRelevance>true</CustomRelevance>
	</Target>
	</ClientQuery>
</BESAPI>
```

## Example STIX pattern for file query:

#### STIX patterns:

  1. `[file:parent_directory_ref.path = '/root']`
  2. `[file:name LIKE '.conf' AND file:parent_directory_ref.path = '/etc']`
  3. `[file:hashes.'SHA-256' = '2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2211111111111122222222333' AND file:parent_directory_ref.path = '/root']`
  4. `[file:name = 'a' AND file:parent_directory_ref.path = '/root' OR file:hashes.'SHA-256' = '2584c4ba8b0d2a52d94023f420b7e356a1b1a3000000444446666666']`
  
  `Note: file:parent_directory_ref.path attribute will support Equality operation only.`

#### Translated relevance query(in the same order as STIX patterns):

  1. `("file", name of it | "n/a",  "sha256", sha256 of it | "n/a",  "sha1", sha1 of it | "n/a",  "md5", md5 of it | "n/a",  pathname of it | "n/a",  size of it | 0,  (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second) of files whose ((modification time of it is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND modification time of it is less than or equal to "23 Oct 2019 10:43:10 +0000" as time)) of folder "/root"`
  2. `("file", name of it | "n/a",  "sha256", sha256 of it | "n/a",  "sha1", sha1 of it | "n/a",  "md5", md5 of it | "n/a",  pathname of it | "n/a",  size of it | 0,  (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second) of files whose (((name of it as string contains ".conf" as string)) AND (modification time of it is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND modification time of it is less than or equal to "23 Oct 2019 10:43:10 +0000" as time)) of folder "/etc"`
  3. `("file", name of it | "n/a",  "sha256", sha256 of it | "n/a",  "sha1", sha1 of it | "n/a",  "md5", md5 of it | "n/a",  pathname of it | "n/a",  size of it | 0,  (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second) of files whose (((sha256 of it as string = "2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2211111111111122222222333" as string)) AND (modification time of it is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND modification time of it is less than or equal to "23 Oct 2019 10:43:10 +0000" as time)) of folder "/root"`
  4. `("file", name of it | "n/a",  "sha256", sha256 of it | "n/a",  "sha1", sha1 of it | "n/a",  "md5", md5 of it | "n/a",  pathname of it | "n/a",  size of it | 0,  (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second) of files whose (((sha256 of it as string = "2584c4ba8b0d2a52d94023f420b7e356a1b1a3000000444446666666" as string) OR (name of it as lowercase = "a" as lowercase)) AND (modification time of it is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND modification time of it is less than or equal to "23 Oct 2019 10:43:10 +0000" as time)) of folder "/root"`

## Example STIX pattern for process query:

#### STIX patterns:

  1. `[process:name LIKE 'node']`
  2. `[process:name = 'node' OR process:binary_ref.hashes.'SHA-256' = '74c4ff75e3623e64e3d6620864b69ed1d75fa460e520b88ed234234fsdfsdsdfs']`

#### Translated relevance query(in the same order as STIX patterns):

  1. `("process", name of it | "n/a",  pid of it as string | "n/a",  "sha256", sha256 of image file of it | "n/a",  "sha1", sha1 of image file of it | "n/a",  "md5", md5 of image file of it | "n/a",  pathname of image file of it | "n/a",  ppid of it as string | "n/a",  (if (windows of operating system) then  user of it as string | "n/a"  else name of user of it as string | "n/a"),  size of image file of it | 0,  (if (windows of operating system) then  (creation time of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second))  of processes whose (((name of it as string contains "node" as string)) AND (if (windows of operating system) then (creation time of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND creation time of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time) else (start time of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND start time of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time)))`
  2. `("process", name of it | "n/a",  pid of it as string | "n/a",  "sha256", sha256 of image file of it | "n/a",  "sha1", sha1 of image file of it | "n/a",  "md5", md5 of image file of it | "n/a",  pathname of image file of it | "n/a",  ppid of it as string | "n/a",  (if (windows of operating system) then  user of it as string | "n/a"  else name of user of it as string | "n/a"),  size of image file of it | 0,  (if (windows of operating system) then  (creation time of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second))  of processes whose (((sha256 of image file of it as string = "74c4ff75e3623e64e3d6620864b69ed1d75fa460e520b88ed234234fsdfsdsdfs" as string) OR (name of it as lowercase = "node" as lowercase)) AND (if (windows of operating system) then (creation time of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND creation time of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time) else (start time of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND start time of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time)))`
  
 ## Example STIX pattern for network query:

#### STIX patterns:

  1. `[ipv4-addr:value LIKE '192' AND network-traffic:src_port > 300]`

#### Translated relevance query(in the same order as STIX patterns):

  1. `("Local Address", local address of it as string | "n/a",  "Remote Address", remote address of it as string | "n/a",  "Local port", local port of it | -1,  "remote port", remote port of it | -1,  "Process name", names of processes of it,  pid of process of it as string | "n/a",  "sha256", sha256 of image files of processes of it | "n/a",  "sha1", sha1 of image files of processes of it | "n/a",  "md5", md5 of image files of processes of it | "n/a",  pathname of image files of processes of it | "n/a",  ppid of process of it as string | "n/a",  (if (windows of operating system) then  user of processes of it as string | "n/a"  else name of user of processes of it as string | "n/a"),  size of image files of processes of it | 0,  (if (windows of operating system) then  (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second),  "TCP", tcp of it, "UDP", udp of it)  of sockets whose (((local port of it is greater than 300 ) AND (local address of it as string contains "192" as string OR remote address of it as string contains "192" as string)) AND (if (windows of operating system) then (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time) else (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time))) of network`

## Example STIX pattern for mac address query:

#### STIX patterns - Network:

  1. `[mac-addr:value = '0a-65-a4-7f-ad-88' AND ipv4-addr:value = '192.168.2.3']`

#### Translated relevance query(in the same order as STIX patterns):
#### Splits into 2 queries

  1. `("Local Address", local address of it as string | "n/a",  "Remote Address", remote address of it as string | "n/a",  "Local port", local port of it | -1,  "remote port", remote port of it | -1,  "Process name", names of processes of it,  pid of process of it as string | "n/a",  "sha256", sha256 of image files of processes of it | "n/a",  "sha1", sha1 of image files of processes of it | "n/a",  "md5", md5 of image files of processes of it | "n/a",  pathname of image files of processes of it | "n/a",  ppid of process of it as string | "n/a",  (if (windows of operating system) then  user of processes of it as string | "n/a"  else name of user of processes of it as string | "n/a"),  size of image files of processes of it | 0,  (if (windows of operating system) then  (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second),  "TCP", tcp of it, "UDP", udp of it)  of sockets whose (((local address of it as string = "192.168.2.3" as string OR remote address of it as string = "192.168.2.3" as string)) AND (if (windows of operating system) then (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time) else (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time))) of network`
  2. `("Address", address of it as string | "n/a",  mac address of it as string | "n/a") of adapters whose ((mac address of it as string = "0a-65-a4-7f-ad-88" as string) AND (loopback of it = false AND address of it != "0.0.0.0")) of network`

### Translate, Transmit, Translate Result flow of a STIX pattern:
```
[ipv4-addr:value LIKE '192'] START t'2019-01-10T08:43:10.003Z' STOP t'2019-10-23T10:43:10.003Z'
```

### Translated relevance query:

```
("Local Address", local address of it as string | "n/a",  "Remote Address", remote address of it as string | "n/a",  "Local port", local port of it | -1,  "remote port", remote port of it | -1,  "Process name", names of processes of it,  pid of process of it as string | "n/a",  "sha256", sha256 of image files of processes of it | "n/a",  "sha1", sha1 of image files of processes of it | "n/a",  "md5", md5 of image files of processes of it | "n/a",  pathname of image files of processes of it | "n/a",  ppid of process of it as string | "n/a",  (if (windows of operating system) then  user of processes of it as string | "n/a"  else name of user of processes of it as string | "n/a"),  size of image files of processes of it | 0,  (if (windows of operating system) then  (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second),  "TCP", tcp of it, "UDP", udp of it)  of sockets whose (((local address of it as string contains "192" as string OR remote address of it as string contains "192" as string)) AND (if (windows of operating system) then (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2019 08:43:10 +0000" as time AND creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time) else (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2019 08:43:10 +0000" as time AND start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time))) of network
```
### As BigFix is an as-synchronous connector the above translated relevance query is passed as parameter to STIX transmission module

```
transmit
"bigfix"
"{\"host\":\"xx.xx.xx.xx\", \"port\":\"xxxxx\", \"cert_verify\":\"False\"}"
"{\"auth\":{\"username\":\"xxxxx\",\"password\":\"xxxxxx\"}}"
query
"<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true</ApplicabilityRelevance><QueryText>("Local Address", local address of it as string | "n/a",  "Remote Address", remote address of it as string | "n/a",  "Local port", local port of it | -1,  "remote port", remote port of it | -1,  "Process name", names of processes of it,  pid of process of it as string | "n/a",  "sha256", sha256 of image files of processes of it | "n/a",  "sha1", sha1 of image files of processes of it | "n/a",  "md5", md5 of image files of processes of it | "n/a",  pathname of image files of processes of it | "n/a",  ppid of process of it as string | "n/a",  (if (windows of operating system) then  user of processes of it as string | "n/a"  else name of user of processes of it as string | "n/a"),  size of image files of processes of it | 0,  (if (windows of operating system) then  (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second),  "TCP", tcp of it, "UDP", udp of it)  of sockets whose (((local address of it as string contains "192" as string OR remote address of it as string contains "192" as string)) AND (if (windows of operating system) then (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2019 08:43:10 +0000" as time AND creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time) else (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2019 08:43:10 +0000" as time AND start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time))) of network</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>"

```
### A search_id is returned which is further passed to STIX transmission result module 
```
{'search_id': '4269', 'success': True}
```
### Transmit get result
```
transmit bigfix "{\"host\":\"xx.xx.xx.xx\", \"port\":\"xxxxx\", \"cert_verify\":\"False\"}" 
{\"auth\":{\"username\":\"testapi\",\"password\":\"test123\"}} results 4269 <offset> <length> 
```
### BigFix query result (Result is formatted by STIX transmission result module):

```
[{'computer_identity': '550872812-WIN-N11M78AV7BP', 'subQueryID': 1, 'local_address': '192.168.36.10', 'local_port': '139', 'process_ppid': '0', 'process_user': 'NT AUTHORITY\\SYSTEM', 'timestamp': '1565875693', 'process_name': 'System', 'process_id': '4', 'type': 'Socket', 'protocol': 'udp', 'event_count': '1'}]
```

### STIX observable output:

```
{
    "type": "bundle",
    "id": "bundle--be2d04e1-be80-4d70-b7dd-f9723b2e9468",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "bigfix",
            "identity_class": "events"
        },
        {
            "id": "observed-data--4977301c-31de-4c1c-98ee-20f64810ffc0",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-09-16T07:17:54.300Z",
            "modified": "2019-09-16T07:17:54.300Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "192.168.36.10"
                },
                "1": {
                    "type": "network-traffic",
                    "src_ref": "0",
                    "src_port": 139,
                    "protocols": [
                        "udp"
                    ]
                },
                "2": {
                    "type": "process",
                    "pid": 0
                },
                "3": {
                    "type": "process",
                    "parent_ref": "2",
                    "creator_user_ref": "4",
                    "name": "System",
                    "pid": 4
                },
                "4": {
                    "type": "user-account",
                    "user_id": "NT AUTHORITY\\SYSTEM"
                }
            },
            "x_bigfix_relevance": {
                "computer_identity": "550872812-WIN-N11M78AV7BP"
            },
            "first_observed": "2019-08-15T13:28:13.000Z",
            "last_observed": "2019-08-15T13:28:13.000Z",
            "number_observed": 1
        }
    ]
}
```
### STIX pattern - Process:
```
[process:name = 'systemd'] START t'2019-08-01T08:43:10.003Z' STOP t'2019-08-31T10:43:10.003Z'
```

### Translated relevance query:

```
("process", name of it | "n/a",  pid of it as string | "n/a",  "sha256", sha256 of image file of it | "n/a",  "sha1", sha1 of image file of it | "n/a",  "md5", md5 of image file of it | "n/a",  pathname of image file of it | "n/a",  ppid of it as string | "n/a",  (if (windows of operating system) then  user of it as string | "n/a"  else name of user of it as string | "n/a"),  size of image file of it | 0,  (if (windows of operating system) then  (creation time of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second))  of processes whose (((name of it as lowercase = "systemd" as lowercase)) AND (if (windows of operating system) then (creation time of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "01 Aug 2019 08:43:10 +0000" as time AND creation time of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "31 Aug 2019 10:43:10 +0000" as time) else (start time of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "01 Aug 2019 08:43:10 +0000" as time AND start time of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "31 Aug 2019 10:43:10 +0000" as time)))
```
### As BigFix is an as-synchronous connector the above translated relevance query is passed as parameter to STIX transmission module

```
transmit
"bigfix"
"{\"host\":\"xx.xx.xx.xx\", \"port\":\"xxxxx\", \"cert_verify\":\"False\"}"
"{\"auth\":{\"username\":\"xxxxx\",\"password\":\"xxxxxx\"}}"
query
"<BESAPI xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"BESAPI.xsd\"><ClientQuery><ApplicabilityRelevance>true</ApplicabilityRelevance><QueryText>(\"process\", name of it | \"n/a\",  pid of it as string | \"n/a\",  \"sha256\", sha256 of image file of it | \"n/a\",  \"sha1\", sha1 of image file of it | \"n/a\",  \"md5\", md5 of image file of it | \"n/a\",  pathname of image file of it | \"n/a\",  ppid of it as string | \"n/a\",  (if (windows of operating system) then  user of it as string | \"n/a\"  else name of user of it as string | \"n/a\"),  size of image file of it | 0,  (if (windows of operating system) then  (creation time of it | \"01 Jan 1970 00:00:00 +0000\" as time -  \"01 Jan 1970 00:00:00 +0000\" as time)/second else  (start time of it | \"01 Jan 1970 00:00:00 +0000\" as time -  \"01 Jan 1970 00:00:00 +0000\" as time)/second))  of processes whose (((name of it as lowercase = \"systemd\" as lowercase)) AND (if (windows of operating system) then (creation time of it | \"01 Jan 1970 00:00:00 +0000\" as time is greater than or equal to \"01 Aug 2019 08:43:10 +0000\" as time AND creation time of it | \"01 Jan 1970 00:00:00 +0000\" as time is less than or equal to \"31 Aug 2019 10:43:10 +0000\" as time) else (start time of it | \"01 Jan 1970 00:00:00 +0000\" as time is greater than or equal to \"01 Aug 2019 08:43:10 +0000\" as time AND start time of it | \"01 Jan 1970 00:00:00 +0000\" as time is less than or equal to \"31 Aug 2019 10:43:10 +0000\" as time)))</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>"

```
### A search_id is returned which is further passed to STIX transmission result module 
```
{'search_id': '4270', 'success': True}
```
### Transmit get result
```
transmit bigfix "{\"host\":\"xx.xx.xx.xx\", \"port\":\"xxxxx\", \"cert_verify\":\"False\"}" 
{\"auth\":{\"username\":\"testapi\",\"password\":\"test123\"}} results 4270 <offset> <length> 
```

### Bigfix query result (Result is formatted by STIX transmission module):

```
[{'computer_identity': '13476923-archlinux', 'subQueryID': 1, 'sha256hash': '2f2f74f4083b95654a742a56a6c7318f3ab378c94b69009ceffc200fbc22d4d8', 'sha1hash': '0c8e8b1d4eb31e1e046fea1f1396ff85068a4c4a', 'md5hash': '148fd5f2a448b69a9f21d4c92098c4ca', 'file_path': '/usr/lib/systemd/systemd', 'process_ppid': '0', 'process_user': 'root', 'timestamp': '1565616101', 'process_name': 'systemd', 'process_id': '1', 'file_size': '1468376', 'type': 'process', 'event_count': '1'}]
```

### STIX observable output:

```
{
    "type": "bundle",
    "id": "bundle--c850ed1a-6987-40d0-b501-031d9a03b248",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "bigfix",
            "identity_class": "events"
        },
        {
            "id": "observed-data--d6ab76aa-5504-4778-ba15-686f7a50b96a",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-09-16T07:26:57.601Z",
            "modified": "2019-09-16T07:26:57.601Z",
            "objects": {
                "0": {
                    "type": "file",
                    "hashes": {
                        "SHA-256": "2f2f74f4083b95654a742a56a6c7318f3ab378c94b69009ceffc200fbc22d4d8",
                        "SHA-1": "0c8e8b1d4eb31e1e046fea1f1396ff85068a4c4a",
                        "MD5": "148fd5f2a448b69a9f21d4c92098c4ca"
                    },
                    "parent_directory_ref": "1",
                    "size": 1468376
                },
                "1": {
                    "type": "directory",
                    "path": "/usr/lib/systemd/systemd"
                },
                "2": {
                    "type": "process",
                    "binary_ref": "0",
                    "parent_ref": "3",
                    "creator_user_ref": "4",
                    "name": "systemd",
                    "pid": 1
                },
                "3": {
                    "type": "process",
                    "pid": 0
                },
                "4": {
                    "type": "user-account",
                    "user_id": "root"
                }
            },
            "x_bigfix_relevance": {
                "computer_identity": "13476923-archlinux"
            },
            "first_observed": "2019-08-12T13:21:41.000Z",
            "last_observed": "2019-08-12T13:21:41.000Z",
            "number_observed": 1
        }
    ]
}
```

## Relevance query for files:

### STIX pattern - FILE:
```
[file:parent_directory_ref.path = '/tmp']
```

### Translated relevance query:
```
("file", name of it | "n/a",  "sha256", sha256 of it | "n/a",  "sha1", sha1 of it | "n/a",  "md5", md5 of it | "n/a",  pathname of it | "n/a",  size of it | 0,  (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second) of files whose ((modification time of it is greater than or equal to "10 Jan 2019 08:43:10 +0000" as time AND modification time of it is less than or equal to "23 Oct 2019 10:43:10 +0000" as time)) of folder "/tmp"
```
### As BigFix is an as-synchronous connector the above translated relevance query is passed as parameter to STIX transmission module

```
transmit
"bigfix"
"{\"host\":\"xx.xx.xx.xx\", \"port\":\"xxxxx\", \"cert_verify\":\"False\"}"
"{\"auth\":{\"username\":\"xxxxx\",\"password\":\"xxxxxx\"}}"
query
"<BESAPI xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"BESAPI.xsd\"><ClientQuery><ApplicabilityRelevance>true</ApplicabilityRelevance><QueryText>(\"file\", name of it | \"n/a\",  \"sha256\", sha256 of it | \"n/a\",  \"sha1\", sha1 of it | \"n/a\",  \"md5\", md5 of it | \"n/a\",  pathname of it | \"n/a\",  size of it | 0,  (modification time of it - \"01 Jan 1970 00:00:00 +0000\" as time)/second) of files whose ((modification time of it is greater than or equal to \"10 Jan 2019 08:43:10 +0000\" as time AND modification time of it is less than or equal to \"23 Oct 2019 10:43:10 +0000\" as time)) of folder \"/tmp\"</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>"

```
### A search_id is returned which is further passed to STIX transmission result module 
```
{'search_id': '4272', 'success': True}
```
### Transmit get result
```
transmit bigfix "{\"host\":\"xx.xx.xx.xx\", \"port\":\"xxxxx\", \"cert_verify\":\"False\"}" 
{\"auth\":{\"username\":\"testapi\",\"password\":\"test123\"}} results 4272 <offset> <length>
```

### Bigfix query result (Result is formatted by STIX transmission module):
```
[{'computer_identity': '1626351170-xlcr.hcl.local', 'subQueryID': 1, 'sha256hash': '89698504cb73fefacd012843a5ba2e0acda7fd8d5db4efaad22f7fe54fa422f5', 'sha1hash': '41838ed7a546aeefe184fb8515973ffee7c3ba7e', 'md5hash': '958d9ba84826e48094e361102a272fd6', 'file_path': '/tmp/big42E1.tmp', 'file_name': 'big42E1.tmp', 'file_size': '770', 'type': 'file', 'timestamp': '1567046172', 'event_count': '1'}]
```

### STIX observable output:
```
{
    "type": "bundle",
    "id": "bundle--048d0ca3-ef0e-474f-9bf6-208a8c2764f5",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "bigfix",
            "identity_class": "events"
        },
        {
            "id": "observed-data--8b29cc45-d649-402c-b4fd-4b940ca63e23",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-09-16T07:36:58.784Z",
            "modified": "2019-09-16T07:36:58.784Z",
            "objects": {
                "0": {
                    "type": "file",
                    "hashes": {
                        "SHA-256": "89698504cb73fefacd012843a5ba2e0acda7fd8d5db4efaad22f7fe54fa422f5",
                        "SHA-1": "41838ed7a546aeefe184fb8515973ffee7c3ba7e",
                        "MD5": "958d9ba84826e48094e361102a272fd6"
                    },
                    "parent_directory_ref": "1",
                    "name": "big42E1.tmp",
                    "size": 770
                },
                "1": {
                    "type": "directory",
                    "path": "/tmp/big42E1.tmp"
                },
                "2": {
                    "type": "process",
                    "binary_ref": "0"
                }
            },
            "x_bigfix_relevance": {
                "computer_identity": "1626351170-xlcr.hcl.local"
            },
            "first_observed": "2019-08-29T02:36:12.000Z",
            "last_observed": "2019-08-29T02:36:12.000Z",
            "number_observed": 1
        }
    ]
}
```

### STIX pattern - MAC:
```
[mac-addr:value = '0a-ab-41-e0-89-f8']
```

### Translated relevance query:
```
("Address", address of it as string | "n/a",  mac address of it as string | "n/a") of adapters whose ((mac address of it as string = "0a-ab-41-e0-89-f8" as string) AND (loopback of it = false AND address of it != "0.0.0.0")) of network
```
### As BigFix is an as-synchronous connector the above translated relevance query is passed as parameter to STIX transmission module

```
transmit
"bigfix"
"{\"host\":\"xx.xx.xx.xx\", \"port\":\"xxxxx\", \"cert_verify\":\"False\"}"
"{\"auth\":{\"username\":\"xxxxx\",\"password\":\"xxxxxx\"}}"
query
"<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="BESAPI.xsd"><ClientQuery><ApplicabilityRelevance>true</ApplicabilityRelevance><QueryText>("Address", address of it as string | "n/a",  mac address of it as string | "n/a") of adapters whose ((mac address of it as string = "0a-ab-41-e0-89-f8" as string) AND (loopback of it = false AND address of it != "0.0.0.0")) of network</QueryText><Target><CustomRelevance>true</CustomRelevance></Target></ClientQuery></BESAPI>"

```
### A search_id is returned which is further passed to STIX transmission result module 
```
{'search_id': '4273', 'success': True}
```
### Transmit get result
```
transmit bigfix "{\"host\":\"xx.xx.xx.xx\", \"port\":\"xxxxx\", \"cert_verify\":\"False\"}" 
{\"auth\":{\"username\":\"testapi\",\"password\":\"test123\"}} results 4273 <offset> <length>
```

### Bigfix query result (Result is formatted by STIX transmission module):
```
[{'computer_identity': '541866979-suse01', 'subQueryID': 1, 'local_address': '192.168.36.110', 'mac': '0a-ab-41-e0-89-f8', 'type': 'Address', 'event_count': '1'}]
```

### STIX observable output:
```
{
    "type": "bundle",
    "id": "bundle--484d8a70-31c9-43e3-813d-1f2465d316a0",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "bigfix",
            "identity_class": "events"
        },
        {
            "id": "observed-data--6ff66e10-7391-4fcc-81dd-f8f2ee1b8926",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-09-16T07:41:32.348Z",
            "modified": "2019-09-16T07:41:32.348Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "192.168.36.110",
                    "resolves_to_refs": ["2"]
                },
                "1": {
                    "type": "network-traffic",
                    "src_ref": "0"
                },
                "2": {
                    "type": "mac-addr",
                    "value": "0a-ab-41-e0-89-f8"
                }
            },
            "x_bigfix_relevance": {
                "computer_identity": "541866979-suse01"
            },
            "number_observed": 1
        }
    ]
}

```
