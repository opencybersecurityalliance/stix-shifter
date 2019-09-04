# BigFix

## Supported stix pattern for file query:

BigFix module currently supports limited stix patterns for the BigFix file query. Below are some examples of supported pattern and translated relevance query:

#### Stix patterns:

  1. `[file:parent_directory_ref.path = '/root']`
  2. `[file:name LIKE '.conf' AND file:parent_directory_ref.path = '/etc']`
  3. `[file:hashes.'SHA-256' = '2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2211111111111122222222333' AND file:parent_directory_ref.path = '/root']`
  4. `[file:name = 'a' AND file:parent_directory_ref.path = '/root' OR file:hashes.'SHA-256' = '2584c4ba8b0d2a52d94023f420b7e356a1b1a3000000444446666666']`

#### Translated relevance query(in the same order as stix patterns):

  1. `("file", name of it | "n/a",  "sha256", sha256 of it | "n/a",  "sha1", sha1 of it | "n/a",  "md5", md5 of it | "n/a",  pathname of it | "n/a",  size of it | 0,  (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second) of files whose ((modification time of it is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND modification time of it is less than or equal to "23 Oct 2019 10:43:10 +0000" as time)) of folder "/root"`
  2. `("file", name of it | "n/a",  "sha256", sha256 of it | "n/a",  "sha1", sha1 of it | "n/a",  "md5", md5 of it | "n/a",  pathname of it | "n/a",  size of it | 0,  (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second) of files whose (((name of it as string contains ".conf" as string)) AND (modification time of it is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND modification time of it is less than or equal to "23 Oct 2019 10:43:10 +0000" as time)) of folder "/etc"`
  3. `("file", name of it | "n/a",  "sha256", sha256 of it | "n/a",  "sha1", sha1 of it | "n/a",  "md5", md5 of it | "n/a",  pathname of it | "n/a",  size of it | 0,  (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second) of files whose (((sha256 of it as string = "2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2211111111111122222222333" as string)) AND (modification time of it is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND modification time of it is less than or equal to "23 Oct 2019 10:43:10 +0000" as time)) of folder "/root"`
  4. `("file", name of it | "n/a",  "sha256", sha256 of it | "n/a",  "sha1", sha1 of it | "n/a",  "md5", md5 of it | "n/a",  pathname of it | "n/a",  size of it | 0,  (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second) of files whose (((sha256 of it as string = "2584c4ba8b0d2a52d94023f420b7e356a1b1a3000000444446666666" as string) OR (name of it as lowercase = "a" as lowercase)) AND (modification time of it is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND modification time of it is less than or equal to "23 Oct 2019 10:43:10 +0000" as time)) of folder "/root"`

## Supported stix pattern for process query:

BigFix module currently supports limited stix patterns for the BigFix process query. Below are some examples of supported pattern and translated relevance query:

#### Stix patterns:

  1. `[process:name LIKE 'node']`
  2. `[process:name = 'node' OR process:binary_ref.hashes.'SHA-256' = '74c4ff75e3623e64e3d6620864b69ed1d75fa460e520b88ed234234fsdfsdsdfs']`

#### Translated relevance query(in the same order as stix patterns):

  1. `("process", name of it | "n/a",  pid of it as string | "n/a",  "sha256", sha256 of image file of it | "n/a",  "sha1", sha1 of image file of it | "n/a",  "md5", md5 of image file of it | "n/a",  pathname of image file of it | "n/a",  ppid of it as string | "n/a",  (if (windows of operating system) then  user of it as string | "n/a"  else name of user of it as string | "n/a"),  size of image file of it | 0,  (if (windows of operating system) then  (creation time of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second))  of processes whose (((name of it as string contains "node" as string)) AND (if (windows of operating system) then (creation time of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND creation time of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time) else (start time of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND start time of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time)))`
  2. `("process", name of it | "n/a",  pid of it as string | "n/a",  "sha256", sha256 of image file of it | "n/a",  "sha1", sha1 of image file of it | "n/a",  "md5", md5 of image file of it | "n/a",  pathname of image file of it | "n/a",  ppid of it as string | "n/a",  (if (windows of operating system) then  user of it as string | "n/a"  else name of user of it as string | "n/a"),  size of image file of it | 0,  (if (windows of operating system) then  (creation time of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second))  of processes whose (((sha256 of image file of it as string = "74c4ff75e3623e64e3d6620864b69ed1d75fa460e520b88ed234234fsdfsdsdfs" as string) OR (name of it as lowercase = "node" as lowercase)) AND (if (windows of operating system) then (creation time of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND creation time of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time) else (start time of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND start time of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time)))`
  
 ## Supported stix pattern for network query:

BigFix module currently supports limited stix patterns for the BigFix network query. Below are some examples of supported pattern and translated relevance query:

#### Stix patterns:

  1. `[ipv4-addr:value LIKE '192' AND network-traffic:src_port > 300]`

#### Translated relevance query(in the same order as stix patterns):

  1. `("Local Address", local address of it as string | "n/a",  "Remote Address", remote address of it as string | "n/a",  "Local port", local port of it | -1,  "remote port", remote port of it | -1,  "Process name", names of processes of it,  pid of process of it as string | "n/a",  "sha256", sha256 of image files of processes of it | "n/a",  "sha1", sha1 of image files of processes of it | "n/a",  "md5", md5 of image files of processes of it | "n/a",  pathname of image files of processes of it | "n/a",  ppid of process of it as string | "n/a",  (if (windows of operating system) then  user of processes of it as string | "n/a"  else name of user of processes of it as string | "n/a"),  size of image files of processes of it | 0,  (if (windows of operating system) then  (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second),  "TCP", tcp of it, "UDP", udp of it)  of sockets whose (((local port of it is greater than 300 ) AND (local address of it as string contains "192" as string OR remote address of it as string contains "192" as string)) AND (if (windows of operating system) then (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time) else (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time))) of network`

## Supported stix pattern for network adapter query:

BigFix module currently supports limited stix pattern for the BigFix network adapter query. Below are some examples of supported pattern and translated relevance query:

#### Stix patterns:

  1. `[mac-addr:value = '0a-65-a4-7f-ad-88' AND ipv4-addr:value = '192.168.2.3']`

#### Translated relevance query(in the same order as stix patterns):
#### Splits into 2 queries

  1. `("Local Address", local address of it as string | "n/a",  "Remote Address", remote address of it as string | "n/a",  "Local port", local port of it | -1,  "remote port", remote port of it | -1,  "Process name", names of processes of it,  pid of process of it as string | "n/a",  "sha256", sha256 of image files of processes of it | "n/a",  "sha1", sha1 of image files of processes of it | "n/a",  "md5", md5 of image files of processes of it | "n/a",  pathname of image files of processes of it | "n/a",  ppid of process of it as string | "n/a",  (if (windows of operating system) then  user of processes of it as string | "n/a"  else name of user of processes of it as string | "n/a"),  size of image files of processes of it | 0,  (if (windows of operating system) then  (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second),  "TCP", tcp of it, "UDP", udp of it)  of sockets whose (((local address of it as string = "192.168.2.3" as string OR remote address of it as string = "192.168.2.3" as string)) AND (if (windows of operating system) then (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time) else (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time))) of network`
  2. `("Address", address of it as string | "n/a",  mac address of it as string | "n/a") of adapters whose ((mac address of it as string = "0a-65-a4-7f-ad-88" as string) AND (loopback of it = false AND address of it != "0.0.0.0")) of network`
## Relevance query for processes:

### Stix pattern:
```
[ipv4-addr:value LIKE = '192']
```

### Translated relevance query:

```
("Local Address", local address of it as string | "n/a",  "Remote Address", remote address of it as string | "n/a",  "Local port", local port of it | -1,  "remote port", remote port of it | -1,  "Process name", names of processes of it,  pid of process of it as string | "n/a",  "sha256", sha256 of image files of processes of it | "n/a",  "sha1", sha1 of image files of processes of it | "n/a",  "md5", md5 of image files of processes of it | "n/a",  pathname of image files of processes of it | "n/a",  ppid of process of it as string | "n/a",  (if (windows of operating system) then  user of processes of it as string | "n/a"  else name of user of processes of it as string | "n/a"),  size of image files of processes of it | 0,  (if (windows of operating system) then  (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second else  (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time -  "01 Jan 1970 00:00:00 +0000" as time)/second),  "TCP", tcp of it, "UDP", udp of it)  of sockets whose (((local address of it as string contains "192" as string OR remote address of it as string contains "192" as string)) AND (if (windows of operating system) then (creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND creation time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time) else (start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is greater than or equal to "10 Jan 2013 08:43:10 +0000" as time AND start time of process of it | "01 Jan 1970 00:00:00 +0000" as time is less than or equal to "23 Oct 2019 10:43:10 +0000" as time))) of network
```

### Bigfix query result (Result is formatted by stix transmission module):

```
[{'computer_identity': '550872812-WIN-N11M78AV7BP', 'subQueryID': 1, 'local_address': '192.168.36.10', 'local_port': '139', 'process_ppid': '0', 'process_user': 'NT AUTHORITY\\SYSTEM', 'start_time': '1565875693', 'process_name': 'System', 'process_id': '4', 'type': 'Socket', 'protocol': 'udp'}]
```

### Stix observable output:

```
 {
            "id": "observed-data--684bb4b2-6882-47ce-a593-a4771b189241",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "192.168.122.1"
                },
                "1": {
                    "type": "network-traffic",
                    "src_ref": "0",
                    "src_port": 53,
                    "protocols": [
                        "udp"
                    ]
                },
                "2": {
                    "type": "file",
                    "hashes": {
                        "SHA-256": "31e96c3cf483177865830298305e55cbd8bf7afebecc6bcba78360133cf24140",
                        "SHA-1": "2043de0a76149d0b9e5a0ee0183c077c9235c1c8",
                        "MD5": "05546846517405bcc46c4176c4ddf03a"
                    },
                    "parent_directory_ref": "3",
                    "size": 344856
                },
                "3": {
                    "type": "directory",
                    "path": "/usr/sbin/dnsmasq"
                },
                "4": {
                    "type": "process",
                    "binary_ref": "2",
                    "parent_ref": "5",
                    "creator_user_ref": "6",
                    "name": "dnsmasq",
                    "pid": 3170
                },
                "5": {
                    "type": "process",
                    "pid": 1
                },
                "6": {
                    "type": "user-account",
                    "user_id": "nobody"
                }
            },
            "name": "537366757-farpoint.hcl.local",
            "created": "2019-06-03T13:16:17.000Z",
            "first_observed": "2019-06-03T13:16:17.000Z",
            "last_observed": "2019-06-03T13:16:17.000Z"
        }
    ]
}
```
### Stix pattern:
```
[process:name = 'system']
```

### Translated relevance query:

```
( "process", name of it | "n/a", process id of it as string | "n/a", "sha256", sha256 of image file of it | "n/a", "sha1", sha1 of image file of it | "n/a", "md5", md5 of image file of it | "n/a", pathname of image file of it | "n/a", (start time of it - "01 Jan 1970 00:00:00 +0000" as time)/second ) of processes whose (name of it as lowercase = "system" as lowercase )
```

### Bigfix query result (Result is formatted by stix transmission module):

```
[{"computer_identity": "12369754-bigdata4545.canlab.ibm.com", "subQueryID": 1, "start_time": "1541424881", "type": "process", "process_name": "systemd", "process_id": "1", "sha256hash": "74c4ff75e3623e64e3d6620864b69ed1d75fa460e520b88ed234234fsdfsdsdfs", "sha1hash": "916933045c5c91ebcaa325e7f8302f3123123dfgf0000", "md5hash": "28a9beb86c4d4c31ba572805baaa777f", "file_path": "/file/path/systemd"}]
```

### Stix observable output:

```
{
    "type": "bundle",
    "id": "bundle--e50ba76e-b2e4-4afc-8c29-611d752e0d02",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "BigFix",
            "identity_class": "events"
        },
        {
            "id": "observed-data--f6f39014-7068-40b0-841f-623e8933b071",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "objects": {
                "0": {
                    "type": "process",
                    "name": "systemd",
                    "pid": "1",
                    "binary_ref": "1"
                },
                "1": {
                    "type": "file",
                    "hashes": {
                        "SHA-256": "9c74c625b2aba7a2e8d8a42e2e94715c355aaafff5556bd5404ba52b726792a6",
                        "SHA-1": "916933045c5c91ebcaa325e7f8302f3123123dfgf0000",
                        "MD5": "28a9beb86c4d4c31ba572805baaa777f"
                    },
                    "parent_directory_ref": "2"
                },
                "2": {
                    "type": "directory",
                    "path": "/file/path/systemd"
                }
            },
            "name": "1234567-test.canlab.ibm.com",
            "created": "2018-11-05T13:34:41.000Z",
            "first_observed": "2018-11-05T13:34:41.000Z",
            "last_observed": "2018-11-05T13:34:41.000Z"
        }
    ]
}
```

## Relevance query for files:

### Stix pattern:
```
[file:name = '*' AND file:parent_directory_ref.path = '/tmp']
```

### Translated relevance query:
```
("file", name of it | "n/a", "sha256", sha256 of it | "n/a", "sha1", sha1 of it | "n/a", "md5", md5 of it | "n/a", pathname of it | "n/a", (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second ) of files of folder ("/tmp")
```

### Bigfix query result (Result is formatted by stix transmission module):
```
[{"computer_identity": "12369754-bigdata4545.canlab.ibm.com", "subQueryID": 1, "type": "file", "file_name": "test_file.txt", "sha256hash": "7236f966f07259a1de3ee0d48a3ef0ee47c4a551af7f0d76dcabbbb9d6e00940", "sha1hash": "8b5e953be1db90172af66631132f6f27dda402d2", "md5hash": "e5307d27f0eb9a27af8597a1ddc51e89", "file_path": "/tmp/test_file.txt", "modified_time": "1541424894"}]
```

### Stix observable output:
```
{
    "type": "bundle",
    "id": "bundle--2b6fc06d-0869-4d0a-bac6-1bdefa5e0870",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "BigFix",
            "identity_class": "events"
        },
        {
            "id": "observed-data--fb149477-9efe-4646-a831-2d482f314b9b",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "test_file.txt",
                    "hashes": {
                        "SHA-256": "9c74c625b2aba7a2e8d8a42e2e94715c355aaafff5556bd5404ba52b726792a6",
                        "SHA-1": "916933045c5c91ebcaa325e7f8302f3123123dfgf0000",
                        "MD5": "28a9beb86c4d4c31ba572805baaa777f"
                    },
                    "parent_directory_ref": "1"
                },
                "1": {
                    "type": "directory",
                    "path": "/tmp/test_file.txt"
                },
                "2": {
                    "type": "process",
                    "binary_ref": "0"
                }
            },
            "name": "1123456-test.canlab.ibm.com",
            "modified": "2018-11-05T13:34:54.000Z",
            "first_observed": "2018-11-05T13:34:54.000Z",
            "last_observed": "2018-11-05T13:34:54.000Z"
        }
    ]
}
```

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