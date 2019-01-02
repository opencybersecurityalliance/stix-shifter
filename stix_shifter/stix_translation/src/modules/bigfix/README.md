# BigFix

## Supported stix pattern for file query:

BigFix module currently supports limited stix patterns for the big file query. Below are some examples of supported pattern and translated relevance query:

#### Stix patterns:

  1. `[file:parent_directory_ref.path = '/root' AND file:name = '*']`
  2. `[file:name Like 'arbitrary_file_name.txt' AND file:parent_directory_ref.path = '/etc']`
  3. `[file:hashes.sha256 = '2584c4ba8b0d2a52d94023f420b7e356a1b1a3f2211111111111122222222333' AND file:parent_directory_ref.path = '/root']`
  4. `[file:name = 'a' AND file:parent_directory_ref.path = '/root' OR file:hashes.sha256 = '2584c4ba8b0d2a52d94023f420b7e356a1b1a3000000444446666666']`

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
  3. `[process:name = 'node' or file:hashes.sha256 = '74c4ff75e3623e64e3d6620864b69ed1d75fa460e520b88ed234234fsdfsdsdfs']`
  4. `[process:name = 'node' AND file:hashes.sha256 = '0c0017201b82e1d8613513dc80d1bf46320a957c393bsdfsdf3423432456546w']`

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

### Bigfix query result:

```
{'success': True, 'data': [{"computerID": 111222333, "computerName": "DESKTOP-TEST", "subQueryID": 1, "isFailure": True, "result": "The operator 'start time' is not defined.", "ResponseTime": 1000}, {"computerID": 111555222, "computerName": "1111.canlab.ibm.com", "subQueryID": 1, "isFailure": False, "result": "process, systemd, 1, sha256, 9c74c625b2aba7a2e8d8a42e2e94715c355367f7cbfa9bd5404baaaaaaaaxxxvvv, sha1, 916933045c5c91ebcaa325e7f8302f3a777aaaa, md5, 28a9beb86c4d4c31bcdf2805bea112244, /file/path/systemd, 1541424881", "ResponseTime": 6000}, {"computerID": 111222444, "computerName": "canlab.ibm.com", "subQueryID": 1, "isFailure": False, "result": "process, systemd-test2, 583, sha256, 6718ca93ac89be647b8faf70d8db98a2257f1adfc10adasfasf234234hh25d79b5f, sha1, b8124a45cb6efb6eb0e79deaab2d755c6aaavvvbbb1, md5, 9f1475e503bfdc1f473d72c888aa1111, /file/path/systemd-test2, 1541424886", "ResponseTime": 6000}]}
```

### Stix observable output:

```
{
    "type": "bundle",
    "id": "bundle--f6c3d2ec-dd40-4732-aaa3-b6647ebb6b71",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "BigFix",
            "identity_class": "events"
        },
        {
            "id": "observed-data--7436f8c5-8e5a-421b-8fd2-be460dd60802",
            "type": "observed-data",
            "name": "111555222-1111.canlab.ibm.com",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
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
                        "SHA-256": "9c74c625b2aba7a2e8d8a42e2e94715c355367f7cbfa9bd5404baaaaaaaaxxxvvv",
                        "SHA-1": "916933045c5c91ebcaa325e7f8302f3a777aaaa",
                        "MD5": "28a9beb86c4d4c31bcdf2805bea112244"
                    },
                    "parent_directory_ref": "2"
                },
                "2": {
                    "type": "directory",
                    "path": "/file/path/systemd"
                }
            },
            "created": "2018-11-05T13:34:41.000Z"
        },
        {
            "id": "observed-data--4065c9fd-f94b-421c-afa6-71ae991ddc77",
            "type": "observed-data",
            "name": "111222444-canlab.ibm.com",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "objects": {
                "0": {
                    "type": "process",
                    "name": "systemd-test2",
                    "pid": "583",
                    "binary_ref": "1"
                },
                "1": {
                    "type": "file",
                    "hashes": {
                        "SHA-256": "6718ca93ac89be647b8faf70d8db98a2257f1adfc10adasfasf234234hh25d79b5f",
                        "SHA-1": "b8124a45cb6efb6eb0e79deaab2d755c6aaavvvbbb1",
                        "MD5": "9f1475e503bfdc1f473d72c888aa1111"
                    },
                    "parent_directory_ref": "2"
                },
                "2": {
                    "type": "directory",
                    "path": "/file/path/systemd-test2"
                }
            },
            "created": "2018-11-05T13:34:46.000Z"
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
### Bigfix query result:

```
{'success': True, 'data': }[{"computerID": 121111, "computerName": "DESKTOP-TEST", "subQueryID": 1, "isFailure": True, "result": "Singular expression refers to nonexistent object.", "ResponseTime": 1000}, {"computerID": 222333555, "computerName": "1122.canlab.ibm.com", "subQueryID": 1, "isFailure": False, "result": "file, test_file1, sha256, 7236f966f07259a1de3ee0d48a222222222444444d76dcabbbb9d6e00940, sha1, 8b5e953be1db90172af66631132f6f27dda402d2, md5, e5307d27f0eb11112222333331ddc51e89, /tmp/test_file1, 1541424894", "ResponseTime": 5000}, {"computerID": 444555666, "computerName": "33445.canlab.ibm.com", "subQueryID": 1, "isFailure": False, "result": "file, test_file2, sha256, 80f0be6226a036ade711111112222213ed1a2ef02ed4c1d2424247025d6351529, sha1, 468ffec645354007f155555666c4a3c5c16ac65, md5, 8d683d83c1bcfa95a66666777774f52c, /tmp/test_file2, 1544528864", "ResponseTime": 5000}]}
```

### Stix observable output:
```
{
    "type": "bundle",
    "id": "bundle--316f370d-aa27-4c66-b7dc-62cb2e053ba3",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "BigFix",
            "identity_class": "events"
        },
        {
            "id": "observed-data--58a09e1a-8f1b-497a-8222-91c572a64370",
            "type": "observed-data",
            "name": "222333555-1122.canlab.ibm.com",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "test_file1",
                    "hashes": {
                        "SHA-256": "7236f966f07259a1de3ee0d48a222222222444444d76dcabbbb9d6e00940",
                        "SHA-1": "8b5e953be1db90172af66631132f6f27dda402d2",
                        "MD5": "e5307d27f0eb11112222333331ddc51e89"
                    },
                    "parent_directory_ref": "1"
                },
                "1": {
                    "type": "directory",
                    "path": "/tmp/test_file1"
                },
                "2": {
                    "type": "process",
                    "binary_ref": "0"
                }
            },
            "modified": "2018-11-05T13:34:54.000Z"
        },
        {
            "id": "observed-data--1ac2e1fa-6dce-42e0-a5e2-86dee75c590e",
            "type": "observed-data",
            "name": "444555666-33445.canlab.ibm.com",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "test_file2",
                    "hashes": {
                        "SHA-256": "80f0be6226a036ade711111112222213ed1a2ef02ed4c1d2424247025d6351529",
                        "SHA-1": "468ffec645354007f155555666c4a3c5c16ac65",
                        "MD5": "8d683d83c1bcfa95a66666777774f52c"
                    },
                    "parent_directory_ref": "1"
                },
                "1": {
                    "type": "directory",
                    "path": "/tmp/test_file2"
                },
                "2": {
                    "type": "process",
                    "binary_ref": "0"
                }
            },
            "modified": "2018-12-11T11:47:44.000Z"
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


