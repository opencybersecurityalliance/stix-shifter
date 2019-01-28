# BigFix

## Supported stix pattern for file query:

BigFix module currently supports limited stix patterns for the big file query. Below are some examples of supported pattern and translated relevance query:

#### Stix patterns:

  1. `[file:parent_directory_ref.path = '/root' AND file:name = '*']`
  2. `[file:name Like 'arbitrary_file_name.txt' AND file:parent_directory_ref.path = '/etc']`
  3. `[file:hashes.'SHA-256' = '2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2211111111111122222222333' AND file:parent_directory_ref.path = '/root']`
  4. `[file:name = 'a' AND file:parent_directory_ref.path = '/root' OR file:hashes.'SHA-256' = '2584c4ba8b0d2a52d94023f420b7e356a1b1a3000000444446666666']`

#### Translated relevance query(in the same order as stix patterns):

  1. `("file", name of it | "n/a", "sha256", sha256 of it | "n/a", "sha1", sha1 of it | "n/a", "md5", md5 of it | "n/a", pathname of it | "n/a", (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second ) of files of folder ("/root")`
  2. `("file", name of it | "n/a", "sha256", sha256 of it | "n/a", "sha1", sha1 of it | "n/a", "md5", md5 of it | "n/a", pathname of it | "n/a", (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second ) of files whose (name of it as lowercase = "arbitrary_file_name.txt" as lowercase) of folder ("/etc")`
  3. `("file", name of it | "n/a", "sha256", sha256 of it | "n/a", "sha1", sha1 of it | "n/a", "md5", md5 of it | "n/a", pathname of it | "n/a", (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second ) of files whose (sha256 of it as lowercase = "2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2211111111111122222222333" as lowercase) of folder ("/root")`
  4. `("file", name of it | "n/a", "sha256", sha256 of it | "n/a", "sha1", sha1 of it | "n/a", "md5", md5 of it | "n/a", pathname of it | "n/a", (modification time of it - "01 Jan 1970 00:00:00 +0000" as time)/second ) of files whose (name of it as lowercase = "a" as lowercase OR sha256 of it as lowercase = "2584c4ba8b0d2a52d94023f420b7e356a1b1a3000000444446666666" as lowercase) of folder ("/root")`

## Supported stix pattern for process query:

BigFix module currently supports limited stix patterns for the big process query. Below are some examples of supported pattern and translated relevance query:

#### Stix patterns:

  1. `[process:name = '*']`
  2. `[process:name Like 'node']`
  3. `[process:name = 'node' or file:hashes.'SHA-256' = '74c4ff75e3623e64e3d6620864b69ed1d75fa460e520b88ed234234fsdfsdsdfs']`
  4. `[process:name = 'node' AND file:hashes.'SHA-256' = '0c0017201b82e1d8613513dc80d1bf46320a957c393bsdfsdf3423432456546w']`

#### Translated relevance query(in the same order as stix patterns):

  1. `( "process", name of it | "n/a", process id of it as string | "n/a", "sha256", sha256 of image file of it | "n/a", "sha1", sha1 of image file of it | "n/a", "md5", md5 of image fileof it | "n/a", pathname of image file of it | "n/a", (start time of it - "01 Jan 1970 00:00:00 +0000" as time)/second ) of processes`
  2. `( "process", name of it | "n/a", process id of it as string | "n/a", "sha256", sha256 of image file of it | "n/a", "sha1", sha1 of image file of it | "n/a", "md5", md5 of image fileof it | "n/a", pathname of image file of it | "n/a", (start time of it - "01 Jan 1970 00:00:00 +0000" as time)/second ) of processes whose (name of it as lowercase contains "node" as lowercase )`
  3. `( "process", name of it | "n/a", process id of it as string | "n/a", "sha256", sha256 of image file of it | "n/a", "sha1", sha1 of image file of it | "n/a", "md5", md5 of image fileof it | "n/a", pathname of image file of it | "n/a", (start time of it - "01 Jan 1970 00:00:00 +0000" as time)/second ) of processes whose (name of it as lowercase = "node" as lowercase OR sha256 of image file of it as lowercase = "74c4ff75e3623e64e3d6620864b69ed1d75fa460e520b88ed234234fsdfsdsdfs" as lowercase )`
  4. `( "process", name of it | "n/a", process id of it as string | "n/a", "sha256", sha256 of image file of it | "n/a", "sha1", sha1 of image file of it | "n/a", "md5", md5 of image fileof it | "n/a", pathname of image file of it | "n/a", (start time of it - "01 Jan 1970 00:00:00 +0000" as time)/second ) of processes whose (name of it as lowercase = "node" as lowercase AND sha256 of image file of it as lowercase = "0c0017201b82e1d8613513dc80d1bf46320a957c393bsdfsdf3423432456546w" as lowercase )`

## Relevance query for processes:

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

[{"computer_identity": "12369754-bigdata4545.canlab.ibm.com", "subQueryID": 1, "type": "file", "file_name": "test_file.txt", "sha256hash": "7236f966f07259a1de3ee0d48a3ef0ee47c4a551af7f0d76dcabbbb9d6e00940", "sha1hash": "8b5e953be1db90172af66631132f6f27dda402d2", "md5hash": "e5307d27f0eb9a27af8597a1ddc51e89", "file_path": "/tmp/test_file.txt", "modified_time": "1541424894"}]

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